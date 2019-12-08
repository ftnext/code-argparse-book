import argparse
import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import call, MagicMock, patch

from PIL import Image

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


class ShrinkImageTestCase(TestCase):
    @patch("shrink.shrink_size", spec=s.shrink_size)
    @patch("shrink.needs_shrink", spec=s.needs_shrink, return_value=True)
    @patch("shrink.Image.open", spec=Image.open)
    @patch("shrink.is_target_image", spec=s.is_target_image, return_value=True)
    def test_not_specify_save_path(
        self, is_target_image, mock_open, needs_shrink, shrink_size
    ):
        image_path = MagicMock(spec=Path)
        shrinked_length = MagicMock(spec=int)
        image_mock = mock_open.return_value
        new_size = shrink_size.return_value
        resized_im = image_mock.resize.return_value

        s.shrink_image(image_path, shrinked_length)

        self.assertEqual(
            is_target_image.call_args_list, [call(image_path.name)]
        )
        self.assertEqual(mock_open.call_args_list, [call(image_path)])
        self.assertEqual(
            needs_shrink.call_args_list,
            [call(image_mock.size, shrinked_length)],
        )
        self.assertEqual(
            shrink_size.call_args_list,
            [call(image_mock.size, shrinked_length)],
        )
        self.assertEqual(
            image_mock.resize.call_args_list, [call(new_size, Image.BICUBIC)]
        )
        self.assertEqual(
            resized_im.save.call_args_list, [call(image_path.name)]
        )
