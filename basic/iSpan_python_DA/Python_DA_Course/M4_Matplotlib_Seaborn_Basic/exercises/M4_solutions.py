# %% [markdown]
# # 📊 M4 Matplotlib 與 Seaborn 練習題解答

# 本文件提供 M4 Matplotlib 與 Seaborn 練習題的解答。在解答中，我們展示了如何使用 Matplotlib 和 Seaborn 
# 創建各類數據視覺化圖表，以及如何通過自定義設置提升圖表的專業性與可讀性。

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
# 解答 1.1
x = np.linspace(0, 2*np.pi, 1000)  # 創建從0到2π的1000個等分點

plt.figure(figsize=(10, 6))  # 設置圖形大小

# 繪製三條不同的線
plt.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')       # 紅色實線
plt.plot(x, np.cos(x), 'b--', linewidth=2, label='cos(x)')      # 藍色虛線
plt.plot(x, np.tan(x), 'g-.', linewidth=2, label='tan(x)')      # 綠色點劃線

# 設置y軸範圍限制
plt.ylim(-2, 2)

# 添加標題和軸標籤
plt.title('三角函數圖表', fontsize=16)
plt.xlabel('x (弧度)', fontsize=12)
plt.ylabel('y 值', fontsize=12)

# 添加網格和圖例
plt.grid(True, alpha=0.3)
plt.legend(loc='upper right', fontsize=12)

plt.tight_layout()
plt.show()

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
# 解答 1.2
# 創建2行3列的子圖網格
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# 將子圖陣列展平，便於循環訪問
axes = axes.flatten()

# 創建x值陣列
x1 = np.linspace(0, 2*np.pi, 100)  # 用於三角函數
x2 = np.linspace(0, 4, 100)         # 用於指數函數
x3 = np.linspace(0.1, 10, 100)      # 用於對數函數
x4 = np.linspace(-3, 3, 100)        # 用於冪函數

# 1. 正弦曲線
axes[0].plot(x1, np.sin(x1), 'r-', linewidth=2)
axes[0].set_title('正弦函數 (sin(x))', fontsize=14)
axes[0].set_xlabel('x')
axes[0].set_ylabel('sin(x)')
axes[0].grid(True, alpha=0.3)

# 2. 餘弦曲線
axes[1].plot(x1, np.cos(x1), 'b-', linewidth=2)
axes[1].set_title('餘弦函數 (cos(x))', fontsize=14)
axes[1].set_xlabel('x')
axes[1].set_ylabel('cos(x)')
axes[1].grid(True, alpha=0.3)

# 3. 指數曲線 y = 2^x
axes[2].plot(x2, 2**x2, 'g-', linewidth=2)
axes[2].set_title('指數函數 (2^x)', fontsize=14)
axes[2].set_xlabel('x')
axes[2].set_ylabel('2^x')
axes[2].grid(True, alpha=0.3)

# 4. 對數曲線 y = log(x)
axes[3].plot(x3, np.log(x3), 'm-', linewidth=2)
axes[3].set_title('對數函數 (log(x))', fontsize=14)
axes[3].set_xlabel('x')
axes[3].set_ylabel('log(x)')
axes[3].grid(True, alpha=0.3)

# 5. 拋物線 y = x²
axes[4].plot(x4, x4**2, 'c-', linewidth=2)
axes[4].set_title('拋物線 (x²)', fontsize=14)
axes[4].set_xlabel('x')
axes[4].set_ylabel('x²')
axes[4].grid(True, alpha=0.3)

# 6. 立方曲線 y = x³
axes[5].plot(x4, x4**3, 'y-', linewidth=2)
axes[5].set_title('立方曲線 (x³)', fontsize=14)
axes[5].set_xlabel('x')
axes[5].set_ylabel('x³')
axes[5].grid(True, alpha=0.3)

# 調整子圖間距
plt.tight_layout()

# 添加總標題
fig.suptitle('數學函數圖表集', fontsize=20, y=1.02)
plt.show()

# %% [markdown]
# ### 練習 1.3: 面向對象風格繪圖
# 使用Matplotlib的面向對象接口（使用fig和ax對象，而不是plt函數）創建一個散點圖：
# - 創建50個隨機點
# - 點的大小應該隨機變化
# - 點的顏色應該使用漸變色彩
# - 添加標題、軸標籤和網格
# - 添加一個顏色條(colorbar)

# %%
# 解答 1.3
# 創建數據
n_points = 50
x = np.random.rand(n_points) * 10  # 範圍 0-10 的隨機 x 值
y = np.random.rand(n_points) * 10  # 範圍 0-10 的隨機 y 值
sizes = np.random.rand(n_points) * 300 + 50  # 範圍 50-350 的隨機點大小
colors = np.random.rand(n_points)  # 範圍 0-1 的隨機值用於顏色映射

# 創建圖形和軸對象
fig, ax = plt.subplots(figsize=(10, 8))

# 使用散點圖函數
scatter = ax.scatter(x, y, s=sizes, c=colors, cmap='viridis', 
                    alpha=0.7, edgecolors='black', linewidths=0.5)

# 添加標題和軸標籤
ax.set_title('隨機點散點圖', fontsize=16)
ax.set_xlabel('X 軸', fontsize=14)
ax.set_ylabel('Y 軸', fontsize=14)

# 添加網格
ax.grid(True, linestyle='--', alpha=0.6)

