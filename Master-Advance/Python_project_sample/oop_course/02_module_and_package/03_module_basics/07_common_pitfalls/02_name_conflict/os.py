# 錯誤示例：與內建模組名稱衝突
def listdir(path="."):
    return "這是自定義的 listdir 函數"

def mkdir(path):
    return "這是自定義的 mkdir 函數"
