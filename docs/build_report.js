const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ImageRun, AlignmentType, PageBreak, ShadingType, BorderStyle,
  Header, Footer, PageNumber, NumberFormat, LevelFormat, convertInchesToTwip
} = require("docx");
const fs = require("fs");

const NAVY = "1f3a5f";
const GREY = "555555";

function h1(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 320, after: 160 } });
}
function h2(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 } });
}
function p(text, opts = {}) {
  return new Paragraph({ children: [new TextRun({ text, ...opts })], spacing: { after: 140 } });
}
function bullet(text) {
  return new Paragraph({ text, bullet: { level: 0 }, spacing: { after: 60 } });
}
function image(path, widthPx, heightPx, maxWidthIn = 6.3) {
  const ratio = heightPx / widthPx;
  const w = maxWidthIn;
  const hIn = w * ratio;
  return new Paragraph({
    children: [new ImageRun({ data: fs.readFileSync(path), transformation: { width: w * 96, height: hIn * 96 }, type: "png" })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
  });
}
function caption(text) {
  return new Paragraph({
    children: [new TextRun({ text, italics: true, size: 18, color: "666666" })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 280 },
  });
}

function simpleTable(headers, rows) {
  const mkCell = (text, bold = false, shade = false) => new TableCell({
    width: { size: Math.floor(9350 / headers.length), type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, fill: "E9EFF7" } : undefined,
    children: [new Paragraph({ children: [new TextRun({ text: String(text), bold })] })],
  });
  const headerRow = new TableRow({ children: headers.map(hd => mkCell(hd, true, true)) });
  const dataRows = rows.map(r => new TableRow({ children: r.map(c => mkCell(c)) }));
  return new Table({
    width: { size: 9350, type: WidthType.DXA },
    columnWidths: headers.map(() => Math.floor(9350 / headers.length)),
    rows: [headerRow, ...dataRows],
  });
}

const diagrams = "docs/diagrams/";
const shots = "docs/screenshots/";

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullet-list",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT }],
    }],
  },
  sections: [
    // ---------------- COVER PAGE ----------------
    {
      properties: { page: { size: { width: 12240, height: 15840 } } },
      children: [
        new Paragraph({ text: "", spacing: { before: 2200 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "VITyarthi -- Build Your Own Project", size: 28, color: GREY })],
        }),
        new Paragraph({ text: "", spacing: { before: 200 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Student Result Management System", bold: true, size: 56, color: NAVY })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 200 },
          children: [new TextRun({ text: "A CLI-Based Python Application for Managing Student Marks, Grading, and Class Analytics", italics: true, size: 26 })],
        }),
        new Paragraph({ text: "", spacing: { before: 1200 } }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Course Project Report", size: 24, bold: true })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 100 },
          children: [new TextRun({ text: "Subject: Python Programming (Modules 1\u201312)", size: 22 })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 400 },
          children: [new TextRun({ text: "Submitted as part of the flipped-course evaluation", size: 20, color: "777777" })],
        }),
        new Paragraph({ children: [new PageBreak()] }),
      ],
    },
    // ---------------- MAIN REPORT ----------------
    {
      properties: {
        page: { size: { width: 12240, height: 15840 }, margin: { top: 1000, bottom: 1000, left: 1200, right: 1200 } },
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.RIGHT,
            children: [new TextRun({ text: "Student Result Management System", size: 16, color: "999999" })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "999999" })],
          })],
        }),
      },
      children: [
        // 1. Introduction
        h1("1. Introduction"),
        p("Tracking student marks manually or in scattered spreadsheets is time-consuming and error-prone, and makes it difficult to quickly answer class-level questions such as \u201cwho is the topper?\u201d or \u201cwhat is the pass percentage in a subject?\u201d. The Student Result Management System (SRMS) is a command-line Python application, built entirely with the Python standard library, that lets a teacher or administrator maintain a roster of students, record subject-wise marks, automatically compute grades according to a configurable policy, and generate class-wide analytics -- all without needing a database server, a GUI framework, or an internet connection."),
        p("The project was designed to apply, in a single cohesive codebase, every concept taught across the course syllabus: variables and operators, input/output, operator precedence, type conversion, the core data structures (list, tuple, dict, set), control flow, functions, modules & packages, array-based data storage, and full object-oriented programming."),

        // 2. Problem Statement
        h1("2. Problem Statement"),
        p("Design and implement a fully offline, command-line result management system that allows a teacher to: (a) maintain a roster of students; (b) record and update marks for each student across a fixed set of subjects, with robust input validation; (c) automatically compute each student's total, percentage, and letter grade using a transparent and consistent policy; and (d) generate class-wide insights -- a rank list, the topper, subject-wise averages, and a pass/fail summary -- and export them for further use. The solution must be executable purely from the terminal, persist data between runs, and be organised into clean, testable, modular code."),

        // 3. Functional Requirements
        h1("3. Functional Requirements"),
        p("The system is organised into three major functional modules, each with a clear input/output structure and a logical workflow (see Section 7, Use Case Diagram, and Section 4, Design & Documentation):"),
        h2("3.1 Student & Marks Management"),
        bullet("Add a new student (unique roll number + name), with duplicate detection."),
        bullet("Enter or update a student's marks, subject by subject, with input validation."),
        bullet("Search students by (partial, case-insensitive) name."),
        bullet("List all students with their current percentage and grade."),
        bullet("Remove a student from the roster, with an explicit confirmation step."),
        h2("3.2 Result Processing & Grading"),
        bullet("Compute total marks and percentage from a student's per-subject marks."),
        bullet("Map percentage to a letter grade (A+ through F) via a configurable grade table."),
        bullet("Determine per-subject pass/fail and overall pass/fail (aggregate threshold AND no individual subject failures)."),
        bullet("Generate a formatted, human-readable marksheet for any student."),
        h2("3.3 Reporting & Analytics"),
        bullet("Rank the entire class by percentage (with roll-number tie-breaking)."),
        bullet("Identify the class topper and compute the class average."),
        bullet("Compute subject-wise class averages."),
        bullet("Compute a pass/fail summary for the class."),
        bullet("Export a full class report (rank, roll no, name, total, percentage, grade, result) to CSV."),

        // 4. Non-functional requirements
        h1("4. Non-Functional Requirements"),
        simpleTable(
          ["Requirement", "How it is addressed"],
          [
            ["Performance", "All operations are O(n) or better over the in-memory student list (a handful of students to a few thousand); the roster is loaded once at startup and only re-read/written on explicit save, avoiding repeated disk I/O."],
            ["Reliability", "Every user-facing action is wrapped in a single top-level exception handler in main.py that catches the entire SRMSError hierarchy, so malformed input or a missing record never crashes the program."],
            ["Usability", "A numbered menu, clear prompts, aligned tabular output, and explicit confirmation before destructive actions (student removal) keep the CLI approachable for a non-technical user."],
            ["Maintainability", "A layered architecture (CLI -> Service -> Utility -> Model -> Data Access) with single-responsibility modules means a change to, e.g., the CSV format only touches file_handler.py."],
            ["Error-Handling Strategy", "A custom exception hierarchy (SRMSError and 7 subclasses) gives every failure mode a specific, catchable type and a friendly message, instead of raw Python tracebacks."],
            ["Resource Efficiency", "The `array` module is used for class-wide percentage figures (a homogeneous numeric dataset), which is more memory-compact than a general-purpose list of Python floats."],
          ]
        ),
        new Paragraph({ text: "", spacing: { after: 200 } }),

        // 5. System Architecture
        h1("5. System Architecture"),
        p("SRMS follows a layered architecture. The CLI (main.py) is the only layer the user interacts with; it delegates all business logic to the Service layer (ResultManager for CRUD, ReportService for grading/analytics), which in turn relies on the Utility layer for validation and grade computation, the Model layer (Student, Subject) for encapsulated OOP behaviour, and the Data Access layer (FileHandler) for all CSV I/O. Each layer depends only on the layer(s) directly below it, which keeps the codebase easy to test, extend, and reason about."),
        image(diagrams + "01_architecture.png", 1483, 1141),
        caption("Figure 1: System Architecture Diagram"),

        // 6. Process flow
        h1("6. Process Flow / Workflow"),
        p("The application runs a continuous menu loop: load data, display the menu, read and validate the user's choice and input, execute the corresponding action, display the result, and repeat until the user chooses to save and exit. Invalid input at any point is caught and reported without disrupting the loop."),
        image(diagrams + "02_workflow.png", 986, 1533, 4.6),
        caption("Figure 2: Process Flow / Workflow Diagram"),

        // 7. Use case diagram
        h1("7. Use Case Diagram"),
        p("A single actor -- the Administrator/Teacher -- interacts with all nine use cases exposed by the system, corresponding one-to-one with the main menu options."),
        image(diagrams + "03_use_case.png", 1483, 1180),
        caption("Figure 3: Use Case Diagram"),

        // 8. Class diagram
        h1("8. Class / Component Diagram"),
        p("Student is the central OOP class, composed of Subject objects and providing derived properties (total, percentage, grade, pass/fail). ResultManager owns the in-memory roster and CRUD operations; ReportService is a stateless collection of grading/analytics operations; FileHandler isolates all CSV I/O; and every business-rule failure raises a subclass of the common SRMSError base exception."),
        image(diagrams + "04_class_diagram.png", 1746, 1272),
        caption("Figure 4: Class Diagram"),

        // 9. Sequence diagram
        h1("9. Sequence Diagram"),
        p("The sequence below traces the \u201cEnter / Update Marks\u201d use case end-to-end: the CLI first confirms the student exists, validates the raw marks input via the Utility layer, then asks ResultManager to update the Student object's marks before confirming success back to the user."),
        image(diagrams + "05_sequence_diagram.png", 1615, 1075),
        caption("Figure 5: Sequence Diagram -- Enter / Update Marks"),

        // 10. Data / storage design
        h1("10. Data / Storage Design"),
        p("Data is persisted as a flat CSV file (data/students.csv) with one row per student. This was chosen deliberately over a database because (a) the course syllabus's scope is core Python rather than database technology, and (b) it keeps the project runnable anywhere with zero setup. The schema is:"),
        simpleTable(
          ["Column", "Type", "Description"],
          [
            ["roll_no", "string (unique)", "Primary key -- alphanumeric student identifier"],
            ["name", "string", "Student's full name"],
            ["Python", "float (0-100)", "Marks scored in Python"],
            ["Mathematics", "float (0-100)", "Marks scored in Mathematics"],
            ["Data Structures", "float (0-100)", "Marks scored in Data Structures"],
            ["English", "float (0-100)", "Marks scored in English"],
            ["Computer Networks", "float (0-100)", "Marks scored in Computer Networks"],
          ]
        ),
        new Paragraph({ text: "", spacing: { after: 200 } }),

        // 11. Design decisions
        h1("11. Design Decisions & Rationale"),
        bullet("Layered architecture: chosen so that grading logic, validation, persistence and presentation can each change independently -- e.g. swapping CSV for SQLite would only require editing FileHandler."),
        bullet("Custom exception hierarchy over generic exceptions: gives calling code (main.py) a single catch-all (SRMSError) while still letting each failure carry a specific, descriptive type."),
        bullet("Dict-of-Subject-objects on Student (rather than a flat list of marks): gives O(1) subject lookup/update and keeps each mark paired with pass/fail behaviour via the Subject class."),
        bullet("Set for roll-number indexing in ResultManager: turns duplicate-detection from an O(n) scan into an O(1) lookup."),
        bullet("array module for class-wide percentages: a deliberate, syllabus-aligned use of Python's built-in array data structure for homogeneous numeric data, as distinct from a general-purpose list."),
        bullet("Class/static methods on ReportService: the service is stateless by design (it only derives facts from the students handed to it), so its methods don't need an instance."),

        // 12. Implementation details
        h1("12. Implementation Details"),
        p("The codebase spans 13 Python files organised into a proper package structure (src/, src/models/, src/services/, src/utils/, tests/), exceeding the minimum of 5\u201310 meaningful modules. Key implementation points:"),
        bullet("Type conversion: raw CSV values and raw console input (always strings) are explicitly converted to float/int in validators.py and Student.from_csv_row(), with ValueError caught and re-raised as InvalidMarksError."),
        bullet("Control flow: the CLI's main loop, the grade-boundary lookup in grade_calculator.py, and every validation function rely on if/elif/for/while constructs taught in Modules 7\u20138."),
        bullet("Functions & modules/packages: business logic is decomposed into small, single-purpose functions and organised into importable packages (src.models, src.services, src.utils), directly applying Modules 9\u201310."),
        bullet("Data structures: list (roster), dict (a student's subjects), tuple (immutable SUBJECTS and GRADE_TABLE), set (roll-number index), and array (class percentages) are each used where they are the *appropriate* structure, not interchangeably."),
        bullet("OOP: Student and Subject are full classes with encapsulated state and behaviour; Student defines __str__, __repr__, __eq__ and __hash__; classmethod from_csv_row() acts as an alternate constructor; the exception hierarchy demonstrates inheritance."),
        bullet("Error handling: a single try/except SRMSError block in the CLI's main loop converts every business-rule violation into a friendly, non-crashing message."),

        // 13. Screenshots
        h1("13. Screenshots / Results"),
        p("Sample runs of the application, captured directly from the terminal:"),
        image(shots + "01_menu_and_list.png", 1270, 1259, 5.6),
        caption("Figure 6: Main menu and student list"),
        image(shots + "02_marksheet.png", 1270, 1408, 5.6),
        caption("Figure 7: Individual student marksheet"),
        image(shots + "03_statistics.png", 1270, 1308, 5.6),
        caption("Figure 8: Class-wide statistics"),

        // 14. Testing approach
        h1("14. Testing Approach"),
        p("The project includes an automated unit test suite (tests/test_grade_calculator.py, 17 tests) built with Python's unittest framework, covering:"),
        bullet("Grade-boundary computation at every threshold edge (e.g. 89.99% -> 'A', 90% -> 'A+')."),
        bullet("Validator functions: valid and invalid roll numbers, names, marks (non-numeric, out of range), and subjects."),
        bullet("The Student model: total/percentage arithmetic, overall grade, pass/fail with and without a failed subject, and equality-by-roll-number."),
        p("In addition, the full CLI was manually exercised end-to-end (adding a student, entering marks, viewing a marksheet, listing, ranking, computing statistics, exporting, and saving) and specific error paths were verified interactively -- duplicate roll numbers, non-existent roll numbers, and non-numeric marks input all produce a friendly error message rather than a crash. Run the suite with:"),
        new Paragraph({
          children: [new TextRun({ text: "python3 -m unittest discover -s tests -v", font: "Consolas", size: 20 })],
          shading: { type: ShadingType.CLEAR, fill: "F0F0F0" },
          spacing: { after: 200 },
        }),

        // 15. Challenges faced
        h1("15. Challenges Faced"),
        bullet("Deciding the overall pass/fail rule: settled on requiring both a minimum aggregate percentage AND no individual subject failures, matching how most real academic systems compute results, rather than a single aggregate-only check."),
        bullet("Keeping the CSV read/write layer perfectly in sync with the Student model's fields, solved by defining CSV_FIELDNAMES once in config.py and having both the reader (Student.from_csv_row) and writer (Student.to_csv_row) depend on the same SUBJECTS tuple."),
        bullet("Producing clear, exam-ready design diagrams without relying on an external diagramming tool or the internet -- solved by writing a small, reusable matplotlib-based diagram generator (docs/generate_diagrams.py) so every diagram is reproducible from source."),

        // 16. Learnings
        h1("16. Learnings & Key Takeaways"),
        bullet("How to structure a non-trivial Python project into clean, single-responsibility packages rather than one large script."),
        bullet("Why choosing the right data structure (set for membership checks, array for homogeneous numeric data, tuple for fixed configuration) matters even in a small project."),
        bullet("How a custom exception hierarchy simplifies error handling at the call site while preserving specific, debuggable failure information."),
        bullet("The value of writing automated tests alongside the implementation, which caught an early off-by-one error in the grade-boundary logic."),

        // 17. Future enhancements
        h1("17. Future Enhancements"),
        bullet("Swap the CSV backend for SQLite behind the same FileHandler interface to support much larger datasets."),
        bullet("Add bulk CSV import for onboarding an entire class at once."),
        bullet("Generate a per-student PDF marksheet (reusing the pdf-generation approach used for this report)."),
        bullet("Wrap the existing service layer in a small Flask web front-end without changing any business logic."),

        // 18. References
        h1("18. References"),
        bullet("Python Software Foundation -- Python 3 Standard Library Documentation: https://docs.python.org/3/library/"),
        bullet("Python Software Foundation -- csv module documentation: https://docs.python.org/3/library/csv.html"),
        bullet("Python Software Foundation -- array module documentation: https://docs.python.org/3/library/array.html"),
        bullet("Python Software Foundation -- unittest module documentation: https://docs.python.org/3/library/unittest.html"),
        bullet("Course modules 1\u201312 (Introduction to Python through Object Oriented Programming in Python), as supplied on the course platform."),
      ],
    },
  ],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("docs/report.docx", buf);
  console.log("Report written to docs/report.docx");
});
