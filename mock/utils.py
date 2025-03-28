import pandas as pd
import fitz  # PyMuPDF for PDFs
import csv
from io import TextIOWrapper
from .models import MCQ, Paper, Subcategory

def process_csv(file):
    """Processes CSV files and saves data into the MCQ model."""
    decoded_file = TextIOWrapper(file, encoding='utf-8')
    reader = csv.reader(decoded_file)
    next(reader)  # Skip header row
    for row in reader:
        paper, _ = Paper.objects.get_or_create(name=row[0])
        MCQ.objects.create(
            paper=paper,
            year=int(row[1]),
            question=row[2],
            option_a=row[3],
            option_b=row[4],
            option_c=row[5],
            option_d=row[6],
            correct_answer=row[7]
        )

def process_excel(file):
    """Processes Excel files and saves data into the MCQ model."""
    df = pd.read_excel(file)
    for _, row in df.iterrows():
        paper, _ = Paper.objects.get_or_create(name=row['Paper Name'])
        MCQ.objects.create(
            paper=paper,
            year=row['Year'],
            question=row['Question'],
            option_a=row['Option A'],
            option_b=row['Option B'],
            option_c=row['Option C'],
            option_d=row['Option D'],
            correct_answer=row['Correct Answer']
        )

def process_pdf(file):
    """Extracts text from a PDF file and processes MCQs."""
    doc = fitz.open(file)
    text = ""
    for page in doc:
        text += page.get_text("text")  # Extract text from each page
    lines = text.split("\n")
    
    for i in range(0, len(lines), 7):  # Assuming 7 lines per MCQ (Adjust if needed)
        try:
            paper, _ = Paper.objects.get_or_create(name="Extracted Paper")
            MCQ.objects.create(
                paper=paper,
                year=2025,  # Assume current year if not provided
                question=lines[i].strip(),
                option_a=lines[i+1].strip(),
                option_b=lines[i+2].strip(),
                option_c=lines[i+3].strip(),
                option_d=lines[i+4].strip(),
                correct_answer=lines[i+5].strip()
            )
        except IndexError:
            continue  # Skip if there are missing data points