# 設置軸範圍
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# 添加顏色條
cbar = fig.colorbar(scatter, ax=ax, label='顏色值')
cbar.set_label('顏色值', fontsize=12)

# 添加額外的美化元素
ax.set_facecolor('#f8f9fa')  # 設置背景顏色
for spine in ax.spines.values():
    spine.set_linewidth(1.5)  # 加粗邊框線

plt.tight_layout()
plt.show()

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
# 解答 2.1
# 設置學生數量
n_students = 30

# 創建各列數據
student_names = [f'Student_{i+1}' for i in range(n_students)]
classes = np.random.choice(['Class A', 'Class B', 'Class C'], size=n_students)
math_scores = np.random.randint(0, 101, size=n_students)  # 0-100之間的隨機分數
science_scores = np.random.randint(0, 101, size=n_students)
language_scores = np.random.randint(0, 101, size=n_students)

# 計算平均分
average_scores = (math_scores + science_scores + language_scores) / 3

# 判斷通過情況
pass_status = ['Pass' if avg >= 60 else 'Fail' for avg in average_scores]

# 創建DataFrame
student_data = pd.DataFrame({
    '姓名': student_names,
    '班級': classes,
    '數學': math_scores,
    '科學': science_scores,
    '語文': language_scores,
    '平均分': average_scores,
    '通過情況': pass_status
})

# 顯示數據
print("學生成績數據集預覽:")
print(student_data.head(10))

# 顯示基本統計資訊
print("\n基本統計資訊:")
print(student_data[['數學', '科學', '語文', '平均分']].describe())

# 顯示通過率
pass_rate = student_data['通過情況'].value_counts(normalize=True)
print("\n通過率:")
print(pass_rate)

# 顯示各班級人數
class_counts = student_data['班級'].value_counts()
print("\n各班級人數:")
print(class_counts)

# %% [markdown]
# ### 練習 2.2: 繪製長條圖比較不同班級的平均分數
# 計算每個班級在三個科目上的平均分數，並創建一個分組長條圖進行比較。
# 要求添加適當的標題、軸標籤和圖例。

# %%
# 解答 2.2
# 計算每個班級在各科目的平均分數
class_averages = student_data.groupby('班級')[['數學', '科學', '語文']].mean().reset_index()

# 重塑數據以便於繪圖
class_averages_melted = pd.melt(class_averages, 
                               id_vars='班級',
                               value_vars=['數學', '科學', '語文'],
                               var_name='科目',
                               value_name='平均分數')

print("重塑後的數據:")
print(class_averages_melted)

# 設置顏色
colors = ['#3498db', '#2ecc71', '#e74c3c']

# 創建分組長條圖
plt.figure(figsize=(12, 7))

# 計算長條的位置
classes = class_averages['班級'].unique()
subjects = ['數學', '科學', '語文']
n_classes = len(classes)
n_subjects = len(subjects)
width = 0.25  # 長條寬度
indices = np.arange(n_classes)  # 班級位置

# 繪製長條圖
for i, subject in enumerate(subjects):
    # 獲取特定科目每個班級的平均分
    scores = class_averages[subject].values
    
    # 繪製長條
    bars = plt.bar(indices + (i - 1) * width, scores, width, 
                  label=subject, color=colors[i], edgecolor='black', linewidth=1)
    
    # 添加數值標籤
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}', ha='center', va='bottom', fontsize=10)

# 添加標題和軸標籤
plt.title('各班級在不同科目的平均分數比較', fontsize=16, pad=15)
plt.xlabel('班級', fontsize=14, labelpad=10)
plt.ylabel('平均分數', fontsize=14, labelpad=10)

# 設置x軸刻度標籤
plt.xticks(indices, classes, fontsize=12)

# 添加網格線
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 添加圖例
plt.legend(fontsize=12, title='科目', title_fontsize=13)

# 調整佈局
plt.tight_layout()

# 顯示圖形
plt.show()

# %% [markdown]
# ### 練習 2.3: 繪製多個分佈圖
# 使用您創建的數據集，在一個2x2的子圖布局中繪製四個分佈圖：
# 1. 數學分數的直方圖
# 2. 科學分數的直方圖
# 3. 語文分數的直方圖
# 4. 所有學生平均分數的直方圖

# %%
# 解答 2.3
# 創建2x2的子圖佈局
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 展平axes數組以便迭代
axes = axes.flatten()

# 設置顏色
colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6']

# 1. 數學分數的直方圖
axes[0].hist(student_data['數學'], bins=10, color=colors[0], alpha=0.7, edgecolor='black')
axes[0].set_title('數學分數分佈', fontsize=14)
axes[0].set_xlabel('分數', fontsize=12)
axes[0].set_ylabel('學生人數', fontsize=12)
axes[0].grid(True, linestyle='--', alpha=0.6)
axes[0].axvline(x=student_data['數學'].mean(), color='red', linestyle='--', 
               label=f'平均分: {student_data["數學"].mean():.1f}')
axes[0].legend()

# 2. 科學分數的直方圖
axes[1].hist(student_data['科學'], bins=10, color=colors[1], alpha=0.7, edgecolor='black')
axes[1].set_title('科學分數分佈', fontsize=14)
axes[1].set_xlabel('分數', fontsize=12)
axes[1].set_ylabel('學生人數', fontsize=12)
axes[1].grid(True, linestyle='--', alpha=0.6)
axes[1].axvline(x=student_data['科學'].mean(), color='red', linestyle='--', 
               label=f'平均分: {student_data["科學"].mean():.1f}')
