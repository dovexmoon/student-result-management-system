"""
utils/validators.py
--------------------
Pure functions that validate raw user input and convert it into the correct
Python type, raising a specific custom exception on failure. Centralising
this logic (rather than repeating it inside the CLI) is what lets the rest
of the codebase trust that a "marks" value in memory is always a valid
float in range, etc.

Demonstrates: type conversion (str -> int/float), operators, and control
flow (module: Type Conversion, Precedence & Associativity, Control Flow).
"""

from src.config import SUBJECTS, MAX_MARKS_PER_SUBJECT
from src.exceptions import (
    InvalidRollNumberError,
    InvalidNameError,
    InvalidMarksError,
    InvalidSubjectError,
)


def validate_roll_no(raw: str) -> str:
    roll_no = raw.strip().upper()
    if not roll_no:
        raise InvalidRollNumberError("Roll number cannot be empty.")
    if not roll_no.isalnum():
        raise InvalidRollNumberError(
            "Roll number must be alphanumeric (letters/digits only)."
        )
    return roll_no


def validate_name(raw: str) -> str:
    name = raw.strip()
    if not name:
        raise InvalidNameError("Name cannot be empty.")
    if not all(ch.isalpha() or ch.isspace() for ch in name):
        raise InvalidNameError("Name must contain only letters and spaces.")
    return name.title()


def validate_subject(raw: str) -> str:
    subject = raw.strip()
    # Case-insensitive match against the configured subject list.
    for known in SUBJECTS:
        if known.lower() == subject.lower():
            return known
    raise InvalidSubjectError(
        f"'{raw}' is not a recognised subject. Choose from: {', '.join(SUBJECTS)}"
    )


def validate_marks(raw: str) -> float:
    try:
        marks = float(raw)  # type conversion, may raise ValueError
    except ValueError:
        raise InvalidMarksError(f"'{raw}' is not a valid number.")

    if marks < 0 or marks > MAX_MARKS_PER_SUBJECT:
        raise InvalidMarksError(
            f"Marks must be between 0 and {MAX_MARKS_PER_SUBJECT} (got {marks})."
        )
    return round(marks, 2)
