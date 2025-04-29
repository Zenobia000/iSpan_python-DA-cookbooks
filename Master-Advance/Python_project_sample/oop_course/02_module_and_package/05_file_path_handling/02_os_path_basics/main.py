# 主題：不同操作系統的路徑分隔符不同 (Windows: '\\', Unix/Mac: '/')

import os

print("當前工作目錄:", os.getcwd())
print("連接路徑:", os.path.join("folder", "file.txt"))

print("\n示範常用函數:")

# 絕對路徑
print("絕對路徑:", os.path.abspath("file.txt"))

# 目錄與檔名
path = "/path/to/file.txt"
print("目錄部分:", os.path.dirname(path))
print("檔名部分:", os.path.basename(path))

# 檢查路徑
print("路徑是否存在:", os.path.exists("main.py"))
print("是否為檔案:", os.path.isfile("main.py"))
print("是否為目錄:", os.path.isdir("."))

# 分離副檔名
filename = "example.txt"
name, ext = os.path.splitext(filename)
print("檔名:", name)
print("副檔名:", ext)


