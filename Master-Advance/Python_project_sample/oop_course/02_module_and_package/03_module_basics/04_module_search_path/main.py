import sys

# 1. 簡介
# sys 是 Python 的標準庫之一，負責提供一組與 Python 解譯器 本身及其運行環境有關的功能。

# 可以控制程式的行為

# 可以存取與 Python 執行環境、系統互動的資訊

# 常見用途：取得版本資訊、操作執行路徑、讀取參數、強制退出程式、設定標準輸入輸出等。


print("當前 Python 搜索路徑:")
for path in sys.path:
    print("-", path)


