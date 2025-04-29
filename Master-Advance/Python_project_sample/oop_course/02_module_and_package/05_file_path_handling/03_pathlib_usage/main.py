# 主題：不同操作系統的路徑分隔符不同 (Windows: '\\', Unix/Mac: '/')

# pathlib.Path 類的優勢:
# - 面向對象的接口，更直觀
# - 鏈式操作，代碼更簡潔
# - 自動處理不同操作系統的差異
# - 內置更多功能，減少對其他模組的依賴


from pathlib import Path

p = Path('folder/file.txt')
print("路徑:", p)
print("父目錄:", p.parent)


print("\n示範常用方法:")

# 創建與連接路徑
path = Path('folder') / 'file.txt'
print("路徑連接:", path)

# 獲取系統路徑
print("當前目錄:", Path.cwd())
print("主目錄:", Path.home())

# 路徑資訊
example_path = Path('folder/subfolder/example.txt')
print("絕對路徑:", example_path.absolute())
print("父目錄:", example_path.parent)
print("檔名:", example_path.name)
print("副檔名:", example_path.suffix)
print("純檔名:", example_path.stem)
print("路徑部分:", example_path.parts)

# 檢查路徑
current_file = Path(__file__)
print("當前檔案:", current_file)
print("檔案是否存在:", current_file.exists())
print("是否為檔案:", current_file.is_file())
print("是否為目錄:", current_file.parent.is_dir())

# 目錄操作
parent_dir = current_file.parent
print("\n當前目錄檔案:")
for item in parent_dir.iterdir():
    print(f"- {item.name}")

print("\n搜尋 .py 檔案:")
for py_file in parent_dir.glob("*.py"):
    print(f"- {py_file.name}")


