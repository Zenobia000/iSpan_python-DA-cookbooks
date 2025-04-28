# %% [markdown]
## 📘 M2.2 Pandas 基礎資料選取與索引

本教學將介紹 Pandas 中用於選取和索引數據的基本方法，這些是數據分析的核心技能。
我們將從簡單的列和行選取開始，然後學習更精確的索引技術，幫助您從數據中提取所需信息。

# %% [markdown]
### 🎯 教學目標

- 🔍 了解選取 DataFrame 列和行的基本方法
- 📌 掌握 `.loc[]` 和 `.iloc[]` 的基本用法
- 🔎 學習簡單的條件篩選技巧
- 💻 練習常見的數據選取操作

# %%
### 🧰 環境設置

# %%
import numpy as np
import pandas as pd

# 設置顯示選項
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 80)
pd.set_option('display.precision', 3)

# %% [markdown]
### 📊 1. 創建示例數據

# %%
# 創建一個員工數據的示例DataFrame
employees = pd.DataFrame({
    'ID': [101, 102, 103, 104, 105, 106, 107],
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace'],
    'Department': ['HR', 'IT', 'Finance', 'IT', 'Marketing', 'HR', 'Finance'],
    'Salary': [72000, 78000, 83000, 85000, 70000, 75000, 88000],
    'JoinDate': ['2019-05-21', '2018-12-10', '2020-01-15', '2017-08-30', 
                 '2021-03-02', '2019-09-11', '2020-07-28'],
    'Gender': ['F', 'M', 'M', 'M', 'F', 'M', 'F'],
    'Education': ['Masters', 'Bachelors', 'PhD', 'Masters', 'Bachelors', 'Bachelors', 'PhD']
})

# 將JoinDate列轉換為日期類型
employees['JoinDate'] = pd.to_datetime(employees['JoinDate'])

print("員工數據示例:")
print(employees)

# %%
# 解說：
# - 我們創建了一個包含7名員工信息的DataFrame，有7列不同的屬性
# - 這個數據集包含了不同類型的數據：數值型、字符型和日期型
# - 我們將JoinDate列轉換為日期類型，以便後續可以進行日期相關操作
# - 這個簡單的數據集將用於展示各種選取和索引方法

# %% [markdown]
### 📋 2. 基本列選取

# %%
# 2.1 選取單一列 (返回Series)
name_column = employees['Name']
print("選取Name列 (Series):")
print(name_column)
print(f"類型: {type(name_column)}")

# 2.2 選取多列 (返回DataFrame)
selected_columns = employees[['Name', 'Department', 'Salary']]
print("\n選取多列 (DataFrame):")
print(selected_columns)
print(f"類型: {type(selected_columns)}")

# 2.3 選取列的另一種方法 (使用點符號)
dept_column = employees.Department
print("\n使用點符號選取Department列:")
print(dept_column)

# %%
# 解說：
# - 單列選取: 使用單括號 `df['列名']` 返回一個Series對象
# - 多列選取: 使用雙括號 `df[['列名1', '列名2']]` 包含一個列名列表，返回DataFrame
# - 點符號選取: `df.列名` 適用於簡單列名(不包含空格或特殊字符)
# - 選取列是數據分析的基本操作，可以專注於感興趣的變量

# %% [markdown]
### 📋 3. 基本行選取

# %%
# 3.1 使用索引切片選取行 (基於位置)
first_three_rows = employees[0:3]
print("選取前三行:")
print(first_three_rows)

# 3.2 使用條件選取行
it_department = employees[employees['Department'] == 'IT']
print("\n選取IT部門的員工:")
print(it_department)

high_salary = employees[employees['Salary'] > 80000]
print("\n選取薪資超過80000的員工:")
print(high_salary)

# %%
# 解說：
# - 使用切片 `df[start:end]` 可以選取特定範圍的行
# - 切片遵循Python的規則，包含起始索引但不包含結束索引
# - 使用條件表達式 `df[條件]` 可以根據特定條件篩選行
# - 條件篩選返回所有滿足條件的行，是數據分析中非常實用的功能

# %% [markdown]
### 📋 4. 使用 .loc[] 和 .iloc[] 進行精確索引

# %%
# 4.1 基於標籤的索引 (.loc)
# 選取ID為105的行
row_105 = employees.loc[employees['ID'] == 105]
print("選取ID為105的行:")
print(row_105)

# 選取索引為2的行 (第3行，因為索引從0開始)
row_2 = employees.loc[2]
print("\n選取索引為2的行:")
print(row_2)

# 選取索引2到4的行和特定列
subset = employees.loc[2:4, ['Name', 'Department', 'Salary']]
print("\n選取索引2到4的行和特定列:")
print(subset)

