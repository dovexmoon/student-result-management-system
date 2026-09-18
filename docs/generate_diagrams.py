"""
generate_diagrams.py
---------------------
Generates all design diagrams (architecture, workflow, use case, class,
sequence) required by the project report, as clean PNG images, using only
matplotlib (no external tools needed -- keeps the whole pipeline
reproducible with `python docs/generate_diagrams.py`).
"""

import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
from matplotlib.lines import Line2D

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams")
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = "#1f3a5f"
BLUE = "#3a6ea5"
LIGHT = "#eaf1fb"
GREY = "#555555"
ACCENT = "#c0392b"


def box(ax, xy, w, h, text, fc=LIGHT, ec=NAVY, fontsize=10, fontweight="bold", textcolor="#111111"):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.6, edgecolor=ec, facecolor=fc, zorder=2,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
             fontsize=fontsize, fontweight=fontweight, color=textcolor, zorder=3, wrap=True)
    return patch


def arrow(ax, start, end, text=None, style="-|>", color=GREY, connectionstyle="arc3,rad=0.0", ls="-"):
    a = FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=14,
                         color=color, linewidth=1.4, connectionstyle=connectionstyle,
                         linestyle=ls, zorder=1)
    ax.add_patch(a)
    if text:
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(mx, my + 0.12, text, ha="center", va="bottom", fontsize=8.5, color=GREY, style="italic")


def new_fig(w=11, h=8, title=""):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=15, fontweight="bold", color=NAVY, pad=14)
    return fig, ax