axes[1].legend()

# 3. 語文分數的直方圖
axes[2].hist(student_data['語文'], bins=10, color=colors[2], alpha=0.7, edgecolor='black')
axes[2].set_title('語文分數分佈', fontsize=14)
axes[2].set_xlabel('分數', fontsize=12)
axes[2].set_ylabel('學生人數', fontsize=12)
axes[2].grid(True, linestyle='--', alpha=0.6)
axes[2].axvline(x=student_data['語文'].mean(), color='red', linestyle='--', 
               label=f'平均分: {student_data["語文"].mean():.1f}')
axes[2].legend()

# 4. 平均分數的直方圖
axes[3].hist(student_data['平均分'], bins=10, color=colors[3], alpha=0.7, edgecolor='black')
axes[3].set_title('平均分數分佈', fontsize=14)
axes[3].set_xlabel('分數', fontsize=12)
axes[3].set_ylabel('學生人數', fontsize=12)
axes[3].grid(True, linestyle='--', alpha=0.6)
axes[3].axvline(x=student_data['平均分'].mean(), color='red', linestyle='--', 
               label=f'平均分: {student_data["平均分"].mean():.1f}')
axes[3].axvline(x=60, color='green', linestyle='-', 
               label='及格線: 60')
axes[3].legend()

# 添加總標題
plt.suptitle('學生各科目分數分佈', fontsize=18, y=0.98)

# 調整子圖間距
plt.tight_layout()
plt.subplots_adjust(top=0.9)

# 顯示圖形
plt.show()

# %% [markdown]
# ### 練習 2.4: 創建散點矩陣
# 使用pandas的scatter_matrix函數，創建一個三科成績的散點矩陣圖，
# 使用"通過情況"作為點的顏色區分。

# %%
# 解答 2.4
# 從pandas導入scatter_matrix (如果需要)
from pandas.plotting import scatter_matrix

# 創建散點矩陣
# 只選擇需要的列：數學、科學、語文
columns_to_plot = ['數學', '科學', '語文']

# 基於"通過情況"創建顏色映射
colors = {'Pass': 'green', 'Fail': 'red'}
color_values = [colors[status] for status in student_data['通過情況']]

# 繪製散點矩陣
fig, axes = plt.subplots(figsize=(12, 10))
scatter_matrix = pd.plotting.scatter_matrix(
    student_data[columns_to_plot], 
    figsize=(12, 10),
    diagonal='kde',  # 對角線上顯示核密度估計
    marker='o',
    s=80,  # 點的大小
    alpha=0.8,  # 透明度
    c=color_values,  # 基於通過狀態設置顏色
    hist_kwds={'bins': 15},  # 直方圖的bins數
    range_padding=0.1  # 坐標軸範圍的填充
)

# 美化散點矩陣
for ax in scatter_matrix.flatten():
    ax.xaxis.label.set_rotation(45)
    ax.yaxis.label.set_rotation(0)
    ax.yaxis.label.set_ha('right')
    
    # 設置網格
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # 美化刻度標籤
    ax.tick_params(axis='both', labelsize=9)

# 添加圖例（手動添加，因為scatter_matrix沒有直接支持圖例）
import matplotlib.patches as mpatches
pass_patch = mpatches.Patch(color='green', label='通過')
fail_patch = mpatches.Patch(color='red', label='不通過')
plt.legend(handles=[pass_patch, fail_patch], 
           loc='upper right', 
           bbox_to_anchor=(0.95, 0.95),
           fontsize=12)

# 添加總標題
plt.suptitle('學生成績散點矩陣 (按通過情況標色)', fontsize=16, y=0.98)

# 調整佈局
plt.tight_layout()
plt.subplots_adjust(top=0.95)

# 顯示圖形
plt.show()

# %% [markdown]
# ## 📊 練習 3: Seaborn 統計可視化

# %% [markdown]
# ### 練習 3.1: 載入並探索Titanic數據集
# 使用seaborn載入Titanic數據集，並顯示前幾行數據。

# %%
# 解答 3.1
# 載入Titanic數據集
titanic = sns.load_dataset('titanic')

# 顯示前10行數據
print("Titanic數據集前10行:")
print(titanic.head(10))

# 顯示數據集基本資訊
print("\nTitanic數據集資訊:")
print(titanic.info())

# 顯示數值型列的基本統計資訊
print("\nTitanic數據集統計摘要:")
print(titanic.describe())

# 顯示各類別型列的分布情況
print("\n分類變量值統計:")
for column in ['survived', 'pclass', 'sex', 'embarked']:
    if column in titanic.columns:
        print(f"\n{column} 值計數:")
        print(titanic[column].value_counts())
        print(f"{column} 百分比:")
        print(titanic[column].value_counts(normalize=True).round(4) * 100)

# %% [markdown]
# ### 練習 3.2: 創建箱形圖
# 使用Titanic數據集，創建一個箱形圖顯示不同艙位(class)的年齡(age)分佈。
# 要求使用不同的顏色標識男女乘客，並添加適當的標題和標籤。

# %%
# 解答 3.2
# 設置圖形大小
plt.figure(figsize=(12, 7))

# 使用seaborn創建箱形圖
ax = sns.boxplot(x='pclass', y='age', hue='sex', data=titanic, 
               palette={'male': 'blue', 'female': 'pink'},
               linewidth=1)

