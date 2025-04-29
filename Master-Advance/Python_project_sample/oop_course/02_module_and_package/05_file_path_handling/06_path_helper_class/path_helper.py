from pathlib import Path

class ProjectPaths:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.data_dir = self.project_root / "data"
        self.output_dir = self.project_root / "outputs"
        
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
    def get_data_file(self, name):
        return self.data_dir / name
    
    def get_output_file(self, name):
        return self.output_dir / name

project_paths = ProjectPaths()
