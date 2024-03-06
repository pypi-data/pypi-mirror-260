import os
import hashlib


def if_exist_remove(output_path: str) -> None:
    if os.path.exists(output_path):
        os.remove(output_path)


def calculate_hash(path) -> str:
    file_content = open(path, "rb").read()
    return hashlib.md5(file_content).hexdigest()


def assert_not_exist(output_path) -> None:
    assert not (os.path.exists(output_path))


def assert_exist(output_path) -> None:
    assert os.path.exists(output_path)
