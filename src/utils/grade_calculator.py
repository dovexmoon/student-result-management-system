"""
utils/grade_calculator.py
--------------------------
Converts a numeric percentage into a letter grade using the GRADE_TABLE
defined in config.py.

Kept as a standalone function (not a method) because it has no state of
its own and is reused by both Student.overall_grade() and the reporting
layer -- a good example of "functions" (module: Functions in Python) doing
one clearly-scoped job, and is directly unit-tested in tests/test_grade_calculator.py.
"""

from src.config import GRADE_TABLE


def grade_for_percentage(percentage: float) -> str:
    """
    Walk the GRADE_TABLE (ordered highest boundary first) and return the
    first grade whose lower bound the percentage satisfies.

    Demonstrates control flow (for + if) and operator precedence
    (comparison operators) called out explicitly in the syllabus.
    """
    for lower_bound, grade in GRADE_TABLE:
        if percentage >= lower_bound:
            return grade
    return "F"  # unreachable in practice since GRADE_TABLE's last bound is 0.0


def letter_to_grade_point(grade: str) -> float:
    """Optional helper: maps a letter grade to a 0-10 grade point (GPA-style)."""
    mapping = {
        "A+": 10.0, "A": 9.0, "B+": 8.0, "B": 7.0,
        "C": 6.0, "D": 5.0, "F": 0.0,
    }
    return mapping.get(grade, 0.0)