# 添加標題和標籤
plt.title('不同艙位的年齡分佈 (按性別分組)', fontsize=16, pad=15)
plt.xlabel('艙位等級', fontsize=14, labelpad=10)
plt.ylabel('年齡', fontsize=14, labelpad=10)

# 自定義x軸刻度標籤
plt.xticks([0, 1, 2], ['一等艙', '二等艙', '三等艙'], fontsize=12)

# 添加網格
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# 調整圖例
plt.legend(title='性別', title_fontsize=12, fontsize=10)

# 美化箱形圖
for i, box in enumerate(ax.artists):
    # 箱體填充顏色調整半透明
    box.set_alpha(0.7)
    
    # 設置邊框顏色
    box.set_edgecolor('black')
    
    # 美化小鬍鬚和離群點
    for j in range(6*i, 6*(i+1)):
        ax.lines[j].set_color('black')
        ax.lines[j].set_linewidth(1.2)

# 添加均值點
for i, pclass in enumerate([1, 2, 3]):
    for j, gender in enumerate(['male', 'female']):
        # 計算特定艙位和性別的平均年齡
        mean_age = titanic[(titanic['pclass'] == pclass) & 
                           (titanic['sex'] == gender)]['age'].mean()
        
        # 檢查是否有有效的平均值
        if not np.isnan(mean_age):
            plt.scatter(i + (j*0.25 - 0.1), mean_age, marker='D', 
                       s=100, color='red', edgecolor='black', zorder=10)
            plt.text(i + (j*0.25 - 0.1), mean_age + 1, f'均值: {mean_age:.1f}', 
                    ha='center', va='bottom', fontsize=9, color='red')

# 調整佈局
plt.tight_layout()

# 顯示圖形
plt.show()

# %% [markdown]
# ### 練習 3.3: 創建小提琴圖
# 使用Titanic數據集，創建一個小提琴圖比較存活(survived)與非存活乘客的年齡分佈。
# 要求按性別(sex)分開展示。

# %%
# 解答 3.3
# 設置圖形大小
plt.figure(figsize=(12, 8))

# 使用seaborn創建小提琴圖
# x: survived, y: age, 按性別分開展示
ax = sns.violinplot(x='survived', y='age', hue='sex', data=titanic,
                   split=True,  # 分開顯示性別
                   inner='quartile',  # 在小提琴內部顯示分位數
                   palette={'male': 'lightblue', 'female': 'lightpink'},
                   linewidth=1, edgecolor='black')

# 添加標題和標籤
plt.title('泰坦尼克號存活與非存活乘客的年齡分佈 (按性別分割)', fontsize=16, pad=15)
plt.xlabel('存活狀態', fontsize=14, labelpad=10)
plt.ylabel('年齡', fontsize=14, labelpad=10)

# 自定義x軸標籤
plt.xticks([0, 1], ['未存活', '存活'], fontsize=12)

# 添加網格
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# 優化圖例
plt.legend(title='性別', title_fontsize=12, fontsize=10, loc='upper right')

# 添加統計註釋
# 計算並添加存活和非存活乘客的平均年齡
for survived in [0, 1]:
    for sex in ['male', 'female']:
        # 計算特定存活狀態和性別的平均年齡
        mean_age = titanic[(titanic['survived'] == survived) & 
                          (titanic['sex'] == sex)]['age'].mean()
        
        # 計算位置
        x_pos = survived
        # 男性在左側，女性在右側
        x_offset = -0.2 if sex == 'male' else 0.2
        
        # 添加均值點和標籤
        if not np.isnan(mean_age):
            plt.scatter(x_pos + x_offset, mean_age, color='red', s=60, zorder=5, edgecolor='black')
            plt.text(x_pos + x_offset, mean_age - 3, f'均值\n{mean_age:.1f}', 
                    ha='center', fontsize=9, color='black')

# 調整佈局
plt.tight_layout()

# 顯示圖形
plt.show()

# %% [markdown]
# ### 練習 3.4: 創建計數圖
# 創建一個計數圖，展示不同艙位(class)、性別(sex)和存活狀態(survived)的乘客數量。

# %%
# 解答 3.4
# 計算不同艙位、性別和存活狀態的乘客數量
# 首先將 pclass 轉換為分類型變量以便排序
titanic['pclass'] = titanic['pclass'].astype(str)

# 設置風格
sns.set_style("whitegrid")
plt.figure(figsize=(15, 8))

# 使用factorplot (現已更名為catplot) 創建多面板圖
g = sns.catplot(
    data=titanic,
    x="pclass", hue="survived", col="sex",
    kind="count", palette=["#FF5A5F", "#2ECC71"],
    height=7, aspect=0.8, legend=True
)

# 設置標題和標籤
g.fig.suptitle('泰坦尼克號乘客數量 (按艙位、性別和存活狀態分組)', fontsize=16, y=1.05)
g.set_axis_labels("艙位等級", "乘客數量")
g.set_xticklabels(['一等艙', '二等艙', '三等艙'])

# 設置每個子圖的標題
g.set_titles("{col_name}", fontsize=14)

# 添加數值標籤
for ax in g.axes.flat:
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width()/2., height + 3, 
                f'{int(height)}', ha='center', fontsize=11)

# 美化圖例
g._legend.set_title("存活狀態")
new_labels = ['未存活', '存活']
for t, l in zip(g._legend.texts, new_labels):
    t.set_text(l)

