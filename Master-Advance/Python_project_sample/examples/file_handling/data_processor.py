"""
數據處理範例

展示如何使用 path_helper 模組處理檔案路徑，並進行簡單的數據操作。
"""

import csv
import json
import os
from pathlib import Path

# 導入路徑處理模組
from path_helper import project_paths


class DataProcessor:
    """數據處理類，示範物件導向方式處理數據檔案"""
    
    def __init__(self, config_file="settings.json"):
        """
        初始化數據處理器
        
        Args:
            config_file: 設定檔案名稱，位於 config 目錄
        """
        self.config_file = project_paths.get_config_file(config_file)
        self.config = self._load_config()
        
        # 確保數據目錄存在
        data_dir = project_paths.data_dir
        data_dir.mkdir(exist_ok=True, parents=True)
    
    def _load_config(self):
        """
        載入設定檔案
        
        如果設定檔案不存在，則創建預設設定
        """
        if not self.config_file.exists():
            default_config = {
                "input_file": "input.csv",
                "output_file": "processed.csv",
                "transformations": ["uppercase", "add_timestamp"],
                "delimiter": ",",
                "debug": True
            }
            
            # 創建設定檔案目錄
            self.config_file.parent.mkdir(exist_ok=True, parents=True)
            
            # 寫入預設設定
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)
            
            print(f"已創建預設設定檔案: {self.config_file}")
            return default_config
        
        # 載入既有設定
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"設定檔案格式錯誤: {self.config_file}")
            return {}
    
    def create_sample_data(self):
        """創建示範數據檔案"""
        input_file = project_paths.get_data_file(self.config.get("input_file", "input.csv"))
        
        # 示範數據
        sample_data = [
            ["id", "name", "category", "price"],
            ["1", "Apple", "Fruit", "1.99"],
            ["2", "Banana", "Fruit", "0.99"],
            ["3", "Carrot", "Vegetable", "0.49"],
            ["4", "Milk", "Dairy", "2.49"],
            ["5", "Bread", "Bakery", "3.29"]
        ]
        
        # 寫入CSV檔案
        with open(input_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=self.config.get("delimiter", ","))
            writer.writerows(sample_data)
        
        print(f"已創建示範數據檔案: {input_file}")
        return input_file
    
    def process_data(self, input_file=None, output_file=None):
        """
        處理數據檔案
        
        Args:
            input_file: 輸入檔案名稱，若為None則使用設定中的檔案
            output_file: 輸出檔案名稱，若為None則使用設定中的檔案
        
        Returns:
            處理後的輸出檔案路徑
        """
        # 使用設定檔中的值作為預設值
        input_file = input_file or self.config.get("input_file", "input.csv")
        output_file = output_file or self.config.get("output_file", "processed.csv")
        
        # 確保使用完整路徑
        input_path = project_paths.get_data_file(input_file)
        output_path = project_paths.get_output_file(output_file)
        
        # 檢查輸入檔案是否存在
        if not input_path.exists():
            print(f"輸入檔案不存在: {input_path}")
            print("將創建示範數據檔案...")
            input_path = self.create_sample_data()
        
        # 讀取數據
        rows = []
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=self.config.get("delimiter", ","))
                rows = list(reader)
                
                if not rows:
                    print("輸入檔案為空")
                    return None
        except Exception as e:
            print(f"讀取檔案時出錯: {e}")
            return None
        
        # 獲取標題行和數據行
        header = rows[0]
        data_rows = rows[1:]
        
        # 應用轉換
        transformations = self.config.get("transformations", [])
        
        # 處理數據
        processed_rows = []
        for row in data_rows:
            processed_row = row.copy()
            
            # 套用設定中的轉換
            if "uppercase" in transformations and len(row) > 1:
                processed_row[1] = row[1].upper()  # 將第二列轉為大寫
            
            if "add_timestamp" in transformations:
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                processed_row.append(timestamp)  # 添加時間戳
            
            processed_rows.append(processed_row)
        
        # 更新標題列
        if "add_timestamp" in transformations and header:
            header = header.copy()
            header.append("timestamp")
        
        # 寫入處理後的數據
        try:
            # 確保輸出目錄存在
            output_path.parent.mkdir(exist_ok=True, parents=True)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=self.config.get("delimiter", ","))
                writer.writerow(header)
                writer.writerows(processed_rows)
            
            print(f"數據處理完成，結果保存至: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"寫入檔案時出錯: {e}")
            return None
    
    def print_summary(self, file_path=None):
        """
        打印檔案內容摘要
        
        Args:
            file_path: 要摘要的檔案路徑，若為None則使用最新處理的輸出檔案
        """
        if file_path is None:
            file_path = project_paths.get_output_file(self.config.get("output_file", "processed.csv"))
        
        if not file_path.exists():
            print(f"檔案不存在: {file_path}")
            return
        
        try:
            rows = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=self.config.get("delimiter", ","))
                rows = list(reader)
            
            if not rows:
                print("檔案為空")
                return
            
            header = rows[0]
            data_rows = rows[1:]
            
            print(f"\n檔案摘要: {file_path}")
            print(f"總行數: {len(rows)}")
            print(f"標題: {header}")
            print("\n前3行數據:")
            
            for i, row in enumerate(data_rows[:3]):
                print(f"  {i+1}: {row}")
            
            if len(data_rows) > 3:
                print(f"  ... (共 {len(data_rows)} 行)")
            
        except Exception as e:
            print(f"讀取檔案時出錯: {e}")


# 直接執行時的示範代碼
if __name__ == "__main__":
    print("數據處理範例")
    print("-" * 50)
    
    # 顯示專案路徑信息
    print("專案路徑信息:")
    project_paths.debug_info()
    print("-" * 50)
    
    # 創建數據處理器
    processor = DataProcessor()
    
    # 處理數據
    output_file = processor.process_data()
    
    # 顯示結果摘要
    processor.print_summary(output_file) 