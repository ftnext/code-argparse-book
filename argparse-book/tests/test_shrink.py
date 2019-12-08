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


class IsTargetImageTestCase(TestCase):
    def test_is_target(self):
        target_file_names = ["kumiko.jpg", "kanade.png"]
        for filename in target_file_names:
            with self.subTest(filename=filename):
                actual = s.is_target_image(filename)
                self.assertTrue(actual)

    def test_not_target(self):
        not_target_file_names = ["asuka.jpeg", "inochi.txt", "brassband"]
        for filename in not_target_file_names:
            with self.subTest(filename=filename):
                actual = s.is_target_image(filename)
                self.assertFalse(actual)


class NeedsShrinkTestCase(TestCase):
    def setUp(self):
        self.limit = 400

    def test_needs_shrink(self):
        needs_shrink_sizes = [(500, 700), (401, 550), (600, 401)]
        for size in needs_shrink_sizes:
            with self.subTest(size=size):
                actual = s.needs_shrink(size, self.limit)
                self.assertTrue(actual)

    def test_not_shrink(self):
        not_shrink_sizes = [
            (200, 300),
            (400, 400),
            (600, 200),
            (450, 399),
            (300, 500),
            (400, 600),
        ]
        for size in not_shrink_sizes:
            with self.subTest(size=size):
                actual = s.needs_shrink(size, self.limit)
                self.assertFalse(actual)


class ShrinkSizeTestCase(TestCase):
    def setUp(self):
        self.max_length = 400

    def test_width_bigger_than_height(self):
        size = (600, 300)
        actual = s.shrink_size(size, self.max_length)
        self.assertEqual(actual, (400, 200))

    def test_height_bigger_than_width(self):
        size = (500, 700)
        actual = s.shrink_size(size, self.max_length)
        self.assertEqual(actual, (285, 400))

    def test_width_equal_height(self):
        size = (700, 700)
        actual = s.shrink_size(size, self.max_length)
        self.assertEqual(actual, (400, 400))
