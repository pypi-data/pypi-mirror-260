import os
import json
import shutil
from typing import Dict, List, Union


class File:

    @staticmethod
    def create_directory(path: str):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)

    @classmethod
    def remove(cls, path: str):
        if cls.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    @staticmethod
    def read_lines(
        filepath: str,
        mode: str = "r",
        encoding: str = "utf-8"
    ) -> Union[List, Dict]:
        with open(filepath, mode, encoding) as f:
            return f.readlines()

    @staticmethod
    def read(filepath: str, mode: str = "r", encoding: str = "utf-8"):
        with open(filepath, mode, encoding if mode == "r" else None) as f:
            return f.read()

    @staticmethod
    def read_json(filepath: str, mode: str = "r", encoding: str = "utf-8"):
        with open(filepath, mode, encoding if mode == "r" else None) as f:
            return json.load(f)

    @staticmethod
    def write_lines(
        filepath: str,
        lines: list,
        mode: str = "w",
        encoding: str = "utf-8"
    ):
        with open(filepath, mode, encoding) as f:
            f.writelines(lines)

    @staticmethod
    def write_json(
        filepath: str,
        lines: list,
        mode: str = "w",
        encoding: str = "utf-8"
    ):
        with open(filepath, mode, encoding) as f:
            json.dump(lines, f, ensure_ascii=False)

    @staticmethod
    def get_filename(path) -> str:
        return os.path.basename(path)
