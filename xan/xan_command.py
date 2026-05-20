import glob
import os
import ast
from pathlib import Path


def handle_directory(directory_relative_address: str):
    directory_address = directory_relative_address.strip("/")
    init_file_address = directory_address + "/__init__.py"
    file_pattern = directory_address + "/*"
    files = glob.glob(file_pattern)

    functions = []
    classes = []

    for file in files:
        if os.path.isdir(file):
            handle_directory(file)

        path_instance = Path(file)

        if path_instance.name == "__init__.py":
            continue

        print(path_instance.stem)

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


def xan_command(start_directory: str = "."):
    handle_directory(start_directory)
