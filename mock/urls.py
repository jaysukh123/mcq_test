from django.urls import path
from .views import (
    home, exams_view, exam_list, exam_detail, categories, subcategories, 
    test_series, aptitude_home, syllabus_view, books_view, papers, mcq_view, about, privacy, contact, search, upload_mcq, 
)

urlpatterns = [
    path('', home, name='home'),
    
    # Aptitude Section
    path('aptitude/', aptitude_home, name='aptitude'),
    path('syllabus/', syllabus_view, name='syllabus'),
    path('books/', books_view, name='books'),

    # Exam Routes
    path('exams/', exams_view, name='exams'),
    path('exams/list/', exam_list, name='exam_list'),
    path('exams/<slug:exam_slug>/', exam_detail, name='exam_detail'),

    # Category and Subcategory Routes
    path('categories/', categories, name='categories'),
    path('categories/<slug:category_slug>/', subcategories, name='subcategories'),
    
    # Papers and MCQs
    path('categories/<slug:category_slug>/<slug:subcategory_slug>/papers/', papers, name='papers'),
    path('categories/<slug:category_slug>/<slug:subcategory_slug>/papers/<int:paper_id>/MCQ/', mcq_view, name='mcq_view'),

    # Test Series
    path('test-series/<slug:slug>/', test_series, name='test_series'),
    path('about/',about, name='about'),
    path('privacy/', privacy, name='privacy'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('upload-mcq/', upload_mcq, name='upload_mcq'),
    
]    

   


