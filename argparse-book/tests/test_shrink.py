import os
from pathlib import Path
from unittest import TestCase

import shrink as s


class ExistingPathTestCase(TestCase):
    def test_exists_path(self):
        test_directory = os.path.dirname(__file__)
        exists_file_path = os.path.join(
            test_directory, "data", "existing_path", "exists_file.txt"
        )
        expected = Path(exists_file_path)

        actual = s.existing_path(exists_file_path)

        self.assertEqual(actual, expected)
