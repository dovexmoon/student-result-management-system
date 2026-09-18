"""
models/student.py
------------------
Student -- the central OOP class of the system (module: Object Oriented
Programming in Python).

Encapsulates:
    * identity data (roll_no, name)
    * a dict of Subject objects (module: Core Data Structures -> dict)
    * behaviour: total, percentage, grade, pass/fail (module: Control Flow,
      Precedence & Associativity for the arithmetic involved)

Class methods provide alternate constructors (a common, idiomatic OOP
pattern) for building a Student either freshly or from a CSV row.
"""

from src.config import SUBJECTS, MAX_MARKS_PER_SUBJECT, PASS_PERCENTAGE
from src.models.subject import Subject
from src.utils.grade_calculator import grade_for_percentage


class Student:
    """Represents one student and all of their subject marks."""

    def __init__(self, roll_no: str, name: str):
        self.roll_no = roll_no
        self.name = name
        # dict[str, Subject] -- keyed by subject name for O(1) lookup/update
        self.subjects: dict[str, Subject] = {}

    # ------------------------------------------------------------------ #
    # Alternate constructors
    # ------------------------------------------------------------------ #
    @classmethod
    def from_csv_row(cls, row: dict) -> "Student":
        """Build a Student from a csv.DictReader row (all values are strings)."""
        student = cls(roll_no=row["roll_no"], name=row["name"])
        for subject_name in SUBJECTS:
            raw = row.get(subject_name, "")
            # type conversion: CSV always gives strings, we need floats
            marks = float(raw) if raw not in ("", None) else 0.0
            student.subjects[subject_name] = Subject(subject_name, marks)
        return student

    # ------------------------------------------------------------------ #
    # Mutators
    # ------------------------------------------------------------------ #
    def set_marks(self, subject_name: str, marks: float) -> None:
        self.subjects[subject_name] = Subject(subject_name, marks)

    # ------------------------------------------------------------------ #
    # Derived / computed properties
    # ------------------------------------------------------------------ #
    def total_marks(self) -> float:
        return sum(subject.marks for subject in self.subjects.values())

    def max_possible_marks(self) -> int:
        return len(SUBJECTS) * MAX_MARKS_PER_SUBJECT

    def percentage(self) -> float:
        if not self.subjects:
            return 0.0
        return round((self.total_marks() / self.max_possible_marks()) * 100, 2)

    def overall_grade(self) -> str:
        return grade_for_percentage(self.percentage())

    def failed_subjects(self) -> list:
        """List of subject names the student did not clear."""
        return [s.name for s in self.subjects.values() if not s.is_pass()]

    def is_overall_pass(self) -> bool:
        # Overall pass requires BOTH a minimum aggregate percentage AND
        # no individual subject failures -- a realistic academic rule.
        return self.percentage() >= PASS_PERCENTAGE and not self.failed_subjects()

    # ------------------------------------------------------------------ #
    # Serialization
    # ------------------------------------------------------------------ #
    def to_csv_row(self) -> dict:
        row = {"roll_no": self.roll_no, "name": self.name}
        for subject_name in SUBJECTS:
            subject = self.subjects.get(subject_name)
            row[subject_name] = subject.marks if subject else 0.0
        return row

    # ------------------------------------------------------------------ #
    # Dunder / display methods
    # ------------------------------------------------------------------ #
    def __str__(self):
        return f"[{self.roll_no}] {self.name} -- {self.percentage()}% ({self.overall_grade()})"

    def __repr__(self):
        return f"Student(roll_no={self.roll_no!r}, name={self.name!r})"

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.roll_no == other.roll_no

    def __hash__(self):
        return hash(self.roll_no)
