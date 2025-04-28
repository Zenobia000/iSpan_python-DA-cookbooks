# %% [markdown]
## 📘 M2.3 Pandas 檔案讀寫基礎

本課程將介紹 Pandas 中讀取和寫入各種檔案格式的基本方法。掌握這些操作是數據分析的第一步，可以幫助您快速匯入和匯出數據。

# %% [markdown]
### 🎯 教學目標

- 🔍 了解 Pandas 支援的常見檔案格式
- 📥 掌握讀取 CSV、Excel 和 JSON 檔案的基本方法
- 📤 學習如何將 DataFrame 導出為不同格式
- 🔑 了解基本索引操作與檔案讀寫的關係

# %%
### 🧰 環境設置

# %%
import numpy as np
import pandas as pd
import os

# 設置顯示選項
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 80)
pd.set_option('display.precision', 3)

# 設置數據文件路徑
data_dir = os.path.join('..', 'data')

# %% [markdown]
### 📊 1. CSV 檔案的讀寫

CSV (Comma-Separated Values) 檔案是數據交換的最常見格式之一，幾乎所有數據工具都支援這種格式。

# %%
# 1.1 讀取 titanic.csv 數據集
titanic_file = os.path.join(data_dir, 'titanic.csv')
titanic_data = pd.read_csv(titanic_file)

print(f"Titanic 數據集 (共 {titanic_data.shape[0]} 行, {titanic_data.shape[1]} 列):")
print(titanic_data.head())

# %%
# 1.2 查看數據的基本信息
print("Titanic 數據集的基本信息:")
print(titanic_data.info())

print("\nTitanic 數據集的統計摘要:")
print(titanic_data.describe())

