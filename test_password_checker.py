import unittest
from password_strength_checker import assess_password


class TestPasswordChecker(unittest.TestCase):

    def test_empty_password(self):
        score, strength, suggestions = assess_password("")
        self.assertEqual(score, 0)
        self.assertEqual(strength, "Very Weak")

    def test_short_password(self):
        score, strength, suggestions = assess_password("abc")
        self.assertNotEqual(strength, "Very Strong")

    def test_common_password(self):
        score, strength, suggestions = assess_password("password123")
        self.assertEqual(score, 0)
        self.assertEqual(strength, "Very Weak")

    def test_strong_password(self):
        score, strength, suggestions = assess_password(
            "Violet!River82_Moon"
        )
        self.assertEqual(strength, "Very Strong")

    def test_repeated_characters(self):
        score, strength, suggestions = assess_password("AAAA1234!")
        self.assertNotEqual(strength, "Very Strong")


if __name__ == "__main__":
    unittest.main()