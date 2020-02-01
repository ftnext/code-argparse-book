import argparse
from pathlib import Path

from PIL import Image


SHRINKED_LENGTH = 300


def is_target_image(filename):
    return filename.endswith((".png", ".jpg"))


def is_directory_path(a_path):
    """拡張子の.を含まない場合、ディレクトリのパスと判断する

    Path(".")の場合はnameが''となるため、ディレクトリのパスと判断される
    """
    return "." not in a_path.name


def is_current_directory_path(a_path):
    return a_path.resolve() == Path.cwd()


def is_valid_src_and_dest(src_path, dest_path):
    """srcとdestの組合せが適切かを確認

    src_pathがディレクトリ、かつ、dest_pathがファイルの場合に限って、False
    """
    if src_path.is_dir():
        return is_directory_path(dest_path)
    return True


def listup_image_paths(a_path):
    paths = []
    if a_path.is_dir():
        for item_path in a_path.iterdir():
            if is_target_image(item_path.name):
                paths.append(item_path)
        return paths
    if is_target_image(a_path.name):
        paths.append(a_path)
    return paths


def dest_dir_path(dest_path, src_path):
    # 前提：dest_pathとsrc_pathの組合せは適切（この関数で組合せについてエラーの判断はしなくていい）
    if is_current_directory_path(dest_path) and src_path.is_dir():
        dest_dir = dest_path / src_path.name
    else:
        dest_dir = dest_path
    dest_dir.mkdir(parents=True, exist_ok=True)
    return dest_dir


def src_dest_path_pairs(src_paths, dest_dir):
    # dest_dirをファイルのバスも受け付けるようにすると共通化できそう
    path_pairs = []
    for src_path in src_paths:
        dest_path = dest_dir / src_path.name
        path_pair = {"src": src_path, "dest": dest_path}
        path_pairs.append(path_pair)
    return path_pairs


def target_image_path_pairs(src_path, dest_path):
    if not is_directory_path(dest_path):
        assert src_path.is_file()
        # destのパスで指定されたディレクトリがないときは落とす（TODO：dest.parentディレクトリを作るか検討）
        return [{"src": src_path, "dest": dest_path}]
    # 以下では、dest_pathがカレントディレクトリ以外のディレクトリ
    # srcがディレクトリまたはファイルだが、以下の関数でファイルへのパスのリストに揃う
    src_image_paths = listup_image_paths(src_path)
    dest_dir = dest_dir_path(dest_path, src_path)
    path_pairs = src_dest_path_pairs(src_image_paths, dest_dir)
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
    if not is_valid_src_and_dest(src_path, dest_path):
        message = f"ディレクトリの画像の指定先がファイルです。ディレクトリを指定してください"
        raise ValueError(message)
    target_pairs = target_image_path_pairs(src_path, dest_path)
    if target_pairs:
        for target_pair in target_pairs:
            shrink_image(
                target_pair["src"], target_pair["dest"], SHRINKED_LENGTH
            )
