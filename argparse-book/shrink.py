import argparse
from pathlib import Path

from PIL import Image


SHRINKED_LENGTH = 300


def shrink_image(image_path, shrinked_length, save_path=None):
    filename = image_path.name
    if is_target_image(filename):
        im = Image.open(image_path)
        if needs_shrink(im.size, shrinked_length):
            new_size = shrink_size(im.size, shrinked_length)
            resized_im = im.resize(new_size, Image.BICUBIC)
            if save_path is None:
                save_path = filename
            resized_im.save(save_path)
            print(f"画像を縮小しました: {filename}")


def is_target_image(filename):
    return filename.endswith((".png", ".jpg"))


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


def existing_path(path_str):
    path = Path(path_str)
    if not path.exists():
        message = f"{path_str} の指すファイル／ディレクトリが存在しません"
        raise argparse.ArgumentTypeError(message)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=existing_path)
    args = parser.parse_args()

    src_path = args.src
    if src_path.is_dir():
        dest_dir = Path(src_path.name)
        dest_dir.mkdir(exist_ok=True)
        for img_path in src_path.iterdir():
            save_path = dest_dir / img_path.name
            shrink_image(img_path, SHRINKED_LENGTH, save_path)
    else:
        shrink_image(src_path, SHRINKED_LENGTH)
