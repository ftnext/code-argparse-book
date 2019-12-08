import argparse
import os
from pathlib import Path
from unittest import TestCase

import shrink as s


class ExistingPathTestCase(TestCase):
    def setUp(self):
        self.test_directory = os.path.dirname(__file__)

    def test_exists_path(self):
        exists_file_path = os.path.join(
            self.test_directory, "data", "existing_path", "exists_file.txt"
        )
        expected = Path(exists_file_path)

        actual = s.existing_path(exists_file_path)

        self.assertEqual(actual, expected)

    def test_not_exists_path(self):
        not_exists_file_path = os.path.join(
            self.test_directory, "data", "not_exists.png"
        )
        expected_message = f"{not_exists_file_path} の指すファイル／ディレクトリが存在しません"

        with self.assertRaises(argparse.ArgumentTypeError) as cm:
            s.existing_path(not_exists_file_path)
        self.assertEqual(str(cm.exception), expected_message)
