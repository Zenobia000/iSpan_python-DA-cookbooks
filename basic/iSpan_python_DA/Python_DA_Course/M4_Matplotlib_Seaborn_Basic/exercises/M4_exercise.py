# %% [markdown]
# # 📊 M4 Matplotlib 與 Seaborn 練習題

# 本練習題將幫助您鞏固對Matplotlib和Seaborn的理解，通過實際操作來應用所學的數據視覺化技術。完成這些練習題可以增強您處理各類數據視覺化任務的能力。

# %% [markdown]
# ## 🎯 練習內容概述

# 本練習集包含四個部分，對應課程的四個主要主題：
# - 基本Matplotlib操作
# - 常見統計圖表實作
# - Seaborn統計可視化
# - 圖表美化與專業呈現

# %%
# 環境設置
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import warnings

# 忽略警告信息
warnings.filterwarnings('ignore')

# 設置中文字體支持 (如果系統支持)
try:
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

# 設置隨機種子確保結果可重現
np.random.seed(42)

# 設置顯示選項
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 100)

# %% [markdown]
# ## 📊 練習 1: Matplotlib 基礎操作

# %% [markdown]
# ### 練習 1.1: 創建簡單線圖
# 創建一個包含三條線的圖表：
# - sin(x)，用紅色實線表示
# - cos(x)，用藍色虛線表示
# - tan(x)，用綠色點劃線表示，但限制y軸範圍在-2到2之間
# 
# 要求添加標題、軸標籤、圖例和網格。

# %%
# 請在此處編寫您的代碼
# 提示: 使用 plt.plot() 和 plt.ylim()



# %% [markdown]
# ### 練習 1.2: 創建子圖
# 創建一個2行3列的子圖網格，在每個子圖中繪製不同類型的圖表：
# 1. 正弦曲線
# 2. 餘弦曲線 
# 3. 指數曲線 y = 2^x
# 4. 對數曲線 y = log(x)
# 5. 拋物線 y = x²
# 6. 立方曲線 y = x³
# 
# 每個子圖都應有適當的標題。

# %%
# 請在此處編寫您的代碼
# 提示: 使用 plt.subplots() 創建子圖網格



# %% [markdown]
# ### 練習 1.3: 面向對象風格繪圖
# 使用Matplotlib的面向對象接口（使用fig和ax對象，而不是plt函數）創建一個散點圖：
# - 創建50個隨機點
# - 點的大小應該隨機變化
# - 點的顏色應該使用漸變色彩
# - 添加標題、軸標籤和網格
# - 添加一個顏色條(colorbar)

# %%
# 請在此處編寫您的代碼
# 提示: 使用 fig, ax = plt.subplots() 和 ax.scatter()



# %% [markdown]
# ## 📊 練習 2: 常見統計圖表實作

# %% [markdown]
# ### 練習 2.1: 創建並分析數據集
# 創建一個模擬的學生成績數據集，包含以下列：
# - 姓名 (隨機生成，如 'Student_1', 'Student_2'...)
# - 班級 (隨機分配，如 'Class A', 'Class B', 'Class C')
# - 數學分數 (生成0-100之間的隨機分數)
# - 科學分數 (生成0-100之間的隨機分數)
# - 語文分數 (生成0-100之間的隨機分數)
# - 通過情況 (若三科平均分≥60，則為'Pass'，否則為'Fail')
# 
# 創建一個包含30名學生的數據集。

# %%
# 請在此處創建學生成績數據集
# 提示: 使用 np.random.randint() 和 pd.DataFrame()



# %% [markdown]
# ### 練習 2.2: 繪製長條圖比較不同班級的平均分數
# 計算每個班級在三個科目上的平均分數，並創建一個分組長條圖進行比較。
# 要求添加適當的標題、軸標籤和圖例。

# %%
# 請在此處編寫您的代碼



# %% [markdown]
# ### 練習 2.3: 繪製多個分佈圖
# 使用您創建的數據集，在一個2x2的子圖布局中繪製四個分佈圖：
# 1. 數學分數的直方圖
# 2. 科學分數的直方圖
# 3. 語文分數的直方圖
# 4. 所有學生平均分數的直方圖

# %%
# 請在此處編寫您的代碼



# %% [markdown]
# ### 練習 2.4: 創建散點矩陣
# 使用pandas的scatter_matrix函數，創建一個三科成績的散點矩陣圖，
# 使用"通過情況"作為點的顏色區分。

