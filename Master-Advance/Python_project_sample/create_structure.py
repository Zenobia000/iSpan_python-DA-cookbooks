import os
import sys

def create_project_structure():
    """創建專案所需的目錄結構"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定義要創建的目錄結構
    directories = [
        os.path.join(base_dir, 'tutorials'),
        os.path.join(base_dir, 'examples', 'file_handling'),
        os.path.join(base_dir, 'examples', 'oop_examples'),
    ]
    
    # 創建目錄
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"已創建目錄: {directory}")
        except Exception as e:
            print(f"無法創建目錄 {directory}: {e}")
    
    # 創建教學文件的基本架構
    tutorial_files = [
        '01_modules.md',
        '02_packages.md',
        '03_init_files.md',
        '04_file_paths.md',
        '05_cross_folder.md',
        '06_py_vs_ipynb.md',
        '07_functions_to_classes.md',
        '08_inheritance.md',
        '09_encapsulation.md',
        '10_design_patterns.md',
    ]
    
    for file_name in tutorial_files:
        file_path = os.path.join(base_dir, 'tutorials', file_name)
        # 只有在文件不存在時才創建
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {file_name.split('.')[0]}\n\n待編寫的教學內容\n")
                print(f"已創建文件: {file_path}")
            except Exception as e:
                print(f"無法創建文件 {file_path}: {e}")
    
    print("\n專案結構已成功創建！")

if __name__ == "__main__":
    create_project_structure() 