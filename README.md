# Student Result Management System (SRMS)

A command-line application, written in pure Python, that lets a teacher/administrator
manage a class roster, record subject-wise marks, compute grades, and generate
class-wide analytics and reports — built as the course project for **VITyarthi:
Build Your Own Project** (Python — Modules 1 to 12: Introduction to Fundamentals,
Data Structures, Control Flow, Functions, Modules & Packages, Arrays, and OOP).

---

## Overview

Managing student results by hand (or in a scattered spreadsheet) is error-prone
and hard to analyse. SRMS gives a teacher a single, reliable, offline tool to:

- maintain a roster of students,
- enter/update subject-wise marks with input validation,
- automatically compute totals, percentages and letter grades,
- generate a formatted marksheet for any student,
- rank the whole class and compute pass/fail and subject-wise statistics,
- export a class report to CSV.

All data is persisted to a plain CSV file (`data/students.csv`), so no database
server or internet connection is required.

## Features

| # | Functional Module | What it does |
|---|---|---|
| 1 | **Student & Marks Management** | Add, update, search, list and remove students; enter/update marks per subject, with full input validation. |
| 2 | **Result Processing & Grading** | Computes total marks, percentage, and letter grade (A+ → F) per student, and per-subject pass/fail status, using configurable grade boundaries. |
| 3 | **Reporting & Analytics** | Class rank list, topper, class average, subject-wise averages, pass/fail summary, and CSV export of the full class report. |

## Technologies / Tools Used

- **Language:** Python 3.9+ (standard library only — no third-party packages)
- **Core modules used:** `csv` (file I/O / persistence), `array` (compact numeric storage for class statistics), `unittest` (testing), `os`, `sys`
- **Concepts applied:** variables & operators, type conversion, precedence, core data structures (list, dict, tuple, set, array), control flow, functions, packages/modules, array data structures, and full Object-Oriented Programming (classes, encapsulation, inheritance via custom exceptions, class/static methods, dunder methods)
- **Version control:** Git / GitHub

## Project Structure

```
student-result-management-system/
├── main.py                        # CLI entry point (menu-driven)
├── requirements.txt                # documents "stdlib only" — no installs needed
├── README.md
├── statement.md                    # problem statement, scope, target users
├── data/
│   └── students.csv                # sample seed data (5 students)
├── src/
│   ├── config.py                   # constants: subjects, grade table, file paths
│   ├── exceptions.py                # custom exception hierarchy
│   ├── models/
│   │   ├── student.py               # Student class (OOP)
│   │   └── subject.py               # Subject class (OOP)
│   ├── services/
│   │   ├── file_handler.py          # CSV read/write (persistence layer)
│   │   ├── result_manager.py        # Functional Module 1: CRUD
│   │   └── report_service.py        # Functional Modules 2 & 3: grading + analytics
│   └── utils/
│       ├── validators.py            # input validation + type conversion
│       └── grade_calculator.py      # percentage -> letter grade logic
├── tests/
│   └── test_grade_calculator.py     # unit tests (17 tests)
└── docs/
    ├── generate_diagrams.py         # regenerates all diagrams below
    └── diagrams/                    # architecture, workflow, use case, class, sequence
```

This is 13 Python files in a properly packaged structure (`src/`, `src/models/`,
`src/services/`, `src/utils/`, `tests/`), well above the minimum of 5–10
meaningful modules/files.

## Setup & Installation

### Prerequisites
- Python 3.9 or later installed ([python.org](https://www.python.org/downloads/))
- Git (to clone the repository)

Check your Python version:
```bash
python3 --version
```

### 1. Clone the repository
```bash
git clone https://github.com/{github-username}/{repo-name}.git
cd {repo-name}
```

### 2. (Optional but recommended) create a virtual environment
No third-party packages are required, so this is optional — but it's good
practice:
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
There are none beyond the Python standard library. `requirements.txt` is
included to document this explicitly:
```bash
pip install -r requirements.txt
```

## How to Run

From the project root:
```bash
python3 main.py
```

You'll see a menu-driven interface:
```
╔══════════════════════════════════════════════════╗
║   STUDENT RESULT MANAGEMENT SYSTEM                ║
╠══════════════════════════════════════════════════╣
║  1. Add new student                               ║
║  2. Enter / update marks for a student            ║
║  3. View a student's marksheet                    ║
║  4. List all students                             ║
║  5. Search students by name                       ║
║  6. Remove a student                              ║
║  7. Class rank list                               ║
║  8. Class statistics (average, pass/fail, topper) ║
║  9. Export class report to CSV                    ║
║ 10. Save & Exit                                   ║
╚══════════════════════════════════════════════════╝
```

The repository ships with 5 sample students already in `data/students.csv`
so you can try options 3–8 immediately without adding data first. Choose
option **10** at any time to persist changes back to the CSV file.

## Instructions for Testing

Run the automated unit test suite (17 tests covering grading logic, input
validation, and the `Student` model):
```bash
python3 -m unittest discover -s tests -v
```

Expected output ends with:
```
Ran 17 tests in 0.00Xs

OK
```

### Manual test checklist
1. Run `python3 main.py`, choose **4** → confirm the 5 seeded students appear.
2. Choose **1** → add a new student with a fresh roll number → confirm success message.
3. Choose **1** again with the *same* roll number → confirm a friendly
   `DuplicateStudentError` message (not a crash).
4. Choose **2** → enter marks for a student, try entering `abc` for marks →
   confirm a friendly `InvalidMarksError` message.
5. Choose **3** → view that student's marksheet → confirm total, percentage,
   grade and pass/fail are correct.
6. Choose **7** and **8** → confirm rank list and class statistics are sensible.
7. Choose **9** → confirm `data/class_report.csv` is created.
8. Choose **10** → confirm the program exits and `data/students.csv` reflects
   your changes.

## Regenerating the Design Diagrams

All diagrams in `docs/diagrams/` (architecture, workflow, use case, class,
sequence) are generated programmatically and reproducibly:
```bash
python3 docs/generate_diagrams.py
```

## Screenshots

See `docs/screenshots/` for sample runs (menu, marksheet output, and class
statistics).

## Design Decisions (summary)

- **Layered architecture** (CLI → Service → Utility → Model → Data Access) keeps
  each concern isolated and testable in isolation.
- **CSV over a database**: matches the syllabus scope (file I/O module) and
  keeps the project runnable anywhere with zero setup.
- **Custom exception hierarchy** (`SRMSError` and subclasses) turns every
  failure mode into a friendly, specific message instead of a raw traceback.
- **`array` module** used explicitly for class-wide percentage figures, as a
  deliberate, syllabus-aligned choice over a plain list for homogeneous
  numeric data.

## Future Enhancements

- Optional SQLite backend for larger datasets
- CSV import for bulk student onboarding
- PDF marksheet export per student
- Web-based front end (Flask) reusing the existing `src/` service layer unchanged

## License

Built for academic submission (VITyarthi coursework). Free to reference for
learning purposes.
