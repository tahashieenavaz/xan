import os
import ast
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

        root_contents = root.iterdir()
        for entity in root_contents:
            if entity.is_dir():
                self.init(entity)
                continue

            print(entity.absolute())
