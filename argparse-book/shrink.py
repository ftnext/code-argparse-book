import argparse
from pathlib import Path

from PIL import Image


SHRINKED_LENGTH = 300


def target_image_path_pair(src_path):
    filename = src_path.name
    if filename.endswith((".png", ".jpg")):
        return {"src": src_path, "dest": filename}


def shrink_image(src_path, dest_path, shrinked_length):
    im = Image.open(src_path)
    width, height = im.size
    if width > shrinked_length and height > shrinked_length:
        if width > height:
            new_width = shrinked_length
            new_height = int((shrinked_length / width) * height)
        else:
            new_width = int((shrinked_length / height) * width)
            new_height = shrinked_length
        resized_im = im.resize((new_width, new_height), Image.BICUBIC)
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
