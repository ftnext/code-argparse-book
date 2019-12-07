from pathlib import Path

from PIL import Image


SHRINKED_LENGTH = 300


if __name__ == "__main__":
    src_path = Path("/Users/.../Downloads/pyconjp.jpg")  # 絶対パスを指定してください
    filename = src_path.name
    if filename.endswith((".png", ".jpg")):
        im = Image.open(src_path)
        width, height = im.size
        if width > SHRINKED_LENGTH and height > SHRINKED_LENGTH:
            if width > height:
                new_width = SHRINKED_LENGTH
                new_height = int((SHRINKED_LENGTH / width) * height)
            else:
                new_width = int((SHRINKED_LENGTH / height) * width)
                new_height = SHRINKED_LENGTH
            resized_im = im.resize((new_width, new_height), Image.BICUBIC)
            resized_im.save(filename)
            print(f"画像を縮小しました: {filename}")
