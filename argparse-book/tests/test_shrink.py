from pathlib import Path
from unittest import TestCase
from unittest.mock import call, MagicMock, patch

from PIL import Image

import shrink as s


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


class SrcDestPathPairsTestCase(TestCase):
    def setUp(self):
        self.src_path = MagicMock(spec=Path)
        self.dest_path = MagicMock(spec=Path)

    @patch("shrink.is_target_image", return_value=False)
    def test_empty(self, is_target_image):
        filename = self.src_path.name

        actual = s.src_dest_path_pairs(self.src_path, self.dest_path)

        self.assertEqual(is_target_image.call_args_list, [call(filename)])
        self.assertEqual(actual, [])

    @patch("shrink.is_target_image", return_value=True)
    def test_one_pair(self, is_target_image):
        filename = self.src_path.name
        dest_path = self.dest_path / filename
        expected_pair = {"src": self.src_path, "dest": dest_path}

        actual = s.src_dest_path_pairs(self.src_path, self.dest_path)

        self.assertEqual(is_target_image.call_args_list, [call(filename)])
        self.assertEqual(actual, [expected_pair])


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
    def setUp(self):
        self.src_path = MagicMock(spec=Path)
        self.save_path = MagicMock(spec=Path)
        self.shrinked_length = MagicMock(spec=int)

    @patch("shrink.shrink_size", spec=s.shrink_size)
    @patch("shrink.needs_shrink", spec=s.needs_shrink, return_value=True)
    @patch("shrink.Image.open", spec=Image.open)
    def test_shrink(self, image_open, needs_shrink, shrink_size):
        image = image_open.return_value
        new_size = shrink_size.return_value
        resized_im = image.resize.return_value

        s.shrink_image(self.src_path, self.save_path, self.shrinked_length)

        self.assertEqual(image_open.call_args_list, [call(self.src_path)])
        self.assertEqual(
            needs_shrink.call_args_list,
            [call(image.size, self.shrinked_length)],
        )
        self.assertEqual(
            shrink_size.call_args_list,
            [call(image.size, self.shrinked_length)],
        )
        self.assertEqual(
            image.resize.call_args_list, [call(new_size, Image.BICUBIC)]
        )
        self.assertEqual(
            resized_im.save.call_args_list, [call(self.save_path)]
        )

    @patch("shrink.needs_shrink", spec=s.needs_shrink, return_value=False)
    @patch("shrink.Image.open", spec=Image.open)
    def test_not_shrink(self, image_open, needs_shrink):
        image = image_open.return_value

        s.shrink_image(self.src_path, self.save_path, self.shrinked_length)

        self.assertEqual(image_open.call_args_list, [call(self.src_path)])
        self.assertEqual(
            needs_shrink.call_args_list,
            [call(image.size, self.shrinked_length)],
        )
