# %% [markdown]
# # 數據處理範例 (Notebook 版本)
# 
# 這個 Jupyter Notebook 展示如何在筆記本環境中使用與 `.py` 文件相同的模組處理檔案路徑和數據，
# 特別演示了如何解決 `.ipynb` 文件中常見的路徑問題。

# %% [markdown]
# ## 1. 環境設置與路徑處理
# 
# 首先導入必要的模組，並確認筆記本的工作目錄。

# %%
import os
import sys
from pathlib import Path

print(f"當前工作目錄: {os.getcwd()}")

# %% [markdown]
# ### 檢查是否可以直接導入 path_helper 模組
# 
# 我們先嘗試直接導入模組，若無法導入則調整搜尋路徑。

# %%
try:
    from path_helper import project_paths
    print("成功直接導入 path_helper 模組")
except ImportError:
    print("無法直接導入 path_helper 模組，將嘗試調整路徑")
    
    def find_directory_with_file(start_dir, target_file):
        start_path = Path(start_dir)
        for path in [start_path, *start_path.parents]:
            for root, dirs, files in os.walk(path):
                if target_file in files:
                    return Path(root)
        return None
    
    current_dir = os.getcwd()
    path_helper_dir = find_directory_with_file(current_dir, "path_helper.py")
    
    if path_helper_dir:
        print(f"找到 path_helper.py 於: {path_helper_dir}")
        if str(path_helper_dir) not in sys.path:
            sys.path.insert(0, str(path_helper_dir))
            print(f"已將 {path_helper_dir} 添加到模組搜尋路徑")
        from path_helper import project_paths
        print("成功導入 path_helper 模組")
    else:
        print("找不到 path_helper.py 檔案")
        print("將創建簡化版的路徑處理函數")
        
        class SimplePaths:
            def __init__(self):
                self.base_dir = Path(os.getcwd())
                self.data_dir = self.base_dir / 'data'
                self.output_dir = self.base_dir / 'output'
                self.config_dir = self.base_dir / 'config'
                for dir in [self.data_dir, self.output_dir, self.config_dir]:
                    dir.mkdir(exist_ok=True, parents=True)
            
            def get_data_file(self, filename):
                return self.data_dir / filename
            
            def get_output_file(self, filename):
                return self.output_dir / filename
            
            def get_config_file(self, filename):
                return self.config_dir / filename
            
            def debug_info(self):
                print(f"使用簡化版的路徑類\n當前工作目錄: {os.getcwd()}\n數據目錄: {self.data_dir}")
        
        project_paths = SimplePaths()

# %% [markdown]
# ### 顯示專案路徑資訊
# 
# 檢查路徑模組是否正確工作。

# %%
project_paths.debug_info()
data_dir = project_paths.data_dir
print(f"\n數據目錄: {data_dir}")
print(f"此目錄存在: {data_dir.exists()}")

# %% [markdown]
# ## 2. 導入和使用 DataProcessor 類
# 
# 我們有兩種選擇：
# 1. 從 `data_processor.py` 檔案導入
# 2. 在筆記本中直接定義

# %%
try:
    path_helper_dir = None
    for path in sys.path:
        if Path(path, "path_helper.py").exists():
            path_helper_dir = Path(path)
            break
    if path_helper_dir and Path(path_helper_dir, "data_processor.py").exists():
        from data_processor import DataProcessor
        print("成功從 data_processor.py 導入 DataProcessor 類")
    else:
        raise ImportError("找不到 data_processor.py 檔案")
