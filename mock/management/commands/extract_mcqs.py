from django.core.management.base import BaseCommand
from mock.utils import extract_mcqs_from_pdf  # Move the function to utils.py
from mock.models import Paper

class Command(BaseCommand):
    help = "Extract MCQs from a PDF and save them to the database."

    def add_arguments(self, parser):
        parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
        parser.add_argument("paper_id", type=int, help="Paper ID to associate MCQs with")

    def handle(self, *args, **kwargs):
        pdf_path = kwargs["pdf_path"]
        paper_id = kwargs["paper_id"]
        try:
            message = extract_mcqs_from_pdf(pdf_path, paper_id)
            self.stdout.write(self.style.SUCCESS(message))
        except Paper.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Paper with ID {paper_id} does not exist."))