# %%
# 解說：
# - `.loc[]` 用於基於標籤(索引)的選取
# - 可以使用單個索引值、索引範圍或索引列表
# - 可以同時指定行和列，格式為 `.loc[行選擇, 列選擇]`
# - 使用`.loc[]`時，索引範圍是閉區間，即包含結束索引

# %%
# 4.2 基於位置的索引 (.iloc)
# 選取第一行 (索引為0)
first_row = employees.iloc[0]
print("選取第一行:")
print(first_row)

# 選取前三行和第1、3、5列 (位置從0開始)
subset_iloc = employees.iloc[0:3, [0, 2, 4]]
print("\n選取前三行和第1、3、5列:")
print(subset_iloc)

# 使用負索引選取最後一行
last_row = employees.iloc[-1]
print("\n選取最後一行:")
print(last_row)

# %%
# 解說：
# - `.iloc[]` 用於基於位置的選取，與Python列表索引類似
# - 位置索引從0開始，可以使用單個位置、位置範圍或位置列表
# - 可以同時指定行和列的位置，格式為 `.iloc[行位置, 列位置]`
# - 使用`.iloc[]`時，位置範圍是半開區間，即不包含結束位置
# - 負索引表示從末尾開始計數，`-1`表示最後一個元素

# %% [markdown]
### 📋 5. 簡單的條件篩選

# %%
# 5.1 單一條件篩選
female_employees = employees[employees['Gender'] == 'F']
print("女性員工:")
print(female_employees)

# 5.2 多條件篩選 (使用 & 和 |)
# &: 與操作，要求同時滿足多個條件
hr_female = employees[(employees['Department'] == 'HR') & (employees['Gender'] == 'F')]
print("\nHR部門的女性員工:")
print(hr_female)

# |: 或操作，滿足任一條件即可
hr_or_finance = employees[(employees['Department'] == 'HR') | (employees['Department'] == 'Finance')]
print("\nHR或Finance部門的員工:")
print(hr_or_finance)

# 5.3 使用 isin() 進行多值匹配
selected_depts = employees[employees['Department'].isin(['HR', 'IT'])]
print("\nHR或IT部門的員工:")
print(selected_depts)

# %%
# 解說：
# - 單一條件篩選: 使用比較運算符如 ==, >, <, >=, <=, != 等
# - 多條件篩選: 使用 & (與)和 | (或)連接多個條件，記得用括號包裹每個條件
# - `.isin()` 方法用於檢查值是否在給定列表中，適合多值匹配
# - 這些條件篩選方法可以靈活組合，處理各種數據分析需求

# %% [markdown]
### 📊 6. 基礎實例：員工數據分析

# %%
# 6.1 計算各部門的平均薪資
dept_avg_salary = employees.groupby('Department')['Salary'].mean()
print("各部門平均薪資:")
print(dept_avg_salary)

# 6.2 找出薪資最高的員工
highest_salary = employees.loc[employees['Salary'].idxmax()]
print("\n薪資最高的員工:")
print(highest_salary)

# 6.3 統計各學歷層級的員工人數
education_count = employees['Education'].value_counts()
print("\n各學歷層級的員工人數:")
print(education_count)

# %%
# 解說：
# - 通過簡單的選取方法，我們可以執行基本的數據分析任務
# - `groupby()` 用於分組統計，我們會在後續課程中深入學習
# - `.idxmax()` 返回最大值所在的索引位置
# - `.value_counts()` 計算每個唯一值出現的次數
# - 這些基本操作是更複雜分析的基礎

# %% [markdown]
### 📋 7. 總結

# %% [markdown]
#### 7.1 選取和索引的方法概覽
- **列選取**:
  - 單列: `df['列名']` (返回Series)
  - 多列: `df[['列名1', '列名2']]` (返回DataFrame)
  
- **行選取**:
  - 切片: `df[start:end]`
  - 條件: `df[df['列名'] > 值]`
  
- **精確索引**:
  - `.loc[行標籤, 列標籤]` - 基於標籤索引
  - `.iloc[行位置, 列位置]` - 基於位置索引
  
- **條件篩選**:
  - 單條件: `df[df['列名'] == 值]`
  - 多條件與: `df[(條件1) & (條件2)]`
  - 多條件或: `df[(條件1) | (條件2)]`
  - 多值匹配: `df[df['列名'].isin([值1, 值2])]`

# %% [markdown]
#### 7.2 選取與索引時的注意事項
- `.loc[]` 的範圍是閉區間，包含結束索引
- `.iloc[]` 的範圍是半開區間，不包含結束位置
- 使用條件篩選時，多個條件要用括號括起來
- 點符號 (`df.列名`) 只適用於列名不含空格或特殊字符的情況
- 選取單列返回Series，選取多列或行返回DataFrame

# %% [markdown]
#### 7.3 下一步學習
- 更多資料篩選技巧
- 數據分組與聚合
- 處理缺失值
- 數據轉換與計算
- 透視表與交叉表 