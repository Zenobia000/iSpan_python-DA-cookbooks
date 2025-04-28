"""
路徑處理輔助模組

提供跨平台與跨環境(.py 和 .ipynb)的檔案路徑處理功能。
"""

import os
import sys
from pathlib import Path


def get_base_dir():
    """
    獲取專案基礎目錄，適用於不同執行環境。
    
    這個函數能同時在 .py 腳本和 Jupyter notebook 中工作。
    """
    try:
        # 嘗試使用 __file__ 變數 (.py 檔案)
        current_file = Path(__file__).resolve()
        
        # 根據當前檔案位置向上導航至專案根目錄
        # 注意：根據實際結構調整層級數量
        # 當前位置是: examples/file_handling/path_helper.py
        # 需要向上兩層才能到專案根目錄
        return current_file.parent.parent.parent
    
    except NameError:
        # 在沒有 __file__ 的環境中 (.ipynb)
        # 嘗試找到專案標記
        start_dir = Path.cwd()
        for directory in [start_dir, *start_dir.parents]:
            # 檢查是否有標記專案根目錄的檔案/目錄
            markers = [
                '.git',
                'pyproject.toml',
                'setup.py',
                'main.py',
                'README.md'
            ]
            if any((directory / marker).exists() for marker in markers):
                return directory
        
        # 若未找到標記，使用當前目錄
        return start_dir


class ProjectPaths:
    """
    專案路徑管理類，提供統一的路徑處理介面。
    """
    def __init__(self, base_dir=None):
        """
        初始化專案路徑管理器
        
        Args:
            base_dir: 明確指定的專案根目錄，若為None則自動檢測
        """
        # 設置基礎目錄
        self.base_dir = Path(base_dir) if base_dir else get_base_dir()
        
        # 定義常用目錄
        self.data_dir = self.base_dir / 'data'
        self.config_dir = self.base_dir / 'config'
        self.examples_dir = self.base_dir / 'examples'
        self.tutorials_dir = self.base_dir / 'tutorials'
        
        # 日誌和輸出目錄
        self.logs_dir = self.base_dir / 'logs'
        self.output_dir = self.base_dir / 'output'
        
        # 確保必要目錄存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """確保必要目錄存在"""
        for directory in [self.data_dir, self.logs_dir, self.output_dir]:
            directory.mkdir(exist_ok=True, parents=True)
    
    def get_data_file(self, filename):
        """獲取數據檔案的路徑"""
        return self.data_dir / filename
    
    def get_config_file(self, filename):
        """獲取設定檔案的路徑"""
        return self.config_dir / filename
    
    def get_output_file(self, filename):
        """獲取輸出檔案的路徑"""
        return self.output_dir / filename
    
    def get_log_file(self, filename):
        """獲取日誌檔案的路徑"""
        return self.logs_dir / filename
    
    def get_example_file(self, filename):
        """獲取範例檔案的路徑"""
        return self.examples_dir / filename
    
    def get_tutorial_file(self, filename):
        """獲取教學檔案的路徑"""
        return self.tutorials_dir / filename
    
    def get_relative_path(self, path):
        """獲取相對於專案根目錄的路徑"""
        return os.path.relpath(path, self.base_dir)
    
    def debug_info(self):
        """顯示路徑相關的調試資訊"""
        info = {
            "當前工作目錄": os.getcwd(),
            "專案根目錄": str(self.base_dir),
            "數據目錄": str(self.data_dir),
            "Python路徑": sys.path,
        }
        for key, value in info.items():
            print(f"{key}: {value}")


# 創建單例實例，便於導入使用
project_paths = ProjectPaths()


# 簡單測試功能
if __name__ == "__main__":
    print("路徑輔助模組測試")
    print("-" * 50)
    
    paths = ProjectPaths()
    paths.debug_info()
    
    print("\n檔案路徑測試:")
    data_file = paths.get_data_file("sample.csv")
    config_file = paths.get_config_file("settings.json")
    log_file = paths.get_log_file("app.log")
    
    print(f"範例數據檔案路徑: {data_file}")
    print(f"設定檔案路徑: {config_file}")
    print(f"日誌檔案路徑: {log_file}")
    
    # 創建測試檔案
    with open(data_file, "w") as f:
        f.write("id,name,value\n1,test,100\n")
    
    print(f"\n已創建範例數據檔案: {data_file}")
    print(f"檔案存在: {data_file.exists()}") 