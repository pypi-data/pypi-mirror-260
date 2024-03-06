"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Test cases for the project.
"""

import unittest
from typing import List
from my_moodle import MoodleDataUtility


class MoodleDataUtilityTestSuite(unittest.TestCase):
    """Module for testing the MoodleDataUtility class."""

    def test_convert_to_slug(self) -> None:
        """Test the convert_to_slug function.

        This function reads test data from a CSV file, where each line contains a full name
        and its corresponding expected slug. It then compares the output of convert_to_slug
        with the expected slug for each full name.
        """

        test_file: str = "test-data/slug-test.csv"

        full_names: List[str] = []
        expected: List[str] = []

        with open(test_file, encoding="utf-8") as file:
            for line in file:
                full_name, slug = line.split(",")
                full_names.append(full_name)
                expected.append(slug.strip())

        for index, full_name in enumerate(full_names):
            actual = MoodleDataUtility.convert_to_slug(full_name)
            self.assertEqual(actual, expected[index])


if __name__ == "__main__":
    unittest.main()
