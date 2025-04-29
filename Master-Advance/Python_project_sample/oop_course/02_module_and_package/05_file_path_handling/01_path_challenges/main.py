# 主題：檔案路徑處理挑戰總覽

challenges = [
    "不同操作系統的路徑分隔符不同 (Windows: '\\', Unix/Mac: '/')",
    "絕對路徑在不同機器上不同",
    "腳本執行位置與工作目錄可能不同",
    "項目結構在開發環境與部署環境可能不同",
    "Python 模組導入與文件讀取使用不同的路徑機制",
    "Jupyter Notebook 與 .py 檔案的路徑處理邏輯不同"
]

for i, c in enumerate(challenges, 1):
    print(f"{i}. {c}")
