#!/usr/bin/env python3
"""
main.py
-------
Entry point for the Student Result Management System (SRMS).

A menu-driven command-line interface (module: Control Flow Statements in
Python) that wires together every layer of the application:

    models/      -> Student, Subject                (OOP)
    utils/       -> validators, grade_calculator     (functions)
    services/    -> ResultManager, ReportService, FileHandler  (business logic + I/O)

Run with:  python main.py
"""

import sys

from src.config import SUBJECTS, REPORT_CSV
from src.exceptions import SRMSError
from src.services.result_manager import ResultManager
from src.services.report_service import ReportService
from src.services.file_handler import FileHandler
from src.utils.validators import (
    validate_roll_no,
    validate_name,
    validate_subject,
    validate_marks,
)

MENU = """
╔══════════════════════════════════════════════════╗
║   STUDENT RESULT MANAGEMENT SYSTEM                ║
╠══════════════════════════════════════════════════╣
║  1. Add new student                               ║
║  2. Enter / update marks for a student            ║
║  3. View a student's marksheet                    ║
║  4. List all students                             ║
║  5. Search students by name                       ║
║  6. Remove a student                               ║
║  7. Class rank list                               ║
║  8. Class statistics (average, pass/fail, topper) ║
║  9. Export class report to CSV                    ║
║ 10. Save & Exit                                   ║
╚══════════════════════════════════════════════════╝
"""


def prompt(label: str) -> str:
    return input(f"{label}: ").strip()


def action_add_student(rm: ResultManager) -> None:
    roll_no = validate_roll_no(prompt("Roll number"))
    name = validate_name(prompt("Full name"))
    rm.add_student(roll_no, name)
    print(f"✔ Student '{name}' ({roll_no}) added.")


def action_enter_marks(rm: ResultManager) -> None:
    roll_no = validate_roll_no(prompt("Roll number"))
    student = rm.get_student(roll_no)  # raises StudentNotFoundError early if invalid
    print(f"Entering marks for {student.name}. Subjects: {', '.join(SUBJECTS)}")
    for subject_name in SUBJECTS:
        raw = prompt(f"  {subject_name} marks (out of 100)")
        if raw == "":
            continue  # allow skipping a subject, keeps previous value
        marks = validate_marks(raw)
        rm.update_marks(roll_no, subject_name, marks)
    print(f"✔ Marks updated for {student.name}.")


def action_view_marksheet(rm: ResultManager) -> None:
    roll_no = validate_roll_no(prompt("Roll number"))
    student = rm.get_student(roll_no)
    print(ReportService.marksheet(student))


def action_list_students(rm: ResultManager) -> None:
    students = rm.list_students()
    if not students:
        print("No students in the system yet.")
        return
    print(f"\n{'Roll No':<10}{'Name':<22}{'%':>8}{'Grade':>8}")
    print("-" * 48)
    for s in students:
        print(f"{s.roll_no:<10}{s.name:<22}{s.percentage():>8.2f}{s.overall_grade():>8}")


def action_search(rm: ResultManager) -> None:
    keyword = prompt("Search name contains")
    matches = rm.search_by_name(keyword)
    if not matches:
        print("No matches found.")
        return
    for s in matches:
        print(f"  {s}")


def action_remove(rm: ResultManager) -> None:
    roll_no = validate_roll_no(prompt("Roll number to remove"))
    confirm = prompt(f"Type YES to confirm deleting {roll_no}")
    if confirm != "YES":
        print("Cancelled.")
        return
    rm.remove_student(roll_no)
    print(f"✔ Student {roll_no} removed.")


def action_rank_list(rm: ResultManager) -> None:
    ranked = ReportService.rank_list(rm.list_students())
    print(f"\n{'Rank':<6}{'Roll No':<10}{'Name':<22}{'%':>8}{'Grade':>8}")
    print("-" * 54)
    for i, s in enumerate(ranked, start=1):
        print(f"{i:<6}{s.roll_no:<10}{s.name:<22}{s.percentage():>8.2f}{s.overall_grade():>8}")


def action_statistics(rm: ResultManager) -> None:
    students = rm.list_students()
    avg = ReportService.class_average(students)
    top = ReportService.topper(students)
    summary = ReportService.pass_fail_summary(students)
    subj_avg = ReportService.subject_wise_average(students)

    print(f"\nClass average       : {avg}%")
    print(f"Topper              : {top.name} ({top.roll_no}) -- {top.percentage()}%")
    print(f"Passed / Failed     : {summary['passed']} / {summary['failed']} "
          f"(of {summary['total']})")
    print("Subject-wise average:")
    for subject, avg_marks in subj_avg.items():
        print(f"  {subject:<18}: {avg_marks}")


def action_export(rm: ResultManager) -> None:
    students = rm.list_students()
    rows = ReportService.export_rows(students)
    fieldnames = ["rank", "roll_no", "name", "total", "percentage", "grade", "result"]
    FileHandler().export_rows(REPORT_CSV, fieldnames, rows)
    print(f"✔ Class report exported to {REPORT_CSV}")


ACTIONS = {
    "1": action_add_student,
    "2": action_enter_marks,
    "3": action_view_marksheet,
    "4": action_list_students,
    "5": action_search,
    "6": action_remove,
    "7": action_rank_list,
    "8": action_statistics,
    "9": action_export,
}


def main() -> None:
    rm = ResultManager()
    print("Student Result Management System -- type Ctrl+C at any time to abort safely.")

    while True:
        print(MENU)
        choice = prompt("Choose an option (1-10)")

        if choice == "10":
            rm.save()
            print("Data saved. Goodbye!")
            sys.exit(0)

        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option, please choose a number from the menu.")
            continue

        try:
            action(rm)
        except SRMSError as exc:
            # Every custom exception in the system inherits from SRMSError,
            # so this single handler catches them all with a friendly message
            # instead of a raw traceback -- the required error-handling strategy.
            print(f"✖ Error: {exc}")
        except KeyboardInterrupt:
            print("\nInterrupted. Data not saved for this action -- returning to menu.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting without saving unsaved changes. Bye!")
        sys.exit(0)
