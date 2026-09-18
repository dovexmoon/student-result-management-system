"""
config.py
---------
Central configuration for the Student Result Management System (SRMS).

Keeping constants in one place (instead of scattering "magic numbers"
through the codebase) is a maintainability / non-functional requirement
of the project (see docs/report.pdf, section: Non-Functional Requirements).
"""

import os

# ---------------------------------------------------------------------------
# File paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STUDENTS_CSV = os.path.join(DATA_DIR, "students.csv")
REPORT_CSV = os.path.join(DATA_DIR, "class_report.csv")

# ---------------------------------------------------------------------------
# Academic configuration
# ---------------------------------------------------------------------------
# The fixed set of subjects offered. Using a tuple (immutable) because this
# list should not change at runtime -- demonstrates correct use of tuples
# vs lists (module: Core Data Structures).
SUBJECTS = ("Python", "Mathematics", "Data Structures", "English", "Computer Networks")

MAX_MARKS_PER_SUBJECT = 100
PASS_MARKS_PER_SUBJECT = 35   # a student must score >= this to pass a subject
PASS_PERCENTAGE = 40.0        # overall pass threshold

# Grade boundaries expressed as a list of (lower_bound_percentage, grade) tuples,
# ordered highest to lowest. Iterated top-down in utils/grade_calculator.py
# (module: Precedence & Associativity / Control Flow).
GRADE_TABLE = [
    (90.0, "A+"),
    (80.0, "A"),
    (70.0, "B+"),
    (60.0, "B"),
    (50.0, "C"),
    (PASS_PERCENTAGE, "D"),
    (0.0, "F"),
]

# CSV column order -- single source of truth used by both the writer and
# the reader so they can never silently drift apart.
CSV_FIELDNAMES = ["roll_no", "name"] + list(SUBJECTS)
