# Student's Result Management System (SRMS)

A command line application, written in pure Python, that lets a teacher/administrator
manage a class record, record subjectwise marks, compute grades, and generate
classwise analytics and reports , built as the course project for **VITyarthi**
---

## Overview

Managing student results by hand or in a spreadsheet is not errorfree and hard to analyse. SRMS gives a teacher a single, reliable, offline tool to:

- maintain a result of students,
- enter/update subjectwise marks with input validation,
- automatically calculate totals, percentages and letter grades,
- generates a formatted marksheet for any student,
- rank the whole class and concludes pass/fail and subjectwise statistics,
  

## Features

| # | Functional Module | What it does |
|---|---|---|
| 1 | **Student & Marks Management** | Add, update, search, list and remove students; enter/update marks per subject, with full input validation. |
| 2 | **Result Processing & Grading** | Calculates total marks, percentage, and letter grade (A-F) per student, and for every subject pass/fail status, using  the range of marks for grade. |
| 3 | **Reporting & Analytics** | Class rank list, topper, class average, subjectwise averages, pass/fail summary. |

## Technologies / Tools Used

- **Language:** Python 3.9+ (standard library)
- **Core modules used:** `csv`,`array` , `unittest` , `os`, `sys`
- **Concepts applied:** variables & operators, type conversion, precedence, list, dict, tuple, set, array, control flow, functions, packages/modules, array data structures, and full Object Oriented Programming (classes, encapsulation, inheritance via custom exceptions, class/static methods, dunder methods)
- **Version control:** Git / GitHub

## Project Structure

```
student result management system/
├── main.py                        # Command line interface entry point 
├── requirements.txt                # documents "stdlib only"
├── README.md
├── statement.md                    # problem statement, scope, target users
├── data/
│   └── students.csv                # sample data (5 students)
├── src/
│   ├── config.py                   # constants: subjects, grade table, file paths
│   ├── exceptions.py                
│   ├── models/
│   │   ├── student.py               # Student class (OOP)
│   │   └── subject.py               # Subject class (OOP)
│   ├── services/
│   │   ├── file_handler.py          # CSV read/write 
│   │   ├── result_manager.py        # Functional Module 1: Create,Read,Update and Delete
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



## How to Run

From the project root:
```bash
python3 main.py
```

You'll see a menu driven interface:
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
so you can try options 3 to 8 immediately without adding data first. Choose
option **10** at any time to continue changes back to the CSV file.


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



## Screenshots

See `docs/screenshots/` for sample runs (menu, marksheet output, and class
statistics).


## License

Built for academic submission-VITyarthi