# 調整佈局
plt.tight_layout()
plt.subplots_adjust(top=0.9)

# 顯示圖形
plt.show()

# %% [markdown]
# ### 練習 3.5: 創建配對圖
# 使用Titanic數據集的數值變量（如age, fare, survived等）創建一個配對圖，
# 使用性別(sex)區分顏色。

# %%
# 解答 3.5
# 選擇要包含在配對圖中的數值變量
numeric_cols = ['survived', 'age', 'fare', 'pclass', 'sibsp', 'parch']

# 創建一個包含所選列的數據子集
titanic_subset = titanic[numeric_cols + ['sex']].copy()

# 將艙位轉回數值型
titanic_subset['pclass'] = titanic_subset['pclass'].astype(int)

# 使用pairplot創建配對圖
plt.figure(figsize=(12, 10))
g = sns.pairplot(
    data=titanic_subset,
    hue="sex",  # 按性別區分顏色
    vars=numeric_cols,  # 要顯示的變量
    palette={"male": "#3498db", "female": "#e74c3c"},  # 自定義顏色
    diag_kind="kde",  # 對角線上顯示核密度估計
    markers=["o", "s"],  # 男性用圓點，女性用方塊
    plot_kws={"alpha": 0.6, "s": 80, "edgecolor": "w", "linewidth": 0.5},  # 散點圖參數
    diag_kws={"shade": True, "alpha": 0.5},  # 對角線圖參數
    corner=True  # 只顯示下三角部分
)

# 設置總標題
g.fig.suptitle('泰坦尼克號數據集變量間的關係 (按性別分組)', fontsize=16, y=1.02)

# 美化軸標籤
g._legend.set_title("性別")
new_labels = ['男性', '女性']
for t, l in zip(g._legend.texts, new_labels):
    t.set_text(l)

# 自定義變量標籤映射
var_labels = {
    'survived': '存活狀態',
    'age': '年齡',
    'fare': '票價',
    'pclass': '艙位等級',
    'sibsp': '兄弟姐妹/配偶數',
    'parch': '父母/子女數'
}

# 應用自定義標籤
for ax in g.axes.flat:
    if ax is not None:
        # 設置x軸標籤
        if ax.get_xlabel() in var_labels:
            ax.set_xlabel(var_labels[ax.get_xlabel()], fontsize=12)
        
        # 設置y軸標籤
        if ax.get_ylabel() in var_labels:
            ax.set_ylabel(var_labels[ax.get_ylabel()], fontsize=12)

# 顯示圖形
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 練習 3.6: 創建熱圖
# 計算Titanic數據集中數值變量之間的相關性，並使用熱圖展示。
# 要求在熱圖上顯示相關係數值。

# %%
# 解答 3.6
# 選擇數值型變量
numeric_vars = ['survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']

# 計算相關係數矩陣
correlation = titanic[numeric_vars].corr()

# 設置圖表大小
plt.figure(figsize=(10, 8))

# 創建自定義發散調色板，以0為中心
cmap = sns.diverging_palette(240, 10, as_cmap=True)

# 創建熱圖
mask = np.triu(correlation)  # 創建上三角遮罩
heatmap = sns.heatmap(
    correlation,
    annot=True,  # 顯示相關係數值
    fmt='.2f',   # 保留兩位小數
    cmap=cmap,   # 使用自定義調色板
    vmin=-1, vmax=1,  # 設置值範圍
    center=0,    # 設置調色板的中心點
    square=True, # 正方形單元格
    linewidths=0.5,  # 單元格邊框寬度
    cbar_kws={"shrink": .8, "label": "相關係數"}, # 顏色條設置
    mask=mask,  # 應用遮罩，只顯示下三角
    annot_kws={"size": 12}  # 註釋文字大小
)

# 添加標題
plt.title('泰坦尼克號數據集變量間的相關性熱圖', fontsize=16, pad=20)

# 設置軸標籤
# 創建變量名稱映射
var_names = {
    'survived': '存活狀態',
    'pclass': '艙位等級',
    'age': '年齡',
    'sibsp': '兄弟姐妹/配偶數',
    'parch': '父母/子女數',
    'fare': '票價'
}

# 應用自定義標籤
heatmap.set_xticklabels([var_names[var] for var in numeric_vars], fontsize=12)
heatmap.set_yticklabels([var_names[var] for var in numeric_vars], fontsize=12, rotation=0)

# 添加解釋文本
plt.figtext(0.5, 0.01, 
           "相關係數範圍: -1 (完全負相關) 到 1 (完全正相關)", 
           ha="center", fontsize=10, bbox={"facecolor":"orange", "alpha":0.2, "pad":5})

# 調整佈局
plt.tight_layout()

# 顯示圖形
plt.show()

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
# 解答 4.1
# 創建改進版的圖表

# 設置風格
plt.style.use('seaborn-v0_8-whitegrid')

# 創建圖形和軸對象
fig, ax = plt.subplots(figsize=(12, 7))

# 繪製主曲線，使用漸變色
n_points = len(x)
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = plt.matplotlib.collections.LineCollection(
    segments, cmap='viridis', 
    norm=plt.Normalize(0, 10)
)
lc.set_array(x)
lc.set_linewidth(3)
line = ax.add_collection(lc)

# 添加數據點標記 (每10個點標記一次)
ax.scatter(x[::10], y[::10], s=100, c=x[::10], cmap='viridis', 
          edgecolor='white', linewidth=1.5, zorder=3)

