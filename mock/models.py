from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    """Main category for syllabus (e.g., Engineering, Medical, etc.)."""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    syllabus_file = models.FileField(upload_to='syllabus/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).lower()  # Auto-generate slug from name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Subcategory for each category (e.g., Physics, Chemistry under Engineering)."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=100, blank=True, null=True)  # Optional icon for UI
    syllabus_file = models.FileField(upload_to='syllabus/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Exam(models.Model):
    CATEGORY_CHOICES = [
        ('engineering', 'Engineering'),
        ('medical', 'Medical'),
        ('government', 'Government'),
        ('banking', 'Banking'),
    ]
    
    SUBCATEGORY_CHOICES = [
        ('jee', 'JEE Main'),
        ('gate', 'GATE'),
        ('neet', 'NEET'),
        ('aiims', 'AIIMS'),
        ('ssc', 'SSC'),
        ('upsc', 'UPSC'),
        ('ibps', 'IBPS'),
        ('sbi-po', 'SBI PO'),
    ]

    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    exam_date = models.DateField(blank=True, null=True)
    eligibility = models.TextField(blank=True, null=True)
    exam_mode = models.CharField(max_length=100, blank=True, null=True)
    subjects = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    marking_scheme = models.TextField(blank=True, null=True)
    official_website = models.URLField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Paper(models.Model):
    """Represents a past exam paper linked to a subcategory."""
    name = models.CharField(max_length=100, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, related_name='papers', on_delete=models.CASCADE)

    def __str__(self):
        return self.name if self.name else "Unnamed Paper"


class MCQ(models.Model):
    """Stores multiple-choice questions for each paper."""
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name='mcqs')
    year = models.IntegerField() 
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    explanation = models.TextField(blank=True, null=True)  # Optional explanation

    def __str__(self):
        return f"{self.paper.name} - {self.question[:50]}"  # Shorten long questions in __str__
    
    


class AptitudeCategory(models.Model):
    """Category for aptitude questions."""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']  # Sort categories alphabetically

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AptitudeSubCategory(models.Model):
    """Subcategory for aptitude questions."""
    category = models.ForeignKey(AptitudeCategory, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class ContactMessage(models.Model):
    """Model for storing contact form messages."""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
