import pandas as pd

# 定義題目數據
quiz_data = [
    {
        'id': 1,
        'question': 'Python 是什麼語言？',
        'option_a': '編譯型語言',
        'option_b': '直譯型語言',
        'option_c': '機器語言',
        'answer': 'b',
        'category': '基礎概念',
        'difficulty': '簡單',
        'knowledge_point': 'Python 語言特性',
        'question_type': '概念題',
        'chapter': '第一章'
    },
    {
        'id': 2,
        'question': 'NumPy 用來做什麼？',
        'option_a': '圖片處理',
        'option_b': '數值計算',
        'option_c': 'UI 設計',
        'answer': 'b',
        'category': 'NumPy',
        'difficulty': '簡單',
        'knowledge_point': 'NumPy 基本概念',
        'question_type': '概念題',
        'chapter': '第二章'
    },
    {
        'id': 3,
        'question': 'Pandas 的 DataFrame 是什麼？',
        'option_a': '資料庫表格',
        'option_b': '二維資料結構',
        'option_c': '一維資料結構',
        'answer': 'b',
        'category': 'Pandas',
        'difficulty': '中等',
        'knowledge_point': 'DataFrame 概念',
        'question_type': '概念題',
        'chapter': '第三章'
    },
    {
        'id': 4,
        'question': 'Matplotlib 主要用於？',
        'option_a': '資料處理',
        'option_b': '資料視覺化',
        'option_c': '資料分析',
        'answer': 'b',
        'category': 'Matplotlib',
        'difficulty': '簡單',
        'knowledge_point': 'Matplotlib 用途',
        'question_type': '概念題',
        'chapter': '第四章'
    },
    {
        'id': 5,
        'question': 'Seaborn 是基於哪個套件？',
        'option_a': 'Pandas',
        'option_b': 'Matplotlib',
        'option_c': 'NumPy',
        'answer': 'b',
        'category': 'Seaborn',
        'difficulty': '中等',
        'knowledge_point': 'Seaborn 基礎',
        'question_type': '概念題',
        'chapter': '第四章'
    },
    {
        'id': 6,
        'question': 'Python 的 list 和 tuple 主要區別？',
        'option_a': '可變性',
        'option_b': '記憶體使用',
        'option_c': '效能',
        'answer': 'a',
        'category': '基礎概念',
        'difficulty': '中等',
        'knowledge_point': '資料結構',
        'question_type': '比較題',
        'chapter': '第一章'
    },
    {
        'id': 7,
        'question': 'NumPy 的 array 和 Python list 主要區別？',
        'option_a': '記憶體使用',
        'option_b': '運算效能',
        'option_c': '資料型態',
        'answer': 'b',
        'category': 'NumPy',
        'difficulty': '中等',
        'knowledge_point': 'NumPy 效能',
        'question_type': '比較題',
        'chapter': '第二章'
    },
    {
        'id': 8,
        'question': 'Pandas 的 loc 和 iloc 主要區別？',
        'option_a': '索引方式',
        'option_b': '效能',
        'option_c': '記憶體使用',
        'answer': 'a',
        'category': 'Pandas',
        'difficulty': '中等',
        'knowledge_point': '資料選取',
        'question_type': '比較題',
        'chapter': '第三章'
    },
    {
        'id': 9,
        'question': 'Matplotlib 的 figure 和 axes 關係？',
        'option_a': '父子關係',
        'option_b': '獨立物件',
        'option_c': '相同物件',
        'answer': 'a',
        'category': 'Matplotlib',
        'difficulty': '中等',
        'knowledge_point': '圖形結構',
        'question_type': '概念題',
        'chapter': '第四章'
    },
    {
        'id': 10,
        'question': 'Seaborn 的 distplot 和 histplot 區別？',
        'option_a': '功能重疊',
        'option_b': '不同用途',
        'option_c': '效能差異',
        'answer': 'b',
        'category': 'Seaborn',
        'difficulty': '中等',
        'knowledge_point': '分布圖',
        'question_type': '比較題',
        'chapter': '第四章'
    }
]

# 創建 DataFrame
df = pd.DataFrame(quiz_data)

# 保存為 Excel 檔案
df.to_csv('quiz.csv', index=False, encoding='utf-8-sig')

print("quiz.xlsx 已成功創建！") 