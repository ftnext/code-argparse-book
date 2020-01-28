import argparse
from pathlib import Path

from PIL import Image


SHRINKED_LENGTH = 300


def is_target_image(filename):
    return filename.endswith((".png", ".jpg"))


def target_image_path_pair(src_path):
    filename = src_path.name
    if is_target_image(filename):
        return {"src": src_path, "dest": filename}


def needs_shrink(width_height_pair, limit):
    width, height = width_height_pair
    return width > limit and height > limit


def shrink_size(width_height_pair, max_length):
    width, height = width_height_pair
    if width > height:
        new_width = max_length
        new_height = int((max_length / width) * height)
    else:
        new_width = int((max_length / height) * width)
        new_height = max_length
    return (new_width, new_height)


def shrink_image(src_path, dest_path, shrinked_length):
    im = Image.open(src_path)
    if needs_shrink(im.size, shrinked_length):
        new_size = shrink_size(im.size, shrinked_length)
        resized_im = im.resize(new_size, Image.BICUBIC)
        resized_im.save(dest_path)
        print(f"画像を縮小しました: {dest_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=Path)
    args = parser.parse_args()

    src_path = args.src
    target_pair = target_image_path_pair(src_path)
    if target_pair:
        shrink_image(target_pair["src"], target_pair["dest"], SHRINKED_LENGTH)
