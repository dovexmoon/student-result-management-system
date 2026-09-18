"""
services/file_handler.py
-------------------------
All disk I/O lives here and nowhere else in the codebase (single
responsibility). Isolating I/O like this means the rest of the app can be
unit-tested without touching the filesystem, and it's the only place that
needs to know the on-disk format is CSV -- swapping to JSON/SQLite later
would only require changes in this one file.

Demonstrates: file Input/Output operations (module: Input and Output
operations in Python) and defensive error handling.
"""

import csv
import os
from typing import List

from src.config import CSV_FIELDNAMES, STUDENTS_CSV
from src.models.student import Student


class FileHandler:
    """Reads and writes the roster of students to a CSV file."""

    def __init__(self, path: str = STUDENTS_CSV):
        self.path = path

    def load_students(self) -> List[Student]:
        """
        Load all students from the CSV file.
        Returns an empty list (not an error) if the file does not exist yet --
        a brand-new install should just start with an empty roster.
        """
        if not os.path.exists(self.path):
            return []

        students = []
        with open(self.path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(Student.from_csv_row(row))
        return students

    def save_students(self, students: List[Student]) -> None:
        """Overwrite the CSV file with the current in-memory roster."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            for student in students:
                writer.writerow(student.to_csv_row())

    def export_rows(self, path: str, fieldnames: List[str], rows: List[dict]) -> None:
        """Generic helper used by ReportService to export arbitrary tabular reports."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
