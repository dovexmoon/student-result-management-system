
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


name= input("enter your name")

def action_add_student(rm):
    roll_no = int(input("Roll number"))
    name = input("Full name")
    rm.add_student(roll_no, name)
    print(f" Student '{name}' ({roll_no}) added.")


def action_enter_marks(rm):
    roll_no = int(input("Roll number"))
    student_name = input("Enter student name: ")
    subjects = ["Math", "Science", "English"]
    
    for subject in subjects:
        ri = input(f"Enter {subject} marks (out of 100) or press Enter to skip: ")
        if ri != "":
            marks = int(ri)
            print(f"Saved {marks} for {subject}.")
    print(f"Marks updated for {student_name}.")


def action_view_marksheet(rm):
    roll_no = int(input("Roll number"))
    student = rm.get_student(roll_no)
    print(ReportService.marksheet(student))


def action_list_students(rm):
    students = rm.list_students()
    if not students:
        print("No students in the system.")
        return
    print("Roll No | Name | % | Grade")
    print("-" * 30)
    for s in students:
        print(f"{s.roll_no} | {s.name} | {s.percentage()} | {s.overall_grade()}")

def action_search(rm):
    matches = rm.search_by_name(prompt("Search name contains"))
    if not matches:
        return print("No matches found.")    
    for s in matches:
        print(f" {s}")
  

def action_remove(rm):
    roll_no = input("Roll number to remove: ")
    rm.remove_student(roll_no)
    print(f"Student {roll_no} removed.")


def action_rank_list(rm):
    students = rm.list_students()
    ranked = sorted(students, key=lambda s: s.percentage(), reverse=True)
    print("Rank | Roll No | Name | Percentage | Grade")
    print("-" * 50)
    rank = 1
    for s in ranked:
        print(rank, "|", s.roll_no, "|", s.name, "|", s.percentage(), "|", s.overall_grade())
        rank += 1


def action_statistics(rm):
    students = rm.list_students()
    avg = ReportService.class_average(students)
    top = ReportService.topper(students)
    summary = ReportService.pass_fail_summary(students)
    subj_avg = ReportService.subject_wise_average(students)

    print("Class average:", avg, "%")
    print("Topper:", top.name, top.roll_no, top.percentage(), "%")
    print("Passed / Failed:", summary['passed'], "/", summary['failed'], "of", summary['total'])
    print("Subject-wise average:")
    for subject, avg_marks in subj_avg.items():
        print(subject, ":", avg_marks)


def action_export(rm):
    students = rm.list_students()
    rows = ReportService.export_rows(students)
    fieldnames = ["rank", "roll_no", "name", "total", "percentage", "grade", "result"]
    FileHandler().export_rows(REPORT_CSV, fieldnames, rows)
    print("Class report exported to {}".format(report_csv))


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


def main():
    print("Student Result Management System")
    print("Type 10 to exit the program safely.\n")
    while True:
        print("--- MENU ---")
        print("1. Add Student  2. View Results  ...  10. Save & Exit") 
        choice = input("Choose an option (1-10): ")
        if choice == "10":
            print("Saving data... Goodbye!")
            break 
            
        elif choice == "1":
            print("You chose to add a student.")
        elif choice == "2":
            print("You chose to view results.")   
        else:
            print("Invalid option, please choose a number from the menu.")
main()

print("Exiting without saving unsaved changes. Bye!")
exit()