# 添加颜色条
cbar = fig.colorbar(line, ax=ax, label='x 值')
cbar.set_label('x 值', fontsize=12, rotation=270, labelpad=20)

# 改进标题和标签
ax.set_title('衰减正弦波 $y = \sin(x) \cdot e^{-x/5}$', fontsize=18, pad=20)
ax.set_xlabel('x 軸', fontsize=14, labelpad=15)
ax.set_ylabel('y 值', fontsize=14, labelpad=15)

# 调整坐标轴范围
ax.set_xlim(0, 10)
y_min, y_max = y.min() - 0.1, y.max() + 0.1
ax.set_ylim(y_min, y_max)

# 自定义轴刻度
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.yaxis.set_major_locator(MultipleLocator(0.2))
ax.yaxis.set_minor_locator(MultipleLocator(0.1))

# 自定义网格
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_facecolor('#f8f9fa')

# 添加零线
ax.axhline(y=0, color='#999999', linestyle='-', linewidth=1, alpha=0.7)

# 添加注释
max_idx = np.argmax(y)
ax.annotate('最大值點', 
           xy=(x[max_idx], y[max_idx]),
           xytext=(x[max_idx]+1, y[max_idx]+0.1),
           arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
           fontsize=12)

# 添加图例
ax.plot([], [], label='衰减正弦波', color='darkviolet', linewidth=2)
ax.legend(loc='upper right', fontsize=12, frameon=True, 
         shadow=True, framealpha=0.9)

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()

# %% [markdown]
# ### 練習 4.2: 創建帶有註釋的圖表
# 使用與練習4.1相同的數據，創建一個帶有以下元素的圖表：
# - 在最大值和最小值處添加標註（使用箭頭和文本）
# - 添加一個說明數據趨勢的文本框
# - 使用數學公式（使用LaTeX語法）標註函數表達式
# - 添加一個自定義圖例

# %%
# 解答 4.2
# 計算重要點的位置
max_idx = np.argmax(y)
max_x, max_y = x[max_idx], y[max_idx]

min_idx = np.argmin(y)
min_x, min_y = x[min_idx], y[min_idx]

# 創建帶有註釋的圖表
fig, ax = plt.subplots(figsize=(12, 7))

# 繪製主曲線
ax.plot(x, y, color='#3498db', linewidth=2.5, label='衰減正弦波')

# 標記最大值和最小值點
ax.plot(max_x, max_y, 'ro', markersize=10)
ax.plot(min_x, min_y, 'go', markersize=10)

# 添加最大值標註
ax.annotate('最大值: ({:.1f}, {:.2f})'.format(max_x, max_y),
           xy=(max_x, max_y),
           xytext=(max_x+1, max_y+0.1),
           arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, alpha=0.7),
           fontsize=12,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.8, edgecolor='red'))

# 添加最小值標註
ax.annotate('最小值: ({:.1f}, {:.2f})'.format(min_x, min_y),
           xy=(min_x, min_y),
           xytext=(min_x-2, min_y-0.15),
           arrowprops=dict(facecolor='green', shrink=0.05, width=1.5, alpha=0.7),
           fontsize=12,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.8, edgecolor='green'))

# 添加函數表達式
func_text = r'$f(x) = \sin(x) \cdot e^{-\frac{x}{5}}$'
ax.text(5, 0.6, func_text, fontsize=18, color='navy', 
      bbox=dict(facecolor='white', edgecolor='navy', boxstyle='round,pad=0.5', alpha=0.8))

# 添加趨勢說明文本框
trend_text = "曲線表現出一個振蕩衰減的趨勢，\n初始時達到最大值，然後振幅\n逐漸衰減並趨近於零。這種現象\n在物理學中稱為阻尼振動。"
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(6, -0.2, trend_text, fontsize=11, verticalalignment='bottom', 
       bbox=props)

# 添加自定義圖例
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

legend_elements = [
    Line2D([0], [0], color='#3498db', lw=2, label='衰減正弦波'),
    Line2D([0], [0], marker='o', color='w', label='最大值',
          markerfacecolor='r', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='最小值',
          markerfacecolor='g', markersize=10),
    Patch(facecolor='wheat', edgecolor='k', alpha=0.8, label='數據趨勢說明')
]

ax.legend(handles=legend_elements, loc='upper right', fontsize=10,
         title='圖例說明', title_fontsize=12, 
         bbox_to_anchor=(1.15, 1), frameon=True, shadow=True)

# 美化軸和網格
ax.set_xlabel('x 軸', fontsize=14, labelpad=10)
ax.set_ylabel('y 值', fontsize=14, labelpad=10)
ax.set_title('帶註釋的衰減正弦波分析', fontsize=16, pad=15)

ax.grid(True, linestyle='--', alpha=0.7)
ax.set_facecolor('#f8f9fa')

# 添加坐標軸範圍
ax.set_xlim(0, 10)
ax.set_ylim(-0.4, 0.85)

# 調整佈局
plt.tight_layout()

# 顯示圖形
plt.show()

# %% [markdown]
# ### 練習 4.3: 創建多子圖布局
# 創建一個複雜的圖表，包含不同類型的子圖，要求：
# - 使用GridSpec創建非均勻的佈局（至少4個子圖）
# - 每個子圖展示不同類型的圖表（如直方圖、散點圖、折線圖等）
# - 子圖之間有適當的間距
# - 添加整體標題和每個子圖的標題
# - 確保坐標軸標籤不重疊

