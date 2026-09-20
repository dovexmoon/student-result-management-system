from src.config import SUBJECTS, MAX_MARKS_PER_SUBJECT, PASS_PERCENTAGE
from src.models.subject import Subject
from src.utils.grade_calculator import grade_for_percentage


class Student:
   def __init__(self, roll_no: str, name: str):
        self.roll_no = roll_no
        self.name = name
  
        self.subjects: dict[str, Subject] = {}
    @classmethod
    def from_csv_row(cls, row: dict):
        student = cls(roll_no=row["roll_no"], name=row["name"])
        for subject_name in SUBJECTS:
            raw = row.get(subject_name, "")
            marks = float(raw) if raw not in ("", None) else 0.0
            student.subjects[subject_name] = Subject(subject_name, marks)
        return student
    def set_marks(self, subject_name: str, marks: float):
        self.subjects[subject_name] = Subject(subject_name, marks)
    def total_marks(self) -> float:
        return sum(subject.marks for subject in self.subjects.values())

    def max_possible_marks(self):
        return len(SUBJECTS) * MAX_MARKS_PER_SUBJECT

    def percentage(self):
        if not self.subjects:
            return 0.0
        return round((self.total_marks() / self.max_possible_marks()) * 100, 2)

    def overall_grade(self):
        return grade_for_percentage(self.percentage())

    def failed_subjects(self):
        """List of subject names the student did not clear."""
        return [s.name for s in self.subjects.values() if not s.is_pass()]

    def is_overall_pass(self):
        return self.percentage() >= PASS_PERCENTAGE and not self.failed_subjects()

    def to_csv_row(self):
        row = {"roll_no": self.roll_no, "name": self.name}
        for subject_name in SUBJECTS:
            subject = self.subjects.get(subject_name)
            row[subject_name] = subject.marks if subject else 0.0
        return row


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
