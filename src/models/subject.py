from src.config import MAX_MARKS_PER_SUBJECT, PASS_MARKS_PER_SUBJECT


class Subject:

    __slots__ = ("name", "marks")

    def __init__(self, name: str, marks: float):
        self.name = name
        self.marks = marks

    def is_pass(self):
        
        return self.marks >= PASS_MARKS_PER_SUBJECT

    def percentage(self):
        return round((self.marks / MAX_MARKS_PER_SUBJECT) * 100, 2)

    def __str__(self):
        status = "Pass" if self.is_pass() else "Fail"
        return f"{self.name:<18}: {self.marks:>6.2f} / {MAX_MARKS_PER_SUBJECT}  [{status}]"

    def __repr__(self):
        return "Subject(name={!r}, marks={!r})".format(self.name, self.marks)

