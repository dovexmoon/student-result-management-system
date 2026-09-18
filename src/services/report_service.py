"""
services/report_service.py
----------------------------
FUNCTIONAL MODULE 2: Result Processing & Grading
FUNCTIONAL MODULE 3: Reporting & Analytics

Everything here is *read-only* with respect to the roster -- it derives
marksheets, rankings and class-wide statistics from the students handed to
it by ResultManager. Kept as a separate class so grading/reporting logic
is not tangled up with CRUD logic (single-responsibility).

Demonstrates the "array" data structure explicitly (module: Array data
structure in Python) via Python's built-in `array` module, used for the
class's percentage figures where a homogeneous, memory-compact numeric
array is a more appropriate fit than a general-purpose list.
"""

from array import array
from typing import List

from src.config import SUBJECTS
from src.exceptions import EmptyDatasetError
from src.models.student import Student


class ReportService:
    """Generates marksheets, rankings and class-wide statistics."""

    # ------------------------------------------------------------------ #
    # Single-student report
    # ------------------------------------------------------------------ #
    @staticmethod
    def marksheet(student: Student) -> str:
        lines = [
            "=" * 46,
            f" MARKSHEET -- {student.name} (Roll No: {student.roll_no})",
            "=" * 46,
        ]
        for subject in student.subjects.values():
            lines.append(str(subject))
        lines.append("-" * 46)
        lines.append(f"{'Total':<18}: {student.total_marks():>6.2f} / {student.max_possible_marks()}")
        lines.append(f"{'Percentage':<18}: {student.percentage():>6.2f}%")
        lines.append(f"{'Grade':<18}: {student.overall_grade()}")
        result = "PASS" if student.is_overall_pass() else "FAIL"
        lines.append(f"{'Result':<18}: {result}")
        if student.failed_subjects():
            lines.append(f"{'Backlog(s)':<18}: {', '.join(student.failed_subjects())}")
        lines.append("=" * 46)
        return "\n".join(lines)

    # ------------------------------------------------------------------ #
    # Class-wide analytics
    # ------------------------------------------------------------------ #
    @staticmethod
    def _percentage_array(students: List[Student]) -> "array[float]":
        """Build a compact 'f' (float) array of every student's percentage."""
        return array("f", [s.percentage() for s in students])

    @classmethod
    def class_average(cls, students: List[Student]) -> float:
        if not students:
            raise EmptyDatasetError("Cannot compute an average of zero students.")
        percentages = cls._percentage_array(students)
        return round(sum(percentages) / len(percentages), 2)

    @classmethod
    def topper(cls, students: List[Student]) -> Student:
        if not students:
            raise EmptyDatasetError("Cannot find a topper with zero students.")
        return max(students, key=lambda s: s.percentage())

    @classmethod
    def rank_list(cls, students: List[Student]) -> List[Student]:
        """Highest percentage first. Ties broken by roll number for stability."""
        if not students:
            raise EmptyDatasetError("Cannot rank zero students.")
        return sorted(students, key=lambda s: (-s.percentage(), s.roll_no))

    @classmethod
    def pass_fail_summary(cls, students: List[Student]) -> dict:
        if not students:
            raise EmptyDatasetError("Cannot summarise zero students.")
        passed = sum(1 for s in students if s.is_overall_pass())
        failed = len(students) - passed
        return {"passed": passed, "failed": failed, "total": len(students)}

    @classmethod
    def subject_wise_average(cls, students: List[Student]) -> dict:
        """dict comprehension: {subject_name: average_marks_across_all_students}."""
        if not students:
            raise EmptyDatasetError("Cannot compute subject averages with zero students.")
        return {
            subject: round(
                sum(s.subjects[subject].marks for s in students if subject in s.subjects)
                / len(students),
                2,
            )
            for subject in SUBJECTS
        }

    @classmethod
    def export_rows(cls, students: List[Student]) -> List[dict]:
        """Flat rows (rank, roll_no, name, total, percentage, grade, result) for CSV export."""
        rows = []
        for rank, student in enumerate(cls.rank_list(students), start=1):
            rows.append({
                "rank": rank,
                "roll_no": student.roll_no,
                "name": student.name,
                "total": student.total_marks(),
                "percentage": student.percentage(),
                "grade": student.overall_grade(),
                "result": "PASS" if student.is_overall_pass() else "FAIL",
            })
        return rows
