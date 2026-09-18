"""
exceptions.py
-------------
Custom exception hierarchy for SRMS.

Defining our own exceptions (rather than letting raw ValueError / KeyError
propagate to the user) is part of the "Error handling strategy" non-functional
requirement, and demonstrates class INHERITANCE (module: Object Oriented
Programming in Python) -- every custom exception below derives from a single
base class, SRMSError, so calling code can catch them individually or as a
group.
"""


class SRMSError(Exception):
    """Base class for every error raised by this application."""
    pass


class DuplicateStudentError(SRMSError):
    """Raised when trying to add a student whose roll number already exists."""
    def __init__(self, roll_no):
        super().__init__(f"A student with roll number '{roll_no}' already exists.")
        self.roll_no = roll_no


class StudentNotFoundError(SRMSError):
    """Raised when a lookup / update / delete targets a roll number that does not exist."""
    def __init__(self, roll_no):
        super().__init__(f"No student found with roll number '{roll_no}'.")
        self.roll_no = roll_no


class InvalidRollNumberError(SRMSError):
    """Raised when a supplied roll number fails validation."""
    pass


class InvalidNameError(SRMSError):
    """Raised when a supplied student name fails validation."""
    pass


class InvalidMarksError(SRMSError):
    """Raised when supplied marks are non-numeric or out of the allowed range."""
    pass


class InvalidSubjectError(SRMSError):
    """Raised when a subject name is not part of the configured subject list."""
    pass


class EmptyDatasetError(SRMSError):
    """Raised when an operation (e.g. topper, average) is attempted with no students loaded."""
    pass