# %%
# 解答 4.3
# 導入GridSpec
from matplotlib.gridspec import GridSpec

# 創建一個較大的圖形
plt.figure(figsize=(15, 12))

# 使用GridSpec創建非均勻佈局
gs = GridSpec(3, 3, width_ratios=[1.5, 1, 1], height_ratios=[1, 1.5, 1], 
             wspace=0.4, hspace=0.4)

# 1. 折線圖 (左上，跨越兩列)
ax1 = plt.subplot(gs[0, 0:2])

# 創建並繪製衰減正弦曲線
x_line = np.linspace(0, 10, 200)
y_line = np.sin(x_line) * np.exp(-x_line/5)
ax1.plot(x_line, y_line, color='blue', linewidth=2)
ax1.set_title('衰減正弦波', fontsize=14)
ax1.set_xlabel('x 軸', fontsize=12)
ax1.set_ylabel('y 值', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.7)

# 2. 散點圖 (右上)
ax2 = plt.subplot(gs[0, 2])

# 創建隨機散點
n = 50
x_scatter = np.random.rand(n) * 10
y_scatter = np.random.rand(n) * 10
colors = np.random.rand(n)
sizes = np.random.rand(n) * 200 + 50

scatter = ax2.scatter(x_scatter, y_scatter, c=colors, s=sizes, alpha=0.6, 
                     cmap='viridis', edgecolor='black')
ax2.set_title('隨機散點', fontsize=14)
ax2.set_xlabel('x 軸', fontsize=12)
ax2.set_ylabel('y 軸', fontsize=12)
ax2.grid(True, alpha=0.3)

# 3. 熱圖 (中間左，較大)
ax3 = plt.subplot(gs[1, 0])

# 創建一個相關矩陣風格的熱圖
data = np.corrcoef(np.random.rand(10, 10))
im = ax3.imshow(data, cmap='coolwarm', interpolation='nearest', vmin=-1, vmax=1)
ax3.set_title('相關矩陣熱圖', fontsize=14)
plt.colorbar(im, ax=ax3, fraction=0.046, pad=0.04)
ax3.set_xticks(np.arange(data.shape[1]))
ax3.set_yticks(np.arange(data.shape[0]))
ax3.set_xticklabels([f'X{i+1}' for i in range(data.shape[1])], fontsize=8, rotation=45)
ax3.set_yticklabels([f'X{i+1}' for i in range(data.shape[0])], fontsize=8)

# 4. 直方圖 (中間)
ax4 = plt.subplot(gs[1, 1])

# 創建正態分布的直方圖
data_hist = np.random.normal(0, 1, 1000)
ax4.hist(data_hist, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
ax4.set_title('正態分布直方圖', fontsize=14)
ax4.set_xlabel('值', fontsize=12)
ax4.set_ylabel('頻率', fontsize=12)
ax4.grid(True, axis='y', alpha=0.3)

# 5. 餅圖 (中間右)
ax5 = plt.subplot(gs[1, 2])

# 創建餅圖
labels = ['A', 'B', 'C', 'D', 'E']
sizes = [25, 30, 15, 10, 20]
colors = plt.cm.Paired(np.arange(len(labels))/len(labels))
wedges, texts, autotexts = ax5.pie(sizes, labels=labels, autopct='%1.1f%%',
                                  startangle=90, colors=colors, 
                                  wedgeprops={'width': 0.5, 'edgecolor': 'w'},
                                  textprops={'fontsize': 10})
plt.setp(autotexts, size=10, weight="bold")
ax5.set_title('環形圖', fontsize=14)
ax5.axis('equal')  # 確保餅圖是圓的

# 6. 等高線圖 (底部，跨越三列)
ax6 = plt.subplot(gs[2, :])

# 創建等高線圖
x_contour = np.linspace(-3, 3, 100)
y_contour = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x_contour, y_contour)
Z = np.sin(X) * np.cos(Y)

contour = ax6.contourf(X, Y, Z, 20, cmap='viridis')
ax6.contour(X, Y, Z, 10, colors='white', alpha=0.5, linewidths=0.5)
ax6.set_title('等高線圖', fontsize=14)
ax6.set_xlabel('x 軸', fontsize=12)
ax6.set_ylabel('y 軸', fontsize=12)
plt.colorbar(contour, ax=ax6, shrink=0.6, aspect=20, pad=0.02)

# 添加整體標題
plt.suptitle('多樣化圖表佈局展示', fontsize=20, y=0.98)

# 調整佈局
plt.tight_layout()
plt.subplots_adjust(top=0.93)

# 顯示圖形
plt.show()

# %% [markdown]
# ### 練習 4.4: 自定義風格
# 創建一個自定義的Matplotlib/Seaborn風格並應用它：
# - 定義自己的顏色方案
# - 自定義背景、網格和字體
# - 應用此風格到一個展示Titanic生存率的圖表上
# - 按性別分組並用不同顏色區分艙位

