from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from .models import Category, Paper, MCQ, Exam, Subcategory, AptitudeCategory
from .forms import ContactForm, FileUploadForm
import pandas as pd
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import re

# ============================== Home Views ==============================

def home(request):
    """Render the home page."""
    return render(request, 'home.html')

def aptitude_home(request):
    """Render aptitude home page with categories."""
    categories = AptitudeCategory.objects.prefetch_related('subcategories').all()
    return render(request, 'aptitude.html', {'categories': categories})

# ============================== Syllabus & Books ==============================

def syllabus_view(request):
    """Display syllabus categories."""
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'syllabus.html', {'categories': categories})

def books_view(request):
    """Render books page."""
    return render(request, 'books.html')

# ============================== Exam Views ==============================

def exams_view(request):
    """Render exams home page."""
    return render(request, 'exam.html')
def exam_list(request):
    exams = Exam.objects.all()
    categories = Exam.CATEGORY_CHOICES
    subcategories = Exam.SUBCATEGORY_CHOICES

    return render(request, 'exams.html', {
        'exams': exams,
        'categories': categories,
        'subcategories': subcategories,
    })

def exam_detail(request, exam_slug):
    """Display details of a specific exam."""
    exam = get_object_or_404(Exam, slug=exam_slug)
    return render(request, 'exam_detail.html', {'exam': exam})

# ============================== Categories & Subcategories ==============================

def categories(request):
    """Retrieve and cache all categories."""
    categories_data = cache.get_or_set('categories', Category.objects.prefetch_related('subcategories').all(), timeout=300)
    return render(request, 'categories.html', {'categories': categories_data})

def subcategories(request, category_slug):
    """Retrieve subcategories for a given category."""
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'subcategories.html', {'category': category, 'subcategories': category.subcategories.all()})

def test_series(request, slug):
    """Render test series page."""
    return render(request, 'test_series.html', {'slug': slug})

# ============================== Papers & MCQs ==============================

def papers(request, category_slug, subcategory_slug):
    """Retrieve papers based on category and subcategory."""
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(Subcategory, slug=subcategory_slug, category=category)
    return render(request, 'papers.html', {'category': category, 'subcategory': subcategory, 'papers': Paper.objects.filter(subcategory=subcategory)})

def mcq_view(request, category_slug, subcategory_slug, paper_id):
    """Display MCQs for a given paper with pagination."""
    paper = get_object_or_404(Paper, id=paper_id, subcategory__slug=subcategory_slug, subcategory__category__slug=category_slug)
    mcqs = MCQ.objects.filter(paper=paper)
    paginator = Paginator(mcqs, request.GET.get('per_page', 10))
    return render(request, 'mcq.html', {'paper': paper, 'page_obj': paginator.get_page(request.GET.get('page'))})

# ============================== Static Pages ==============================

def about(request):
    return render(request, 'about.html')

def privacy(request):
    return render(request, 'privacy.html')

# ============================== Contact Form ==============================

def contact(request):
    """Handle contact form submission."""
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    return render(request, "contact.html", {"form": form})

# ============================== Search Functionality ==============================



from django.db.models import Q
from django.shortcuts import render

def search(request):
    query = request.GET.get('query', '').strip()  # Ensures query always has a value

    if query:
        exams = Exam.objects.filter(Q(name__icontains=query))
        books = Paper.objects.filter(Q(name__icontains=query))
        syllabus = Category.objects.filter(Q(name__icontains=query))
    else:
        exams = books = syllabus = []  # Empty lists when no search query

    results = {'exams': exams, 'books': books, 'syllabus': syllabus}

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'search_results_list.html', {'results': results})

    return render(request, 'search_results.html', {'query': query, 'results': results})


# ============================== MCQ File Upload ==============================

def upload_mcq(request):
    """Handle MCQ file uploads and process CSV/XLS/JSON files."""
    form = FileUploadForm(request.POST or None, request.FILES or None)
    
    if request.method == "POST" and form.is_valid():
        file = request.FILES['file']
        file_extension = file.name.split('.')[-1].lower()

        try:
            if file_extension == 'csv':
                df = pd.read_csv(file)
            elif file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(file)
            elif file_extension == 'json':
                data = json.load(file)
                df = pd.DataFrame(data)  # Convert JSON data to DataFrame
            else:
                messages.error(request, "Unsupported file format.")
                return redirect('upload_mcq')

            for _, row in df.iterrows():
                MCQ.objects.create(
                    question=row['question'],
                    option_a=row['option_a'],
                    option_b=row['option_b'],
                    option_c=row['option_c'],
                    option_d=row['option_d'],
                    correct_answer=row['correct_answer'],
                    paper=Paper.objects.get(id=row['paper_id'])
                )

            messages.success(request, "MCQs uploaded successfully!")

        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")

        return redirect('upload_mcq')

    return render(request, 'upload_mcq.html', {'form': form})

# ============================== MCQ List ==============================

def mcq_list(request):
    """List all MCQs with pagination."""
    paginator = Paginator(MCQ.objects.all(), 20)
    return render(request, 'mcq_list.html', {'page_obj': paginator.get_page(request.GET.get('page'))})