except ImportError as e:
    print(f"無法導入 DataProcessor 類: {e}")
    print("將直接在筆記本中定義 DataProcessor 類")
    
    import csv
    import json
    import datetime

    class DataProcessor:
        def __init__(self, config_file="settings.json"):
            self.config_file = project_paths.get_config_file(config_file)
            self.config = self._load_config()
        
        def _load_config(self):
            if not self.config_file.exists():
                default_config = {
                    "input_file": "input.csv",
                    "output_file": "processed.csv",
                    "transformations": ["uppercase", "add_timestamp"],
                    "delimiter": ","
                }
                self.config_file.parent.mkdir(exist_ok=True, parents=True)
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=4)
                print(f"已創建預設設定檔案: {self.config_file}")
                return default_config
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"設定檔案格式錯誤: {self.config_file}")
                return {}

        def create_sample_data(self):
            input_file = project_paths.get_data_file(self.config.get("input_file", "input.csv"))
            sample_data = [
                ["id", "name", "category", "price"],
                ["1", "Apple", "Fruit", "1.99"],
                ["2", "Banana", "Fruit", "0.99"],
                ["3", "Carrot", "Vegetable", "0.49"],
                ["4", "Milk", "Dairy", "2.49"],
                ["5", "Bread", "Bakery", "3.29"]
            ]
            with open(input_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=self.config.get("delimiter", ","))
                writer.writerows(sample_data)
            print(f"已創建示範數據檔案: {input_file}")
            return input_file

        def process_data(self, input_file=None, output_file=None):
            input_file = input_file or self.config.get("input_file", "input.csv")
            output_file = output_file or self.config.get("output_file", "processed.csv")
            input_path = project_paths.get_data_file(input_file)
            output_path = project_paths.get_output_file(output_file)
            if not input_path.exists():
                print(f"輸入檔案不存在: {input_path}")
                input_path = self.create_sample_data()
            try:
                with open(input_path, ' 'r', encoding='utf-8') as f:
                    reader = csv.reader(f, delimiter=self.config.get("delimiter", ","))
                    rows = list(reader)
                if not rows:
                    print("輸入檔案為空")
                    return None
                header = rows[0]
                data_rows = rows[1:]
                transformations = self.config.get("transformations", [])
                processed_rows = []
                for row in data_rows:
                    processed_row = row.copy()
                    if "uppercase" in transformations and len(row) > 1:
                        processed_row[1] = row[1].upper()
                    if "add_timestamp" in transformations:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        processed_row.append(timestamp)
                    processed_rows.append(processed_row)
                if "add_timestamp" in transformations and header:
                    header = header.copy()
                    header.append("timestamp")
                output_path.parent.mkdir(exist_ok=True, parents=True)
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=self.config.get("delimiter", ","))
                    writer.writerow(header)
                    writer.writerows(processed_rows)
                print(f"數據處理完成，結果保存至: {output_path}")
                return output_path
            except Exception as e:
                print(f"處理數據時出錯: {e}")
                return None

        def print_summary(self, file_path=None):
            file_path = file_path or project_paths.get_output_file(self.config.get("output_file", "processed.csv"))
            if not file_path.exists():
                print(f"檔案不存在: {file_path}")
                return
            try:
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

# %% [markdown]
# ## 3. 使用 DataProcessor 處理數據

# %%
print("創建數據處理器...", end="")
processor = DataProcessor()
print("完成")

print(f"設定檔案位置: {processor.config_file}")
print(f"設定檔案存在: {processor.config_file.exists()}")
print(f"當前設定: {processor.config}")

# %%
print("開始處理數據...")
output_file = processor.process_data()

if output_file and output_file.exists():
    print(f"處理成功，輸出檔案: {output_file}")
else:
    print("數據處理失敗")

# %%
processor.print_summary(output_file)

# %% [markdown]
# ## 4. 使用 Pandas 進一步分析處理後的數據

# %%
try:
    import pandas as pd
    import matplotlib.pyplot as plt

    if output_file and output_file.exists():
        df = pd.read_csv(output_file)
        print("處理後的數據:")
        display(df)
        if 'price' in df.columns:
            df['price'] = pd.to_numeric(df['price'])
            print("\n價格統計:")
            print(df['price'].describe())
            plt.figure(figsize=(10, 6))
            if 'category' in df.columns:
                category_prices = df.groupby('category')['price'].mean().sort_values(ascending=False)
                category_prices.plot(kind='bar', color='skyblue')
                plt.title('各類別平均價格')
                plt.ylabel('平均價格')
                plt.xlabel('類別')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
    else:
        print("找不到處理後的檔案，無法進行數據分析")
except ImportError:
    print("無法導入 pandas 或 matplotlib，請安裝這些套件: pip install pandas matplotlib")
except Exception as e:
    print(f"數據分析時發生錯誤: {e}")

# %% [markdown]
# ## 5. 總結與比較
# 
# (此處簡化，詳細參考原本的說明)

