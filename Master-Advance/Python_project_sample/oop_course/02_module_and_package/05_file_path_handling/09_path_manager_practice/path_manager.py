from pathlib import Path

class PathManager:
    def __init__(self):
        self.base = Path(__file__).parent

    def to_absolute(self, relative_path):
        return (self.base / relative_path).resolve()

    def debug(self):
        print("Base Path:", self.base)

path_manager = PathManager()
