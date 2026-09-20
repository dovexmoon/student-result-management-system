import csv
import os
from typing import List

from src.config import CSV_FIELDNAMES, STUDENTS_CSV
from src.models.student import Student


class FileHandler:
    def __init__(self, path: str = STUDENTS_CSV):
        self.path = path

    def load_students(self) -> List[Student]:
        if not os.path.exists(self.path):
            return []

        students = []
        with open(self.path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(Student.from_csv_row(row))
        return students

    def save_students(self, students: List[Student]):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            for student in students:
                writer.writerow(student.to_csv_row())

    def export_rows(self, path: str, fieldnames: List[str], rows: List[dict]):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
