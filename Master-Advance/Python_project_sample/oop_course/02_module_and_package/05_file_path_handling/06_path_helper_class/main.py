# 主題：Python 模組導入與文件讀取使用不同的路徑機制

# 兩種導入方式的比較:

# 方式一: 直接導入已實體化的物件
# 優點:
# - 程式碼簡潔,直接使用現成的實體
# - 確保整個專案只有一個實體(Singleton模式)
# - 適合大多數使用情境
# 缺點:
# - 較難進行單元測試(因為無法替換實體)
# - 較難客製化實體參數

# 方式二: 導入類別自行實體化
# 優點:
# - 靈活度高,可自訂實體參數
# - 容易進行單元測試(可替換測試用實體)
# - 可建立多個不同配置的實體
# 缺點:
# - 可能產生多餘的實體
# - 程式碼較冗長
# - 需要自行管理實體生命週期


from path_helper import project_paths

print("資料檔案:", project_paths.get_data_file("test.txt"))
print("輸出檔案:", project_paths.get_output_file("result.csv"))


## 以下是另一種寫法
## 導入藍圖後，再實體化

from path_helper import ProjectPaths

project_paths = ProjectPaths()

print("資料檔案:", project_paths.get_data_file("test.txt"))
print("輸出檔案:", project_paths.get_output_file("result.csv"))



