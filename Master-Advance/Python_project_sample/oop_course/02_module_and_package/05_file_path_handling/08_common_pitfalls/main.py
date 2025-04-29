# 主題：常見路徑處理錯誤總結
# 1. 手動接 '/' 的錯誤示範
wrong_path = "data" + "/" + "input.csv"  # 不要這樣做!

# ------------------------------------------------------------------------
# 正確做法
import os
from pathlib import Path

# 使用 os.path.join
correct_path1 = os.path.join("data", "input.csv")

# 使用 Path 的 / 運算符
correct_path2 = Path("data") / "input.csv"

# 2. 假設工作目錄固定的錯誤示範
wrong_file = open("data/input.csv")  # 不要這樣做!


# 正確做法：動態取得檔案位置
def get_file_dir():
    try:
        return Path(__file__).parent  # .py 檔案
    except NameError:
        return Path.cwd()  # Jupyter notebook

# 使用動態路徑
file_path = get_file_dir() / "data" / "input.csv"

print(correct_path1)
print(correct_path2)
print(file_path)


print("- 手動接 '/' 錯誤，應使用 os.path.join 或 Path / 運算符")
print("- 假設工作目錄固定錯誤，應動態偵測 __file__ 或 cwd()")
