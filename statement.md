# Problem Statement

## Problem Statement

Manually tracking student marks — on paper or in ad-hoc spreadsheets — is
error-prone, hard to validate, and makes it tedious to answer simple
questions like "who is the class topper?" or "what is the pass rate in
Mathematics?". Teachers need a lightweight, dependable tool that captures
each student's subject-wise marks, automatically computes grades using a
consistent policy, and produces class-level insights on demand — without
requiring a database server, an internet connection, or any paid software.

## Scope of the Project

The **Student Result Management System (SRMS)** is a command-line Python
application that:

- maintains a roster of students and their marks across a fixed set of
  subjects (Python, Mathematics, Data Structures, English, Computer
  Networks),
- validates every piece of user input (roll numbers, names, marks) before
  it is stored,
- computes, for each student: total marks, percentage, letter grade
  (A+ through F), per-subject pass/fail, and overall pass/fail,
- computes, for the whole class: a rank list, the topper, the class
  average, subject-wise averages, and a pass/fail summary,
- persists all data to a CSV file so it survives between runs,
- exports a class-wide report to a separate CSV file for sharing/printing.

**Out of scope** (deliberately, to keep the project focused and fully
achievable within the syllabus's taught concepts): a graphical user
interface, multi-user authentication, a networked/web deployment, and a
relational database backend. These are listed under *Future Enhancements*
in the README as natural next steps.

## Target Users

- **Teachers / course instructors** who need a fast way to record marks and
  generate a class's results at the end of a term.
- **Academic administrators** who need summary statistics (pass rate,
  average, topper) for reporting purposes.
- **Students**, indirectly, as the beneficiaries of an accurately and
  consistently graded marksheet.

## High-Level Features

1. **Student & Marks Management** — add, search, list, update and remove
   students; enter or update a student's marks per subject, with full
   validation and duplicate/roll-number-not-found protection.
2. **Result Processing & Grading** — automatic computation of total marks,
   percentage, and letter grade per student using a configurable grade
   table; per-subject and overall pass/fail determination.
3. **Reporting & Analytics** — class rank list, topper identification,
   class-wide average, subject-wise averages, pass/fail summary, and
   one-click export of the full class report to CSV.

See `README.md` for setup/run instructions and the full project report
(submitted separately as PDF) for architecture, design diagrams, and
implementation details.