# --------------------------------------------------------------------------- #
# 1. System Architecture Diagram
# --------------------------------------------------------------------------- #
def architecture_diagram():
    fig, ax = new_fig(11, 8, "System Architecture -- Student Result Management System")

    box(ax, (3.3, 6.6), 4.4, 0.9, "Presentation Layer\nmain.py (CLI Menu)", fc="#dceeff")
    box(ax, (1.0, 4.8), 4.2, 0.9, "Service Layer\nResultManager\n(Student & Marks CRUD)", fc=LIGHT)
    box(ax, (5.8, 4.8), 4.2, 0.9, "Service Layer\nReportService\n(Grading & Analytics)", fc=LIGHT)
    box(ax, (3.3, 3.0), 4.4, 0.9, "Utility Layer\nvalidators.py  |  grade_calculator.py", fc="#f5f0e6")
    box(ax, (3.3, 1.4), 4.4, 0.9, "Model Layer (OOP)\nStudent  |  Subject", fc="#e9f7ef")
    box(ax, (3.3, 0.0), 4.4, 0.9, "Data Access Layer\nFileHandler (csv module)", fc="#fdecea")
    box(ax, (3.3, -1.35), 4.4, 0.85, "Persistent Storage\ndata/students.csv", fc="#ffffff", ec=ACCENT)

    ax.set_ylim(-1.6, 8)

    arrow(ax, (5.5, 6.6), (3.1, 5.7), "calls")
    arrow(ax, (5.5, 6.6), (7.9, 5.7), "calls")
    arrow(ax, (3.1, 5.25), (5.5, 3.9), "validate()")
    arrow(ax, (7.9, 5.25), (5.5, 3.9), "grade_for_percentage()")
    arrow(ax, (5.5, 3.0), (5.5, 2.3), "uses")
    arrow(ax, (5.5, 1.4), (5.5, 0.9), "load / save")
    arrow(ax, (5.5, 0.0), (5.5, -0.5), "read / write")

    fig.savefig(os.path.join(OUT_DIR, "01_architecture.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# 2. Process Flow / Workflow Diagram
# --------------------------------------------------------------------------- #
def workflow_diagram():
    fig, ax = new_fig(6.5, 11, "Process Flow -- Main Program Workflow")

    steps = [
        ("Start Program", "#dceeff"),
        ("Load students.csv\ninto memory", LIGHT),
        ("Display Menu", LIGHT),
        ("Read user choice", LIGHT),
        ("Validate input\n(roll no / marks / name)", "#f5f0e6"),
    ]
    y = 10.2
    positions = []
    for text, fc in steps:
        box(ax, (1.5, y), 3.5, 0.8, text, fc=fc, fontsize=9.5)
        positions.append((3.25, y))
        y -= 1.15

    for i in range(len(positions) - 1):
        arrow(ax, (positions[i][0], positions[i][1]), (positions[i + 1][0], positions[i + 1][1] + 0.8))

    # Decision diamond
    dy = y + 0.4
    ax.add_patch(plt.Polygon([[3.25, dy + 0.55], [4.6, dy], [3.25, dy - 0.55], [1.9, dy]],
                              closed=True, facecolor="#fdecea", edgecolor=ACCENT, linewidth=1.6, zorder=2))
    ax.text(3.25, dy, "Valid?", ha="center", va="center", fontsize=9.5, fontweight="bold")
    arrow(ax, (3.25, y - 0.35 + 1.15), (3.25, dy + 0.55))

    # Yes branch
    box(ax, (1.5, dy - 2.3), 3.5, 0.8, "Execute action\n(Add / Update / Report / Export)", fc="#e9f7ef", fontsize=9)
    arrow(ax, (3.25, dy - 0.55), (3.25, dy - 1.5), "Yes")
    box(ax, (1.5, dy - 3.5), 3.5, 0.8, "Show result to user", fc="#e9f7ef", fontsize=9.5)
    arrow(ax, (3.25, dy - 2.3), (3.25, dy - 2.7))

    # No branch
    ax.text(4.9, dy + 0.15, "No", fontsize=9, color=ACCENT, fontweight="bold")
    arrow(ax, (4.6, dy), (5.9, dy), color=ACCENT)
    box(ax, (5.6, dy - 0.4), 2.0, 0.8, "Print friendly\nerror message", fc="#fdecea", ec=ACCENT, fontsize=8.5)
    arrow(ax, (6.6, dy - 0.4), (6.6, dy - 4.75), color=ACCENT, connectionstyle="arc3,rad=0.0")
    arrow(ax, (6.6, dy - 4.75), (5.0, dy - 4.75), color=ACCENT, connectionstyle="arc3,rad=0.0")

    # Loop back to menu / exit
    arrow(ax, (3.25, dy - 3.5), (3.25, dy - 4.3))
    box(ax, (1.5, dy - 5.1), 3.5, 0.8, "Exit chosen (10)?", fc="#f5f0e6", fontsize=9.5)

    arrow(ax, (0.4, dy - 4.7), (0.4, 8.9), connectionstyle="arc3,rad=0.0", color=BLUE)
    ax.text(0.15, dy - 1, "loop until Exit", rotation=90, fontsize=8, color=BLUE, style="italic")
    arrow(ax, (1.5, dy - 4.7), (0.4, dy - 4.7), color=BLUE)
    arrow(ax, (0.4, 8.9), (1.5, 8.9), color=BLUE)

    box(ax, (1.5, dy - 6.5), 3.5, 0.8, "Save to CSV & Exit", fc="#dceeff")
    ax.text(4.2, dy - 5.75, "Yes", fontsize=8.5, color=GREY, style="italic")
    arrow(ax, (3.25, dy - 5.1), (3.25, dy - 5.7))

    ax.set_ylim(dy - 6.8, 11.1)
    fig.savefig(os.path.join(OUT_DIR, "02_workflow.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# 3. Use Case Diagram
# --------------------------------------------------------------------------- #
def use_case_diagram():
    fig, ax = new_fig(11, 8.3, "Use Case Diagram -- SRMS")

    # Actor (stick figure) - Admin/Teacher
    ax.add_patch(Ellipse((1.3, 6.4), 0.5, 0.5, facecolor="#ffffff", edgecolor="black", linewidth=1.4, zorder=3))
    ax.add_line(Line2D([1.3, 1.3], [6.15, 5.2], color="black", linewidth=1.4, zorder=3))
    ax.add_line(Line2D([0.8, 1.8], [5.85, 5.85], color="black", linewidth=1.4, zorder=3))
    ax.add_line(Line2D([1.3, 0.85], [5.2, 4.6], color="black", linewidth=1.4, zorder=3))
    ax.add_line(Line2D([1.3, 1.75], [5.2, 4.6], color="black", linewidth=1.4, zorder=3))
    ax.text(1.3, 4.3, "Administrator /\nTeacher", ha="center", fontsize=9.5, fontweight="bold")

    system_box = FancyBboxPatch((3.0, 0.4), 7.6, 6.6, boxstyle="round,pad=0.02",
                                 linewidth=1.8, edgecolor=NAVY, facecolor="none", zorder=1)
    ax.add_patch(system_box)
    ax.text(6.8, 7.15, "Student Result Management System", ha="center", fontsize=11,
            fontweight="bold", color=NAVY)

    use_cases = [
        "Add Student", "Enter / Update Marks", "View Marksheet",
        "List All Students", "Search Student", "Remove Student",
        "View Class Rank List", "View Class Statistics", "Export Class Report",
    ]
    ys = [6.2, 5.4, 4.6, 3.8, 3.0, 2.2, 1.4, 0.6, -0.2]
    ys = [y + 0.4 for y in ys]
    for uc, y in zip(use_cases, ys):
        ell = Ellipse((6.9, y), 3.6, 0.62, facecolor=LIGHT, edgecolor=BLUE, linewidth=1.4, zorder=2)
        ax.add_patch(ell)
        ax.text(6.9, y, uc, ha="center", va="center", fontsize=9)
        arrow(ax, (1.85, 4.6), (5.1, y), color="#999999", style="-")

    ax.set_ylim(-0.3, 8.3)
    fig.savefig(os.path.join(OUT_DIR, "03_use_case.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# 4. Class Diagram
# --------------------------------------------------------------------------- #
def class_box(ax, xy, w, h, name, attrs, methods, fc=LIGHT):
    x, y = xy
    outer = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", linewidth=1.6,
                            edgecolor=NAVY, facecolor=fc, zorder=2)
    ax.add_patch(outer)
    title_h = 0.42
    ax.plot([x, x + w], [y + h - title_h, y + h - title_h], color=NAVY, linewidth=1.2, zorder=3)
    attrs_h = 0.28 * len(attrs) + 0.12
    ax.plot([x, x + w], [y + h - title_h - attrs_h, y + h - title_h - attrs_h], color=NAVY, linewidth=1.2, zorder=3)
    ax.text(x + w / 2, y + h - title_h / 2, name, ha="center", va="center", fontsize=10, fontweight="bold")
    ay = y + h - title_h - 0.2
    for a in attrs:
        ax.text(x + 0.12, ay, a, ha="left", va="center", fontsize=7.6, family="monospace")
        ay -= 0.28
    my_ = ay - 0.05
    for m in methods:
        ax.text(x + 0.12, my_, m, ha="left", va="center", fontsize=7.6, family="monospace")
        my_ -= 0.28
    return (x, y, w, h)


def class_diagram():
    fig, ax = new_fig(13, 9, "Class Diagram -- SRMS (core classes)")

    student = class_box(ax, (4.9, 5.6), 3.3, 2.6, "Student",
                         ["- roll_no: str", "- name: str", "- subjects: dict"],
                         ["+ set_marks()", "+ total_marks()", "+ percentage()",
                          "+ overall_grade()", "+ is_overall_pass()"], fc="#e9f7ef")

    subject = class_box(ax, (9.3, 6.3), 3.0, 1.9, "Subject",
                         ["- name: str", "- marks: float"],
                         ["+ is_pass()", "+ percentage()"], fc="#e9f7ef")

    rm = class_box(ax, (0.3, 3.0), 3.9, 2.3, "ResultManager",
                    ["- _students: list[Student]", "- _roll_index: set"],
                    ["+ add_student()", "+ get_student()", "+ update_marks()",
                     "+ remove_student()"], fc=LIGHT)

    rs = class_box(ax, (4.9, 2.6), 3.6, 2.5, "ReportService",
                    ["(stateless -- all\n  @staticmethod /\n  @classmethod)"],
                    ["+ marksheet()", "+ rank_list()", "+ class_average()",
                     "+ topper()", "+ subject_wise_average()"], fc=LIGHT)

    fh = class_box(ax, (9.3, 3.0), 3.2, 1.9, "FileHandler",
                    ["- path: str"],
                    ["+ load_students()", "+ save_students()"], fc="#fdecea")

    exc = class_box(ax, (0.3, 0.3), 3.9, 1.9, "SRMSError\n(base exception)",
                     [], ["DuplicateStudentError", "StudentNotFoundError",
                          "InvalidMarksError", "...more..."], fc="#f5f0e6")

    # relationships
    arrow(ax, (6.55, 6.3), (6.55, 5.6+2.6), "1", color=GREY, style="-")
    ax.text(7.0, 8.35, "composed of  1..*", fontsize=8, style="italic")
    arrow(ax, (9.3, 7.1), (8.2, 7.1), color=GREY, style="-")

    arrow(ax, (4.2, 4.2), (4.9, 6.5), "manages 0..*", color=GREY, style="-")
    arrow(ax, (4.2, 3.6), (4.9, 3.6), "reads via", color=GREY, style="-")
    arrow(ax, (4.2, 3.9), (9.3, 3.9), color=GREY, style="-")
    arrow(ax, (8.5, 3.9), (6.55, 5.6), "uses", color=GREY, style="-")
    arrow(ax, (2.2, 3.0), (2.2, 2.2), "raises", color=ACCENT, style="-", ls="--")

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    fig.savefig(os.path.join(OUT_DIR, "04_class_diagram.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# 5. Sequence Diagram ("Enter marks" flow)
# --------------------------------------------------------------------------- #
def sequence_diagram():
    fig, ax = new_fig(12, 7.5, "Sequence Diagram -- \"Enter / Update Marks\" Flow")

    actors = [("User", 0.8), ("CLI\n(main.py)", 3.4), ("Validators", 6.0),
              ("ResultManager", 8.6), ("Student", 11.0)]
    top_y = 6.9
    for name, x in actors:
        box(ax, (x - 0.9, top_y), 1.8, 0.6, name, fc="#dceeff", fontsize=8.5)
        ax.plot([x, x], [top_y, 0.5], color="#999999", linewidth=1.1, linestyle="--", zorder=1)

    def msg(x1, x2, y, text, dashed=False):
        arrow(ax, (x1, y), (x2, y), text=None,
              style="-|>", color="black", ls="--" if dashed else "-")
        ax.text((x1 + x2) / 2, y + 0.12, text, ha="center", fontsize=7.8)

    y = 6.3
    msg(0.8, 3.4, y, "choose option 2, enter roll no & marks"); y -= 0.55
    msg(3.4, 8.6, y, "get_student(roll_no)"); y -= 0.55
    msg(8.6, 3.4, y, "return student", dashed=True); y -= 0.55
    msg(3.4, 6.0, y, "validate_marks(raw_input)"); y -= 0.55
    msg(6.0, 3.4, y, "return float marks", dashed=True); y -= 0.55
    msg(3.4, 8.6, y, "update_marks(roll_no, subject, marks)"); y -= 0.55
    msg(8.6, 11.0, y, "set_marks(subject, marks)"); y -= 0.55
    msg(11.0, 8.6, y, "OK", dashed=True); y -= 0.55
    msg(8.6, 3.4, y, "return updated student", dashed=True); y -= 0.55
    msg(3.4, 0.8, y, "print '\u2714 Marks updated'"); y -= 0.4

    ax.set_ylim(y - 0.3, 7.7)
    fig.savefig(os.path.join(OUT_DIR, "05_sequence_diagram.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    architecture_diagram()
    workflow_diagram()
    use_case_diagram()
    class_diagram()
    sequence_diagram()
    print("All diagrams generated in:", OUT_DIR)
