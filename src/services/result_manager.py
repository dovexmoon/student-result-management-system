"""
services/result_manager.py
----------------------------
FUNCTIONAL MODULE 1: Student & Marks Management.

Owns the in-memory roster (a list of Student objects) and every CRUD
operation on it: add, remove, update marks, search, list. Persistence is
delegated to FileHandler so this class only contains business rules.

Data structures on display: list (self._students), set (self._roll_index
for O(1) duplicate detection), dict (returned by search).
"""

from typing import List, Optional

from src.exceptions import DuplicateStudentError, StudentNotFoundError
from src.models.student import Student
from src.services.file_handler import FileHandler


class ResultManager:
    """CRUD + lookup operations over the roster of students."""

    def __init__(self, file_handler: Optional[FileHandler] = None):
        self.file_handler = file_handler or FileHandler()
        self._students: List[Student] = self.file_handler.load_students()
        # A set gives O(1) "does this roll number already exist" checks,
        # instead of scanning the whole list every time (module: Core Data
        # Structures -- choosing the right structure for the job).
        self._roll_index = {s.roll_no for s in self._students}

    # ------------------------------------------------------------------ #
    # Persistence
    # ------------------------------------------------------------------ #
    def save(self) -> None:
        self.file_handler.save_students(self._students)

    # ------------------------------------------------------------------ #
    # Create
    # ------------------------------------------------------------------ #
    def add_student(self, roll_no: str, name: str) -> Student:
        if roll_no in self._roll_index:
            raise DuplicateStudentError(roll_no)
        student = Student(roll_no, name)
        self._students.append(student)
        self._roll_index.add(roll_no)
        return student

    # ------------------------------------------------------------------ #
    # Read
    # ------------------------------------------------------------------ #
    def get_student(self, roll_no: str) -> Student:
        for student in self._students:
            if student.roll_no == roll_no:
                return student
        raise StudentNotFoundError(roll_no)

    def list_students(self) -> List[Student]:
        return list(self._students)  # return a copy -- protects internal state

    def search_by_name(self, keyword: str) -> List[Student]:
        keyword = keyword.strip().lower()
        return [s for s in self._students if keyword in s.name.lower()]

    def count(self) -> int:
        return len(self._students)

    # ------------------------------------------------------------------ #
    # Update
    # ------------------------------------------------------------------ #
    def update_marks(self, roll_no: str, subject: str, marks: float) -> Student:
        student = self.get_student(roll_no)  # raises StudentNotFoundError if missing
        student.set_marks(subject, marks)
        return student

    def update_name(self, roll_no: str, new_name: str) -> Student:
        student = self.get_student(roll_no)
        student.name = new_name
        return student

    # ------------------------------------------------------------------ #
    # Delete
    # ------------------------------------------------------------------ #
    def remove_student(self, roll_no: str) -> None:
        student = self.get_student(roll_no)  # validates existence first
        self._students.remove(student)
        self._roll_index.discard(roll_no)
