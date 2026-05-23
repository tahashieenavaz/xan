import glob
import os
import ast
from pathlib import Path


class XanInitCommand:
    def __init__(self):
        super().__init__()

    def __is_main_init(self, path) -> bool:
        return (path.parent / "pyproject.toml").exists()

    def init(self, root: str = "."):
        directory_address = root.strip("/")
        init_file_address = directory_address + "/__init__.py"
        init_file_path = Path(init_file_address)
        files_pattern = directory_address + "/*"
        files = glob.glob(files_pattern)

        is_main_init = False
        if self.__is_main_init(init_file_path):
            is_main_init = True

        functions = []
        classes = []

        for file in files:
            if os.path.isdir(file):
                self.init(file)

            path_instance = Path(file)

            if path_instance.name == "__init__.py":
                continue

            if path_instance.is_file() and path_instance.suffix == ".py":
                text = path_instance.read_text()
                tree = ast.parse(text)
                filename = path_instance.stem

                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):
                        functions.append([filename, node.name])
                    elif isinstance(node, ast.AsyncFunctionDef):
                        functions.append([filename, node.name])
                    elif isinstance(node, ast.ClassDef):
                        classes.append([filename, node.name])

        if len(functions) + len(classes) == 0:
            return

        with open(init_file_address, "w+") as fh:
            for filename, function in functions:
                fh.write(f"from .{filename} import {function}\n")

            for filename, class_name in classes:
                fh.write(f"from .{filename} import {class_name}\n")

            print((init_file_path.parent / "pyproject.toml").exists())
            if is_main_init:
                fh.write("\n\nversion\n\n")

            fh.write("\n__all__ = [\n")
            for _, class_name in classes:
                fh.write(f'\t"{class_name}",\n')

            for _, function in functions:
                fh.write(f'\t"{function}",\n')
            fh.write("]")
