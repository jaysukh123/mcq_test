import os
import csv
from django.core.management.base import BaseCommand
from mock.models import MCQ, Subcategory, Paper

class Command(BaseCommand):
    help = "Import MCQs from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help="Path to CSV file")

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # ✅ Check if file exists before proceeding
        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
            return

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Get or create related objects
                    subcategory, _ = Subcategory.objects.get_or_create(name=row['subcategory'])
                    paper, _ = Paper.objects.get_or_create(name=row['paper'], subcategory=subcategory)

                    # Create MCQ
                    MCQ.objects.create(
                        subcategory=subcategory,
                        paper=paper,
                        year=int(row['year']),
                        question=row['question'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        option_d=row['option_d'],
                        correct_answer=row['correct_answer'],
                        explanation=row['explanation'],
                    )
                    self.stdout.write(self.style.SUCCESS(f"Added MCQ: {row['question'][:50]}..."))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error importing: {row['question'][:50]} - {e}"))

        self.stdout.write(self.style.SUCCESS("CSV Import Completed! 🎉"))
