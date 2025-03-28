from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import json

from .models import Category, Subcategory, Exam, MCQ, Paper, AptitudeCategory, AptitudeSubCategory
from import_export.admin import ExportMixin, ImportMixin
from import_export.resources import ModelResource
from import_export.formats.base_formats import CSV, XLSX, JSON


# ==============================
# REGISTER OTHER MODELS
# ==============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'syllabus_file')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Paper)


@admin.register(AptitudeCategory)
class AptitudeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AptitudeSubCategory)
class AptitudeSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['category']


# ==============================
# MCQ ADMIN PANEL WITH JSON IMPORT
# ==============================
class MCQResource(ModelResource):
    class Meta:
        model = MCQ
        import_id_fields = ['id']

    def get_import_formats(self):
        return [CSV(), XLSX(), JSON()]  # Add JSON here

@admin.register(MCQ)
class MCQAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):
    list_display = ('question', 'paper', 'correct_answer')
    search_fields = ('question', 'paper__name')
    resource_class = MCQResource
    formats = [CSV, XLSX, JSON]  # Add JSON format here

    # Custom admin view for JSON upload
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-json/', self.admin_site.admin_view(self.import_json), name="import_json"),
        ]
        return custom_urls + urls

    def import_json(self, request):
        """Admin panel view to handle JSON MCQ file upload."""
        if request.method == "POST" and request.FILES.get("json_file"):
            try:
                file = request.FILES["json_file"]
                data = json.load(file)

                for item in data:
                    MCQ.objects.create(
                        question=item['question'],
                        option_a=item['option_a'],
                        option_b=item['option_b'],
                        option_c=item['option_c'],
                        option_d=item['option_d'],
                        correct_answer=item['correct_answer'],
                        paper=Paper.objects.get(id=item['paper_id'])
                    )

                messages.success(request, "MCQs imported successfully!")
                return redirect("admin:mock_mcq_changelist")  # Replace 'yourapp' with actual app name

            except Exception as e:
                messages.error(request, f"Error importing JSON: {str(e)}")

        return render(request, "admin/import_json.html")
