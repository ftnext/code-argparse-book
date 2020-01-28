import argparse
from pathlib import Path

from PIL import Image


SHRINKED_LENGTH = 300


def is_target_image(filename):
    return filename.endswith((".png", ".jpg"))


def is_directory_path(a_path):
    """拡張子の.を含まない場合、ディレクトリのパスと判断する"""
    return "." not in a_path.name


def target_image_path_pairs(src_path, dest_path):
    path_pairs = []
    if src_path.is_dir():
        dest_dir = dest_path / src_path.name
        for img_path in src_path.iterdir():
            filename = img_path.name
            if is_target_image(filename):
                save_path = dest_dir / filename
                path_pair = {"src": img_path, "dest": save_path}
                path_pairs.append(path_pair)
        dest_dir.mkdir(exist_ok=True)
    else:
        filename = src_path.name
        if is_target_image(filename):
            if dest_path.resolve() == Path.cwd():
                path_pair = {"src": src_path, "dest": filename}
            elif is_directory_path(dest_path):
                dest_file_path = dest_path / filename
                path_pair = {"src": src_path, "dest": dest_file_path}
                dest_path.mkdir(parents=True, exist_ok=True)
            else:
                path_pair = {"src": src_path, "dest": dest_path}
                dest_dir = dest_path.parent
                dest_dir.mkdir(parents=True, exist_ok=True)
            path_pairs.append(path_pair)
    return path_pairs


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


def existing_path(path_str):
    path = Path(path_str)
    if not path.exists():
        message = f"{path_str} の指すファイル／ディレクトリが存在しません"
        raise argparse.ArgumentTypeError(message)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=existing_path)
    parser.add_argument("--dest", type=Path, default=Path("."))
    args = parser.parse_args()

    src_path = args.src
    dest_path = args.dest
    target_pairs = target_image_path_pairs(src_path, dest_path)
    if target_pairs:
        for target_pair in target_pairs:
            shrink_image(
                target_pair["src"], target_pair["dest"], SHRINKED_LENGTH
            )