# %%
# 1.3 保存部分 Titanic 數據為新的 CSV 文件
# 選擇幾個關鍵列保存
titanic_subset = titanic_data[['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'Fare']]
titanic_subset.to_csv('titanic_subset.csv', index=False)
print("已將 Titanic 子集保存到 titanic_subset.csv")

# 1.4 使用不同參數保存 CSV
titanic_subset.to_csv('titanic_formatted.csv', index=False, 
                    float_format='%.2f',  # 格式化浮點數為兩位小數
                    na_rep='MISSING')     # 將缺失值表示為 "MISSING"
print("已將格式化的 Titanic 子集保存到 titanic_formatted.csv")

# %%
# 1.5 讀取保存的 CSV 文件
read_back = pd.read_csv('titanic_subset.csv')
print("從 CSV 讀取的數據 (前 5 行):")
print(read_back.head())

# %%
# 解說:
# - CSV 是最常用的數據交換格式，文本格式且容易閱讀
# - `read_csv()` 用於從 CSV 檔案讀取數據，返回 DataFrame
# - `to_csv()` 方法可以將 DataFrame 保存為 CSV 檔案
# - 設置 `index=False` 可以避免將行索引保存到 CSV
# - 可通過 `float_format` 控制數值格式，`na_rep` 設置缺失值的表示
# - 對於基本的數據交換，CSV 是最簡單且兼容性最好的選擇

# %% [markdown]
### 📊 2. 讀取其他 CSV 數據集

# %%
# 2.1 讀取 air-quality.csv 數據集
air_quality_file = os.path.join(data_dir, 'air-quality.csv')
air_quality = pd.read_csv(air_quality_file)

print(f"空氣質量數據集 (共 {air_quality.shape[0]} 行, {air_quality.shape[1]} 列):")
print(air_quality.head())

# 2.2 檢查空氣質量數據的數據類型
print("\n空氣質量數據的數據類型:")
print(air_quality.dtypes)

# %%
# 2.3 讀取 pima-indians-diabetes.csv 數據集
diabetes_file = os.path.join(data_dir, 'pima-indians-diabetes.csv')
diabetes = pd.read_csv(diabetes_file)

print(f"糖尿病數據集 (共 {diabetes.shape[0]} 行, {diabetes.shape[1]} 列):")
print(diabetes.head())

# 檢查是否有缺失值 (NaN)
print("\n糖尿病數據集中每列的缺失值數量:")
print(diabetes.isna().sum())

# %%
# 2.4 使用更多 read_csv 參數
# 假設 pima-indians-diabetes.csv 的第一行不是標題
diabetes_no_header = pd.read_csv(diabetes_file, header=None, 
                               names=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                                      'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'])

print("使用自定義列名讀取糖尿病數據集:")
print(diabetes_no_header.head())

# 使用 skiprows 參數跳過前 5 行
diabetes_skip = pd.read_csv(diabetes_file, skiprows=5)
print("\n跳過前 5 行讀取糖尿病數據集:")
print(diabetes_skip.head())

# %%
# 解說:
# - Pandas 的 `read_csv()` 函數有許多參數可以控制讀取行為
# - `header=None` 表示文件沒有標題行，可以通過 `names` 參數提供列名
# - `skiprows` 參數可以跳過指定數量的行或特定行
# - 其他常用參數包括 `sep`（分隔符）、`dtype`（指定列的數據類型）
# - 靈活運用這些參數可以處理各種格式的 CSV 文件

# %% [markdown]
### 📊 3. Excel 檔案的讀寫

Excel 檔案在商業環境中非常普遍，Pandas 提供了與 Excel 進行交互的功能。

# %%
# 3.1 將數據保存為 Excel 檔案
titanic_subset.to_excel('titanic_subset.xlsx', sheet_name='Titanic', index=False)
print("已將 Titanic 子集保存到 Excel 文件")

# 3.2 創建多個工作表的 Excel 檔案
with pd.ExcelWriter('multiple_datasets.xlsx') as writer:
    titanic_subset.to_excel(writer, sheet_name='Titanic', index=False)
    air_quality.to_excel(writer, sheet_name='Air Quality', index=False)
    diabetes.to_excel(writer, sheet_name='Diabetes', index=False)

print("已創建包含多個數據集的 Excel 檔案")

# %%
# 3.3 從 Excel 檔案讀取數據
excel_data = pd.read_excel('titanic_subset.xlsx')
print("從 Excel 讀取的 Titanic 數據:")
print(excel_data.head())

# 3.4 讀取特定工作表
multi_excel_data = pd.read_excel('multiple_datasets.xlsx', sheet_name='Air Quality')
print("\n從多工作表 Excel 讀取的空氣質量數據:")
print(multi_excel_data.head())

# 3.5 讀取所有工作表
all_sheets = pd.read_excel('multiple_datasets.xlsx', sheet_name=None)
print("\nExcel 檔案中的所有工作表:")
for sheet_name, sheet_data in all_sheets.items():
    print(f"- {sheet_name}: {len(sheet_data)} 行, {len(sheet_data.columns)} 列")

# %%
# 解說:
# - Excel 檔案可以包含多個工作表，適合組織相關的數據
# - `to_excel()` 方法將 DataFrame 保存為 Excel 檔案
# - 使用 `ExcelWriter` 可以創建包含多個工作表的 Excel 檔案
# - `read_excel()` 用於讀取 Excel 檔案的數據
# - 使用 `sheet_name` 參數可以指定讀取特定工作表
# - 設置 `sheet_name=None` 將讀取所有工作表，返回字典
# - 與 CSV 相比，Excel 支持更豐富的格式和多工作表，但文件大小通常更大

# %% [markdown]
### 📊 4. JSON 檔案的讀寫

JSON (JavaScript Object Notation) 是一種輕量級的數據交換格式，廣泛用於 Web 應用和 API。

# %%
# 4.1 將 DataFrame 轉換為 JSON 字符串
json_str = titanic_subset.head().to_json()
print("DataFrame 轉換為 JSON 字符串:")
print(json_str[:200] + "...") # 只顯示前200個字符

# 4.2 寫入 JSON 檔案
titanic_subset.head(20).to_json('titanic_subset.json')
print("\n已將 Titanic 子集保存到 titanic_subset.json")

# 4.3 寫入格式化的 JSON 檔案
titanic_subset.head(20).to_json('titanic_pretty.json', orient='records', indent=4)
print("已將 Titanic 子集保存到易讀格式的 titanic_pretty.json")

# %%
# 4.4 從 JSON 檔案讀取數據
df_from_json = pd.read_json('titanic_subset.json')
print("從 JSON 讀取的數據:")
print(df_from_json.head())

# 4.5 從格式化的 JSON 檔案讀取
df_from_pretty_json = pd.read_json('titanic_pretty.json', orient='records')
print("\n從格式化 JSON 讀取的數據:")
print(df_from_pretty_json.head())

# %%
# 解說:
# - JSON 是 Web 和 API 中常用的數據交換格式
# - `to_json()` 方法將 DataFrame 轉換為 JSON 格式
# - `orient` 參數定義了 JSON 的結構，'records' 使每行成為單獨的對象
# - `indent` 參數使 JSON 更易讀，但會增加文件大小
# - `read_json()` 用於從 JSON 讀取數據到 DataFrame
# - JSON 非常適合與 Web 應用和 API 集成，但對於大型數據集可能效率較低

# %% [markdown]
### 📊 5. 基本索引操作

索引是 Pandas 的重要特性，可以顯著影響數據讀寫和後續處理。

# %%
# 5.1 設置索引
titanic_with_id_index = titanic_subset.set_index('PassengerId')
print("使用 PassengerId 作為索引的 Titanic 數據:")
print(titanic_with_id_index.head())

# 5.2 保存與加載帶索引的檔案
titanic_with_id_index.to_csv('titanic_with_index.csv')
loaded_df = pd.read_csv('titanic_with_index.csv', index_col=0)
print("\n讀取帶索引的 CSV:")
print(loaded_df.head())

# 5.3 重設索引
reset_index_df = titanic_with_id_index.reset_index()
print("\n重設索引後的 DataFrame:")
print(reset_index_df.head())

# %%
# 5.4 設置多級索引
# 使用 Pclass 和 Sex 作為多級索引
multi_index_df = titanic_subset.set_index(['Pclass', 'Sex'])
print("使用多級索引的 Titanic 數據:")
print(multi_index_df.head())

# 5.5 保存與加載帶多級索引的檔案
multi_index_df.to_csv('titanic_multi_index.csv')
loaded_multi_index = pd.read_csv('titanic_multi_index.csv', index_col=[0, 1])
print("\n讀取帶多級索引的 CSV:")
print(loaded_multi_index.head())

# %%
# 解說:
# - `set_index()` 方法將 DataFrame 的一列或多列設為索引
# - 使用索引可以更快速地查找和選擇數據
# - 保存檔案時，索引會默認一起保存
# - 讀取檔案時，可以使用 `index_col` 指定索引列
# - `reset_index()` 將索引轉換回普通列
# - 多級索引可以提供更靈活的數據結構，但可能增加複雜性
# - 適當的索引設置可以更容易地處理時間序列和分層數據

# %% [markdown]
### 📋 6. 總結

# %% [markdown]
#### 6.1 檔案讀寫功能概覽

- **CSV 檔案**:
  - 讀取: `pd.read_csv()`
  - 寫入: `df.to_csv()`
  - 優點: 簡單, 通用, 文本格式
  - 缺點: 不支持多工作表, 不保留格式
  
- **Excel 檔案**:
  - 讀取: `pd.read_excel()`
  - 寫入: `df.to_excel()`
  - 優點: 支持多工作表, 保留格式
  - 缺點: 文件較大, 需要額外套件
  
- **JSON 檔案**:
  - 讀取: `pd.read_json()`
  - 寫入: `df.to_json()`
  - 優點: Web友好, 支持嵌套結構
  - 缺點: 可能較大, 複雜結構難處理

# %% [markdown]
#### 6.2 檔案讀寫注意事項

- 讀取前確認檔案存在並可訪問
- 注意文件編碼 (特別是處理非英文字符)
- 檢查是否需要保存或讀取索引
- 選擇適合數據特性和使用場景的檔案格式
- 處理大型檔案時考慮分批讀取

# %% [markdown]
#### 6.3 下一步學習

- 學習處理更多檔案格式 (SQL, HDF5, Parquet等)
- 探索更多讀寫參數以處理複雜情況
- 理解如何處理缺失值和不同數據類型
- 學習數據清洗和準備技術
- 掌握大型檔案的高效讀寫方法 