print("=== 命名衝突問題示範 ===")
print("這個示例展示了與內建模組名稱衝突的問題")

print("\n嘗試導入內建的 os 模組:")
try:
    import os
    print("成功導入 os 模組")
    print("當前目錄內容:", os.listdir())
except Exception as e:
    print("導入失敗:", str(e))

print("\n問題說明:")
print("1. 命名模組為 'os.py' 會遮蔽 Python 內建的 os 模組")
print("2. 這會導致無法使用內建模組的功能")

print("\n最佳實踐:")
print("1. 避免使用內建模組的名稱 (如: os, sys, time)")
print("2. 使用更具描述性的名稱 (如: file_operations.py)")