# %%
# 請在此處編寫您的代碼
# 提示: 使用 pd.plotting.scatter_matrix()



# %% [markdown]
# ## 📊 練習 3: Seaborn 統計可視化

# %% [markdown]
# ### 練習 3.1: 載入並探索Titanic數據集
# 使用seaborn載入Titanic數據集，並顯示前幾行數據。

# %%
# 請在此處編寫您的代碼
# 提示: 使用 sns.load_dataset('titanic')



# %% [markdown]
# ### 練習 3.2: 創建箱形圖
# 使用Titanic數據集，創建一個箱形圖顯示不同艙位(class)的年齡(age)分佈。
# 要求使用不同的顏色標識男女乘客，並添加適當的標題和標籤。

# %%
# 請在此處編寫您的代碼
# 提示: 使用 sns.boxplot()



# %% [markdown]
# ### 練習 3.3: 創建小提琴圖
# 使用Titanic數據集，創建一個小提琴圖比較存活(survived)與非存活乘客的年齡分佈。
# 要求按性別(sex)分開展示。

# %%
# 請在此處編寫您的代碼
# 提示: 使用 sns.violinplot()



# %% [markdown]
# ### 練習 3.4: 創建計數圖
# 創建一個計數圖，展示不同艙位(class)、性別(sex)和存活狀態(survived)的乘客數量。

# %%
# 請在此處編寫您的代碼
# 提示: 使用 sns.countplot()



# %% [markdown]
# ### 練習 3.5: 創建配對圖
# 使用Titanic數據集的數值變量（如age, fare, survived等）創建一個配對圖，
# 使用性別(sex)區分顏色。

# %%
# 請在此處編寫您的代碼
# 提示: 使用 sns.pairplot()



# %% [markdown]
# ### 練習 3.6: 創建熱圖
# 計算Titanic數據集中數值變量之間的相關性，並使用熱圖展示。
# 要求在熱圖上顯示相關係數值。

# %%
# 請在此處編寫您的代碼
# 提示: 使用 titanic.corr() 和 sns.heatmap()



# %% [markdown]
# ## 📊 練習 4: 圖表美化與專業呈現

# %% [markdown]
# ### 練習 4.1: 改進原始圖表
# 以下代碼創建了一個基本折線圖。請改進這個圖表，使其具有專業的外觀，包括：
# - 更好的顏色方案
# - 適當的標題和標籤（包括字體大小和間距）
# - 自定義軸刻度和網格
# - 背景和邊框的優化
# - 添加數據點標記

# %%
# 原始圖表代碼
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-x/5)

plt.figure(figsize=(8, 5))
plt.plot(x, y)
plt.title('Sample Plot')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

# %%
# 請在此處添加您的改進版本



# %% [markdown]
# ### 練習 4.2: 創建帶有註釋的圖表
# 使用與練習4.1相同的數據，創建一個帶有以下元素的圖表：
# - 在最大值和最小值處添加標註（使用箭頭和文本）
# - 添加一個說明數據趨勢的文本框
# - 使用數學公式（使用LaTeX語法）標註函數表達式
# - 添加一個自定義圖例

# %%
# 請在此處編寫您的代碼



# %% [markdown]
# ### 練習 4.3: 創建多子圖布局
# 創建一個複雜的圖表，包含不同類型的子圖，要求：
# - 使用GridSpec創建非均勻的佈局（至少4個子圖）
# - 每個子圖展示不同類型的圖表（如直方圖、散點圖、折線圖等）
# - 子圖之間有適當的間距
# - 添加整體標題和每個子圖的標題
# - 確保坐標軸標籤不重疊

# %%
# 請在此處編寫您的代碼
# 提示: 使用 GridSpec 或 plt.subplot2grid



# %% [markdown]
# ### 練習 4.4: 自定義風格
# 創建一個自定義的Matplotlib/Seaborn風格並應用它：
# - 定義自己的顏色方案
# - 自定義背景、網格和字體
# - 應用此風格到一個展示Titanic生存率的圖表上
# - 按性別分組並用不同顏色區分艙位

# %%
# 請在此處編寫您的代碼



# %% [markdown]
# ## 📋 提交指南

# 完成所有練習後：
# 1. 檢查每個圖表是否具有適當的標題、標籤和圖例
# 2. 確保代碼清晰易讀，並有必要的註釋
# 3. 保存您的結果 