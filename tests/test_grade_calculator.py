import unittest

from src.utils.grade_calculator import grade_for_percentage, letter_to_grade_point
from src.utils.validators import (
    validate_roll_no,
    validate_name,
    validate_marks,
    validate_subject,
)
from src.exceptions import InvalidRollNumberError, InvalidNameError, InvalidMarksError, InvalidSubjectError
from src.models.student import Student


class TestGradeCalculator(unittest.TestCase):
    def test_grade_boundaries(self):
        self.assertEqual(grade_for_percentage(95), "A+")
        self.assertEqual(grade_for_percentage(90), "A+")
        self.assertEqual(grade_for_percentage(89.99), "A")
        self.assertEqual(grade_for_percentage(75), "B+")
        self.assertEqual(grade_for_percentage(65), "B")
        self.assertEqual(grade_for_percentage(55), "C")
        self.assertEqual(grade_for_percentage(40), "D")
        self.assertEqual(grade_for_percentage(39.9), "F")
        self.assertEqual(grade_for_percentage(0), "F")

    def test_grade_point_mapping(self):
        self.assertEqual(letter_to_grade_point("A+"), 10.0)
        self.assertEqual(letter_to_grade_point("F"), 0.0)
        self.assertEqual(letter_to_grade_point("Z"), 0.0) 


class TestValidators(unittest.TestCase):
    def test_valid_roll_no(self):
        self.assertEqual(validate_roll_no(" 26bce001 "), "26BCE001")

    def test_empty_roll_no_raises(self):
        with self.assertRaises(InvalidRollNumberError):
            validate_roll_no("   ")

    def test_non_alnum_roll_no_raises(self):
        with self.assertRaises(InvalidRollNumberError):
            validate_roll_no("26-BCE-001")

    def test_valid_name(self):
        self.assertEqual(validate_name("ASHISH"), "ASHISH")

    def test_name_with_digits_raises(self):
        with self.assertRaises(InvalidNameError):
            validate_name("ASHISH")

    def test_valid_marks(self):
        self.assertEqual(validate_marks("87.5"), 87.5)

    def test_non_numeric_marks_raises(self):
        with self.assertRaises(InvalidMarksError):
            validate_marks("abc")

    def test_out_of_range_marks_raises(self):
        with self.assertRaises(InvalidMarksError):
            validate_marks("150")
        with self.assertRaises(InvalidMarksError):
            validate_marks("-5")

    def test_subject_case_insensitive(self):
        self.assertEqual(validate_subject("python"), "Python")

    def test_unknown_subject_raises(self):
        with self.assertRaises(InvalidSubjectError):
            validate_subject("Astrology")


class TestStudentModel(unittest.TestCase):
    def setUp(self):
        self.student = Student("26BCE001", "ASHISH")
        self.student.set_marks("Python", 90)
        self.student.set_marks("Mathematics", 85)
        self.student.set_marks("Data Structures", 78)
        self.student.set_marks("English", 60)
        self.student.set_marks("Computer Networks", 70)

    def test_total_and_percentage(self):
        self.assertEqual(self.student.total_marks(), 383)
        self.assertAlmostEqual(self.student.percentage(), 76.6, places=1)

    def test_overall_grade(self):
        self.assertEqual(self.student.overall_grade(), "B+")

    def test_pass_with_all_subjects_cleared(self):
        self.assertTrue(self.student.is_overall_pass())

    def test_fail_when_one_subject_below_threshold(self):
        self.student.set_marks("English", 10)  
        self.assertIn("English", self.student.failed_subjects())
        self.assertFalse(self.student.is_overall_pass())

    def test_equality_by_roll_no(self):
        duplicate = Student("21BCE001", "Different Name")
        self.assertEqual(self.student, duplicate)


if __name__ == "__main__":
    unittest.main()
