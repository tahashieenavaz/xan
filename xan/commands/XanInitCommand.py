import ast
import tomllib
from pathlib import Path, PosixPath


class XanInitCommand:
    def __init__(self):
        super().__init__()

    def init(self, root: str | PosixPath = "."):
        # if the passed argument is string convert it to PosixPath for consistency
        if isinstance(root, str):
            root = Path(root)

        # we do not iterate .git folder for efficiency
        if root.stem in [".git"]:
            return

        root_contents = list(root.iterdir())
        directories = filter(lambda item: item.is_dir(), root_contents)
        files = filter(lambda item: item.is_file(), root_contents)
        python_files = filter(
            lambda item: item.suffix == ".py" and item.stem != "__init__", files
        )

        for directory in directories:
            self.init(directory)

        class_names = []
        function_names = []

        for file in python_files:
            with open(file) as handler:
                tree = ast.parse(handler.read())

            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    class_names.append(
                        [
                            file.stem,
                            node.name,
                        ]
                    )
                elif isinstance(node, ast.FunctionDef):
                    function_names.append(
                        [
                            file.stem,
                            node.name,
                        ]
                    )

        if len(function_names) + len(class_names) > 0:
            with open(root / "__init__.py", "w+") as handler:
                for file, name in function_names:
                    handler.write(f"from .{file} import {name}\n")

                for file, name in class_names:
                    handler.write(f"from .{file} import {name}\n")

        parent_toml_file = root.parent / "pyproject.toml"
        current_toml_file = root / "pyproject.toml"
        if parent_toml_file.exists() and not current_toml_file.exists():
            toml_data = tomllib.loads(parent_toml_file.read_text())
            version = toml_data["project"]["version"]
            with open(root / "__init__.py", "a") as handler:
                handler.write(f'__version__ = "{version}"')