# %%
# 解答 4.4
# 創建自定義風格參數
custom_style = {
    # 顏色方案
    'axes.prop_cycle': plt.cycler('color', ['#6200EA', '#00C853', '#FF5722', '#2962FF', '#FFC107']),
    
    # 背景和網格
    'axes.facecolor': '#F5F5F5',
    'axes.grid': True,
    'axes.grid.which': 'both',
    'grid.color': '#BDBDBD',
    'grid.linestyle': '--',
    'grid.linewidth': 0.5,
    'grid.alpha': 0.5,
    
    # 邊框
    'axes.edgecolor': '#424242',
    'axes.linewidth': 1.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    
    # 字體和文本
    'font.family': 'sans-serif',
    'font.weight': 'medium',
    'axes.labelsize': 13,
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    
    # 圖例
    'legend.fancybox': True,
    'legend.frameon': True,
    'legend.framealpha': 0.9,
    'legend.fontsize': 11,
    'legend.edgecolor': '#424242',
    'legend.shadow': True,
    
    # 其他
    'figure.figsize': [10, 6],
    'figure.dpi': 100,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
}

# 套用自定義風格
with plt.rc_context(custom_style):
    # 創建Titanic生存率的圖表
    plt.figure(figsize=(12, 8))
    
    # 準備數據
    # 轉換pclass為分類型變量，以便於排序
    titanic['pclass'] = titanic['pclass'].astype(str)
    
    # 計算每個艙位和性別的生存率
    survival_rates = titanic.groupby(['pclass', 'sex'])['survived'].mean() * 100
    
    # 重塑數據
    survival_df = survival_rates.reset_index()
    survival_df.columns = ['艙位', '性別', '生存率(%)']
    
    # 分別繪製男性和女性的資料
    plt.figure(figsize=(12, 6))
    
    # 設定艙位顏色
    class_colors = {'1': '#6200EA', '2': '#00C853', '3': '#FF5722'}
    
    # 按性別分組繪製生存率
    for i, gender in enumerate(['male', 'female']):
        gender_data = survival_df[survival_df['性別'] == gender]
        
        # 繪製柱狀圖
        bars = plt.bar([p + i*0.3 for p in range(len(gender_data))], 
                      gender_data['生存率(%)'], 
                      width=0.3, 
                      color=[class_colors[c] for c in gender_data['艙位']],
                      edgecolor='black', 
                      linewidth=1.5,
                      alpha=0.8,
                      label=f"{'男性' if gender == 'male' else '女性'}")
        
        # 添加數據標籤
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom', 
                    fontsize=11, fontweight='bold')
    
    # 添加標題和軸標籤
    plt.title('泰坦尼克號生存率 (按性別和艙位分組)', pad=20)
    plt.xlabel('艙位等級', labelpad=15)
    plt.ylabel('生存率 (%)', labelpad=15)
    
    # 自定義 x 軸刻度
    plt.xticks([0.15, 1.15, 2.15], ['一等艙', '二等艙', '三等艙'])
    
    # 創建圖例
    # 性別圖例
    gender_handles = [
        plt.Rectangle((0, 0), 1, 1, color='gray', alpha=0.6, label='男性'),
        plt.Rectangle((0, 0), 1, 1, color='gray', alpha=0.9, label='女性')
    ]
    
    # 艙位圖例
    class_handles = [
        plt.Rectangle((0, 0), 1, 1, color=class_colors['1'], alpha=0.8, label='一等艙'),
        plt.Rectangle((0, 0), 1, 1, color=class_colors['2'], alpha=0.8, label='二等艙'),
        plt.Rectangle((0, 0), 1, 1, color=class_colors['3'], alpha=0.8, label='三等艙')
    ]
    
    # 添加圖例
    first_legend = plt.legend(handles=gender_handles, loc='upper right', title='性別')
    plt.gca().add_artist(first_legend)
    plt.legend(handles=class_handles, loc='upper center', title='艙位')
    
    # 添加文本註釋
    plt.annotate('女性生存率普遍高於男性', 
                xy=(0, 80), xytext=(0, 70),
                fontsize=12, color='#212121',
                bbox=dict(boxstyle="round,pad=0.5", 
                         facecolor='white', alpha=0.8, 
                         edgecolor='#424242'))
    
    # 設置 y 軸範圍
    plt.ylim(0, 100)
    
    # 添加參考線表示50%生存率
    plt.axhline(y=50, linestyle='--', color='#9E9E9E')
    plt.text(2.8, 52, '50%', va='center', ha='center', backgroundcolor='white')
    
    # 顯示圖表
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ## 📋 總結

# %% [markdown]
# 在本練習中，我們探索了使用Matplotlib和Seaborn進行數據視覺化的各種技巧：

# 1. **Matplotlib基礎操作**：
#    - 創建基本線圖並設置顏色、樣式和圖例
#    - 使用子圖網格展示多個圖表
#    - 使用面向對象接口創建和定制散點圖

# 2. **常見統計圖表實作**：
#    - 創建和分析模擬數據集
#    - 使用長條圖比較不同類別的統計量
#    - 繪製直方圖展示數據分佈
#    - 創建散點矩陣顯示變量之間的關係

# 3. **Seaborn統計可視化**：
#    - 使用Seaborn載入和探索數據集
#    - 創建箱形圖、小提琴圖等統計圖表
#    - 使用計數圖展示類別數據
#    - 創建配對圖和熱圖展示變量間關係

# 4. **圖表美化與專業呈現**：
#    - 改進基本圖表使其專業美觀
#    - 添加有意義的註釋和圖例
#    - 創建複雜的多子圖佈局
#    - 定義和應用自定義風格

# 這些技巧可以幫助您創建既美觀又專業的數據視覺化，有效地傳達數據中的關鍵洞察。通過結合Matplotlib和Seaborn的功能，您可以創建適合各種數據類型和分析目標的視覺化效果。 