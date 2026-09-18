"""
models/subject.py
------------------
Subject -- a small value object representing one subject and the marks a
student scored in it. Demonstrates a lightweight OOP class with
encapsulated behaviour (is_pass, grade) rather than a bare dictionary.
"""

from src.config import MAX_MARKS_PER_SUBJECT, PASS_MARKS_PER_SUBJECT


class Subject:
    """A single subject-mark pair belonging to a student."""

    __slots__ = ("name", "marks")

    def __init__(self, name: str, marks: float):
        self.name = name
        self.marks = marks

    def is_pass(self) -> bool:
        """A subject is passed if marks >= the configured passing threshold."""
        return self.marks >= PASS_MARKS_PER_SUBJECT

    def percentage(self) -> float:
        return round((self.marks / MAX_MARKS_PER_SUBJECT) * 100, 2)

    def __str__(self):
        status = "Pass" if self.is_pass() else "Fail"
        return f"{self.name:<18}: {self.marks:>6.2f} / {MAX_MARKS_PER_SUBJECT}  [{status}]"

    def __repr__(self):
        return f"Subject(name={self.name!r}, marks={self.marks!r})"
