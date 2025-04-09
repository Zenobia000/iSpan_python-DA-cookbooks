import streamlit as st
import pandas as pd
import time
from datetime import datetime
import random
import io
import base64
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statistics
import json
import csv

# --- 設定 ---
EXAM_DURATION_MIN = 15  # 測驗時長

# --- 初始化會話狀態 ---
if 'is_test_started' not in st.session_state:
    st.session_state.is_test_started = False
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'class_name' not in st.session_state:
    st.session_state.class_name = ""
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'is_submitted' not in st.session_state:
    st.session_state.is_submitted = False
if 'results' not in st.session_state:
    st.session_state.results = None
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "results"  # 默認顯示個人結果頁面

# --- 讀取題庫 ---
@st.cache_data
def load_questions(file="quiz.csv"):
    """讀取題庫並確保所有欄位都是有效值"""
    df = pd.read_csv(file, encoding='utf-8')
    
    # 確保所有文字欄位都是字符串，不是 NaN
    text_columns = ['question', 'option_a', 'option_b', 'option_c', 'answer', 'category', 'difficulty']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna('').astype(str)
    
    return df

# --- 計分 ---
def evaluate(questions, responses):
    """根據難度計算分數，確保總分為100分"""
    # 定義難度權重比例
    difficulty_weights = {
        "簡單": 1,    # 簡單題權重1
        "中等": 2,    # 中等題權重2
        "困難": 3     # 困難題權重3
    }
    
    # 計算總權重
    total_weight = sum(difficulty_weights[row['difficulty']] for _, row in questions.iterrows())
    
    # 分配每題分數權重
    question_scores = {}
    for _, row in questions.iterrows():
        qid = row['id']
        # 每題的分數 = 該難度權重 / 總權重 * 100
        question_scores[qid] = (difficulty_weights[row['difficulty']] / total_weight) * 100
    
    score = 0
    results = []
    
    # 統計各難度的題目數量和得分
    difficulty_stats = {
        "簡單": {"count": 0, "correct": 0, "points": 0, "max_points": 0},
        "中等": {"count": 0, "correct": 0, "points": 0, "max_points": 0},
        "困難": {"count": 0, "correct": 0, "points": 0, "max_points": 0}
    }
    
    for _, row in questions.iterrows():
        question_id = row['id']
        difficulty = row['difficulty']
        question_score = question_scores[question_id]
        
        # 更新難度統計的最大可能分數
        difficulty_stats[difficulty]["max_points"] += question_score
        difficulty_stats[difficulty]["count"] += 1
        
        correct = str(row['answer']).strip().lower()
        selected = str(responses.get(question_id, "")).strip().lower()
        
        # 檢查答案是否正確 - 空白答案視為錯誤
        is_correct = selected == correct if selected else False
        if is_correct:
            score += question_score
            difficulty_stats[difficulty]["correct"] += 1
            difficulty_stats[difficulty]["points"] += question_score
            
        results.append({
            'id': question_id,
            'question': row['question'],
            'selected': selected,
            'correct': correct,
            'is_correct': is_correct,
            'option_a': row['option_a'],
            'option_b': row['option_b'],
            'option_c': row['option_c'],
            'category': row['category'],
            'difficulty': difficulty,
            'score': question_score if is_correct else 0,
            'max_score': question_score
        })
    
    # 計算最終得分
    final_score = round(score, 1)
    
    # 添加難度統計到結果中
    for diff, stats in difficulty_stats.items():
        stats["correct_rate"] = (stats["correct"] / stats["count"] * 100) if stats["count"] > 0 else 0
        stats["max_points"] = round(stats["max_points"], 1)
        stats["points"] = round(stats["points"], 1)
    
    return final_score, results, difficulty_stats

# --- 產生Excel下載連結 ---
def get_excel_download_link(df, filename="測驗結果.xlsx"):
    """生成下載Excel的HTML link"""
    towrite = io.BytesIO()
    df.to_excel(towrite, encoding='utf-8', index=False, engine='openpyxl')
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">下載測驗結果Excel</a>'
    return href

# --- 結果匯出為Excel ---
def export_results_to_excel(results, name, class_name, score, total):
    """將測驗結果匯出為Excel格式"""
    # 建立DataFrame
    data = []
    for i, result in enumerate(results):
        row = {
            '題號': i+1,
            '題目': result['question'],
            '您的答案': f"{result['selected']}. {result['option_a'] if result['selected'] == 'a' else result['option_b'] if result['selected'] == 'b' else result['option_c'] if result['selected'] == 'c' else '未作答'}",
            '正確答案': f"{result['correct']}. {result['option_a'] if result['correct'] == 'a' else result['option_b'] if result['correct'] == 'b' else result['option_c'] if result['correct'] == 'c' else ''}",
            '是否正確': '✓' if result['is_correct'] else '✗'
        }
        data.append(row)
    
    df = pd.DataFrame(data)
    
    # 添加測驗資訊
    info_df = pd.DataFrame([
        {'說明': '學生姓名', '內容': name},
        {'說明': '班級', '內容': class_name},
        {'說明': '得分', '內容': f"{score}/{total}"},
        {'說明': '正確率', '內容': f"{round(score/total*100, 2)}%"},
        {'說明': '測驗時間', '內容': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ])
    
    # 合併兩個DataFrame成為一個Excel
    with pd.ExcelWriter(io.BytesIO()) as writer:
        info_df.to_excel(writer, sheet_name='測驗資訊', index=False)
        df.to_excel(writer, sheet_name='答題詳情', index=False)
        
        # 設定xlsx為UTF-8編碼
        return writer.book
    
    return df

# --- 根據得分給出激勵話語和特效 ---
def get_encouragement(correct_rate):
    if correct_rate >= 90:
        messages = [
            "太棒了！你的表現非常出色！",
            "傑出的成績！你真的很有天賦！",
            "完美！繼續保持這種水平！",
            "令人驚嘆的表現！你做得非常好！"
        ]
        effect = "balloons"
    elif correct_rate >= 80:
        messages = [
            "很優秀的成績！繼續保持！",
            "出色的表現！你很棒！",
            "很好的掌握！再接再厲！",
            "優異的結果！你的努力值得讚賞！"
        ]
        effect = "snow"
    elif correct_rate >= 70:
        messages = [
            "很好的成績！繼續努力！",
            "做得好！你的努力得到了回報！",
            "優秀的表現！再接再厲！",
            "不錯的成績！你的潛力很大！"
        ]
        effect = "confetti"
    elif correct_rate >= 60:
        messages = [
            "還不錯！但還有進步空間！",
            "繼續加油！你可以做得更好！",
            "及格了！請再接再厲！",
            "有些進步，但仍需努力！"
        ]
        effect = "stars"
    else:
        messages = [
            "不要氣餒，失敗是成功之母！",
            "相信自己，下次一定會更好！",
            "勇於面對困難，持續學習！",
            "這只是開始，繼續努力！"
        ]
        effect = "rain"
    
    return random.choice(messages), effect

# --- 顯示特效 ---
def show_effect(effect_name):
    if effect_name == "balloons":
        st.balloons()
    elif effect_name == "snow":
        st.snow()
    elif effect_name == "confetti":
        # 自製五彩紙屑效果
        st.markdown("""
        <style>
        .confetti {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1000;
            animation: confetti-fall 5s linear infinite;
        }
        @keyframes confetti-fall {
            0% { transform: translateY(-10%); opacity: 1; }
            100% { transform: translateY(100%); opacity: 0; }
        }
        </style>
        <div class="confetti">
            <svg width="100%" height="100%" viewBox="0 0 600 600" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="300" cy="300" r="4" fill="#FF5252" opacity="0.7"/>
                <circle cx="320" cy="150" r="3" fill="#2196F3" opacity="0.7"/>
                <circle cx="190" cy="250" r="5" fill="#FFC107" opacity="0.7"/>
                <circle cx="370" cy="280" r="4" fill="#4CAF50" opacity="0.7"/>
                <circle cx="250" cy="180" r="3" fill="#9C27B0" opacity="0.7"/>
                <rect x="280" y="220" width="8" height="3" fill="#FF9800" opacity="0.7"/>
                <rect x="350" y="150" width="6" height="4" fill="#2196F3" opacity="0.7"/>
                <rect x="400" y="300" width="5" height="5" fill="#4CAF50" opacity="0.7"/>
                <rect x="200" y="350" width="7" height="3" fill="#E91E63" opacity="0.7"/>
                <rect x="100" y="200" width="5" height="6" fill="#9C27B0" opacity="0.7"/>
            </svg>
        </div>
        """, unsafe_allow_html=True)
    elif effect_name == "stars":
        # 自製星星閃爍效果
        st.markdown("""
        <style>
        .stars {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1000;
        }
        .star {
            position: absolute;
            background-color: white;
            border-radius: 50%;
            animation: twinkle 2s infinite;
        }
        @keyframes twinkle {
            0% { opacity: 0.2; }
            50% { opacity: 1; }
            100% { opacity: 0.2; }
        }
        </style>
        <div class="stars">
            <div class="star" style="top: 20%; left: 15%; width: 3px; height: 3px; animation-delay: 0s;"></div>
            <div class="star" style="top: 30%; left: 30%; width: 2px; height: 2px; animation-delay: 0.4s;"></div>
            <div class="star" style="top: 25%; left: 60%; width: 4px; height: 4px; animation-delay: 0.8s;"></div>
            <div class="star" style="top: 10%; left: 40%; width: 3px; height: 3px; animation-delay: 1.2s;"></div>
            <div class="star" style="top: 40%; left: 25%; width: 2px; height: 2px; animation-delay: 1.6s;"></div>
            <div class="star" style="top: 65%; left: 75%; width: 3px; height: 3px; animation-delay: 0.2s;"></div>
            <div class="star" style="top: 50%; left: 80%; width: 4px; height: 4px; animation-delay: 0.6s;"></div>
            <div class="star" style="top: 70%; left: 45%; width: 2px; height: 2px; animation-delay: 1.0s;"></div>
            <div class="star" style="top: 85%; left: 20%; width: 3px; height: 3px; animation-delay: 1.4s;"></div>
            <div class="star" style="top: 90%; left: 65%; width: 2px; height: 2px; animation-delay: 1.8s;"></div>
        </div>
        """, unsafe_allow_html=True)
    elif effect_name == "rain":
        # 自製雨滴效果
        st.markdown("""
        <style>
        .rain {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1000;
        }
        .drop {
            position: absolute;
            width: 2px;
            background: linear-gradient(to bottom, rgba(13, 71, 161, 0), rgba(13, 71, 161, 0.5));
            animation: fall linear infinite;
        }
        @keyframes fall {
            0% { transform: translateY(-100px); opacity: 0; }
            10% { opacity: 1; }
            100% { transform: translateY(100vh); opacity: 0.5; }
        }
        </style>
        <div class="rain">
            <div class="drop" style="left: 10%; height: 30px; animation-duration: 1.5s;"></div>
            <div class="drop" style="left: 20%; height: 20px; animation-duration: 1.8s;"></div>
            <div class="drop" style="left: 30%; height: 15px; animation-duration: 1.2s;"></div>
            <div class="drop" style="left: 40%; height: 25px; animation-duration: 1.6s;"></div>
            <div class="drop" style="left: 50%; height: 20px; animation-duration: 1.3s;"></div>
            <div class="drop" style="left: 60%; height: 30px; animation-duration: 1.7s;"></div>
            <div class="drop" style="left: 70%; height: 15px; animation-duration: 1.4s;"></div>
            <div class="drop" style="left: 80%; height: 25px; animation-duration: 1.9s;"></div>
            <div class="drop" style="left: 90%; height: 20px; animation-duration: 1.5s;"></div>
        </div>
        """, unsafe_allow_html=True)

# --- 儲存結果到CSV ---
def save_result(name, class_name, score, total, responses):
    """保存測驗結果"""
    try:
        # 準備數據
        result_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'name': name,
            'class': class_name,
            'score': score,
            'total': total,
            'correct_rate': round((score/total)*100, 2) if total > 0 else 0
        }
        
        # 添加每題的答案
        for qid, ans in responses.items():
            result_data[f'q{qid}'] = ans
            
        # 轉換為 DataFrame
        result_df = pd.DataFrame([result_data])
        
        # 如果文件存在，則追加；否則創建新文件
        mode = 'a' if os.path.exists('result_log.csv') else 'w'
        header = not os.path.exists('result_log.csv')
        
        # 使用相應的參數寫入 CSV
        result_df.to_csv('result_log.csv', 
                        mode=mode,
                        header=header,
                        index=False,
                        encoding='utf-8',
                        quoting=csv.QUOTE_ALL,
                        escapechar='\\',
                        doublequote=True)
        
        return result_data['correct_rate']
        
    except Exception as e:
        print(f"保存結果時出錯: {str(e)}")
        return 0

# --- 取得題目統計 ---
def get_question_statistics():
    try:
        # 讀取所有結果
        results_df = pd.read_csv('result_log.csv')
        questions = load_questions()
        
        stats = []
        for i in range(1, len(questions) + 1):
            # 獲取正確答案
            correct_answer = str(questions.loc[questions['id'] == i, 'answer'].iloc[0]).strip().lower()
            
            # 計算此題的答對率
            question_col = f'q{i}'
            if question_col in results_df.columns:
                total_answers = results_df[question_col].notna().sum()
                correct_answers = results_df[results_df[question_col].str.strip().str.lower() == correct_answer].shape[0]
                correct_rate = (correct_answers / total_answers * 100) if total_answers > 0 else 0
            else:
                correct_rate = 0
            
            stats.append({
                'question_id': i,
                'correct_rate': correct_rate,
                'total_answers': total_answers if 'total_answers' in locals() else 0
            })
        
        return stats
    except Exception as e:
        print(f"Error in get_question_statistics: {e}")
        return []

# --- 取得類別統計 ---
def get_category_statistics(questions, results_df):
    try:
        category_stats = {}
        
        # 對每個類別計算正確率
        for _, row in questions.iterrows():
            category = row['category']
            question_id = row['id']
            correct_answer = str(row['answer']).strip().lower()
            
            if category not in category_stats:
                category_stats[category] = {'correct': 0, 'total': 0, 'class_correct_sum': 0, 'class_total_sum': 0}
            
            # 計算此類別題目的答對率
            question_col = f'q{question_id}'
            if question_col in results_df.columns:
                # 空值視為錯誤，但不影響總計
                total_answers = results_df.shape[0]  # 考慮所有學生
                # 只計算答案等於正確答案的情況
                correct_answers = results_df[results_df[question_col].fillna("").str.strip().str.lower() == correct_answer].shape[0]
                
                category_stats[category]['correct'] += correct_answers
                category_stats[category]['total'] += total_answers
                
                # 記錄班級總回答數和正確數
                category_stats[category]['class_correct_sum'] = correct_answers
                category_stats[category]['class_total_sum'] = total_answers
        
        # 計算每個類別的正確率
        for category in category_stats:
            total = category_stats[category]['total']
            correct = category_stats[category]['correct']
            category_stats[category]['correct_rate'] = (correct / total * 100) if total > 0 else 0
        
        return category_stats
    except Exception as e:
        print(f"Error in get_category_statistics: {e}")
        return {}

# --- 開始測驗 ---
def start_test():
    st.session_state.is_test_started = True
    st.session_state.start_time = time.time()
    st.session_state.responses = {}
    st.session_state.is_submitted = False
    st.session_state.results = None
    st.experimental_rerun()  # 從 st.rerun() 改為 st.experimental_rerun()

# --- 主流程 ---
def main():
    st.set_page_config(
        page_title="📝 班級線上測驗系統",
        page_icon="",
        layout="wide",  # 使用寬屏布局
        initial_sidebar_state="collapsed"  # 預設收起側邊欄
    )

    # 添加自定義 CSS 樣式
    st.markdown("""
    <style>
        /* 主容器寬度設置 */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        
        /* 標題樣式 */
        h1 {
            text-align: center;
            color: #1E88E5;
            padding-bottom: 2rem;
        }
        
        /* 標籤頁樣式 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            justify-content: center;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            white-space: pre-wrap;
            background-color: #F8F9FA;
            border-radius: 4px;
            gap: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* 卡片樣式 */
        div[data-testid="stExpander"] {
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            margin-bottom: 1rem;
        }
        
        /* 指標數字樣式 */
        div[data-testid="stMetric"] {
            background-color: #F8F9FA;
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
        }
        
        /* 圖表容器樣式 */
        div[data-testid="stPlotlyChart"] {
            background-color: white;
            border-radius: 4px;
            padding: 1rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("📚 Python資料分析能力評量")

    # 如果測驗尚未開始，顯示登入表單
    if not st.session_state.is_test_started:
        # 使用columns來優化登入表單布局
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("login_form", clear_on_submit=False):
                st.markdown("### 👤 考生資訊")
                st.session_state.name = st.text_input("姓名", value=st.session_state.name)
                st.session_state.class_name = st.text_input("班級", value=st.session_state.class_name)
                submitted = st.form_submit_button("開始測驗", use_container_width=True)
                
                if submitted:
                    if st.session_state.name and st.session_state.class_name:
                        start_test()
                    else:
                        st.error("請填寫姓名與班級再開始作答")
        
        # 添加考試說明
        with st.expander("📋 考試說明", expanded=True):
            st.markdown("""
            ### 考試時間與計分方式
            - 考試時間：30分鐘
            - 題目類型：選擇題
            - 計分方式：
                - 簡單題：5分/題
                - 中等題：10分/題
                - 困難題：15分/題
            
            ### 注意事項
            1. 請確實填寫姓名和班級
            2. 答題過程中請勿重新整理頁面
            3. 時間到系統會自動繳交
            4. 完成後可下載成績報告
            """)
        return

    # 測驗已開始
    questions = load_questions()
    end_time = st.session_state.start_time + EXAM_DURATION_MIN * 60

    # 如果已提交，顯示結果頁面
    if st.session_state.is_submitted:
        st.warning(f"📝 測驗已完成")
        score, results, difficulty_stats = evaluate(questions, st.session_state.responses)
        
        # 使用columns優化顯示布局
        st.subheader("📊 得分統計")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("總分", f"{score}/100")
        with col2:
            st.metric("及格狀態", "通過" if score >= 60 else "未通過", 
                     delta="🎉" if score >= 60 else "📚")
        with col3:
            total_correct = sum(1 for r in results if r['is_correct'])
            total_questions = len(results)
            st.metric("答對題數", f"{total_correct}/{total_questions}")
        with col4:
            st.metric("作答時間", f"{EXAM_DURATION_MIN}分鐘")
        
        # 顯示得分和激勵話語
        encouragement, effect = get_encouragement(score/100)
        st.success(f"😊 {encouragement}")
        show_effect(effect)
        
        # 顯示各難度得分情況
        st.subheader("📈 各難度得分分析")
        cols = st.columns(len(difficulty_stats))
        for i, (diff, stats) in enumerate(difficulty_stats.items()):
            with cols[i]:
                st.metric(
                    f"{diff}題得分",
                    f"{stats['points']}/{stats['max_points']}",
                    f"正確率 {stats['correct_rate']:.1f}%"
                )
        
        # 添加分頁選項卡，使用tabs功能
        tabs = st.tabs(["📊 個人結果", "📈 統計分析", "🏆 題目分析"])
        
        # --- 第一頁：個人結果 ---
        with tabs[0]:
            # 產生Excel下載連結
            results_df = pd.DataFrame([{
                '題號': r['id'],
                '題目': r['question'], 
                '您的答案': f"{r['selected']}. {r['option_a'] if r['selected'] == 'a' else r['option_b'] if r['selected'] == 'b' else r['option_c'] if r['selected'] == 'c' else '未作答'}" if r['selected'] else "未作答",
                '正確答案': f"{r['correct']}. {r['option_a'] if r['correct'] == 'a' else r['option_b'] if r['correct'] == 'b' else r['option_c'] if r['correct'] == 'c'else ''}",
                '是否正確': '✓' if r['is_correct'] else '✗'
            } for r in results])
            
            # 建立一個BytesIO對象
            towrite = io.BytesIO()
            # 寫入Excel
            with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
                # 添加學生資訊表
                info_df = pd.DataFrame([
                    {'說明': '學生姓名', '內容': st.session_state.name},
                    {'說明': '班級', '內容': st.session_state.class_name},
                    {'說明': '得分', '內容': f"{score}/100"},
                    {'說明': '正確率', '內容': f"{(score/100*100):.1f}%"},
                    {'說明': '測驗時間', '內容': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                ])
                info_df.to_excel(writer, sheet_name='測驗資訊', index=False)
                
                # 添加答題詳情表
                results_df.to_excel(writer, sheet_name='答題詳情', index=False)
            
            # 重置位置到開頭
            towrite.seek(0)
            
            # 轉換為base64
            b64 = base64.b64encode(towrite.read()).decode()
            
            # 建立下載連結
            dl_link = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{st.session_state.name}_{st.session_state.class_name}_測驗結果.xlsx" class="download-button">📊 下載測驗結果</a>'
            
            # 添加一些CSS樣式
            st.markdown("""
            <style>
            .download-button {
                display: inline-block;
                padding: 0.5em 1em;
                color: white !important;
                background-color: #4CAF50;
                text-align: center;
                border-radius: 4px;
                text-decoration: none;
                font-weight: bold;
                margin: 1em 0;
                transition: background-color 0.3s;
            }
            .download-button:hover {
                background-color: #45a049;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # 顯示下載按鈕
            st.markdown(dl_link, unsafe_allow_html=True)
            
            # 顯示答題詳情
            st.subheader("答題詳情")
            for result in results:
                with st.expander(f"題目 {result['id']}:"):
                    question_text = result['question']
                    
                    # 檢查是否包含程式碼區塊
                    if '\n' in question_text:
                        # 分離題目文字和程式碼區塊
                        parts = question_text.split('\n\n', 1)
                        if len(parts) == 2:
                            st.write(f"**題目:** {parts[0]}")
                            st.code(parts[1], language='python')
                        else:
                            st.write(f"**題目:** {question_text}")
                    else:
                        st.write(f"**題目:** {question_text}")
                    
                    if result['is_correct']:
                        st.success("✅ 回答正確")
                    else:
                        st.error("❌ 回答錯誤" if result['selected'] else "⚠️ 未作答")
                    
                    if result['selected']:
                        st.write("**您的答案:** " + f"{result['selected']}. " + 
                             (result['option_a'] if result['selected'] == 'a' else
                              result['option_b'] if result['selected'] == 'b' else
                              result['option_c'] if result['selected'] == 'c' else "未知選項"))
                    else:
                        st.write("**您的答案:** 未作答")
                    
                    st.write("**正確答案:** " + f"{result['correct']}. " + 
                             (result['option_a'] if result['correct'] == 'a' else
                              result['option_b'] if result['correct'] == 'b' else
                              result['option_c'] if result['correct'] == 'c' else "錯誤"))
        
        # --- 第二頁：統計分析 ---
        with tabs[1]:
            st.subheader("班級統計分析")
            
            # 讀取全部學生數據
            all_results = load_all_results()
            
            if all_results.empty:
                st.info("暫無其他學生完成測驗，無法生成統計數據。")
            else:
                # 確保數據格式正確
                for col in ['score', 'total', 'correct_rate']:
                    if col in all_results.columns:
                        all_results[col] = pd.to_numeric(all_results[col], errors='coerce')
                
                # 計算當前學生的分數和全班的分數統計
                current_score = score  # 直接使用計算好的分數
                
                # 計算統計摘要 - 分數應該是0-100範圍
                stats_summary = get_statistics_summary(all_results, current_score)
                
                # 計算學生百分位
                student_percentile = calculate_student_percentile(current_score, all_results["score"].values)
                
                # 顯示班級基本統計信息
                st.write("#### 班級統計")
                
                # 如果只有一個或兩個學生，顯示特別處理
                if all_results.shape[0] <= 2:
                    st.info(f"目前僅有 {all_results.shape[0]} 位學生完成測驗，統計數據僅供參考。")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("參與人數", all_results.shape[0])
                    
                    # 計算及格率
                    if 'score' in all_results.columns:
                        pass_count = (all_results['score'] >= 60).sum()
                        pass_rate = (pass_count / all_results.shape[0]) * 100 if all_results.shape[0] > 0 else 0
                        st.metric("及格率", f"{pass_rate:.1f}%")
                    else:
                        st.metric("及格率", "0.0%")
                
                with col2:
                    # 處理平均分
                    if 'score' in all_results.columns and not all_results['score'].empty:
                        avg_score = all_results['score'].mean()
                        st.metric("平均分數", f"{avg_score:.1f}分")
                        
                        # 處理中位數
                        median_score = all_results['score'].median()
                        st.metric("中位數", f"{median_score:.1f}分")
                    else:
                        st.metric("平均分數", "0.0分")
                        st.metric("中位數", "0.0分")
                
                with col3:
                    # 處理最高分和標準差
                    if 'score' in all_results.columns and not all_results['score'].empty:
                        max_score = all_results['score'].max()
                        std_dev = all_results['score'].std() if len(all_results) > 1 else 0.0
                        st.metric("最高分", f"{max_score:.1f}分")
                        st.metric("標準差", f"{std_dev:.1f}")
                    else:
                        st.metric("最高分", "0.0分")
                        st.metric("標準差", "0.0")
                
                # 顯示您的表現
                st.write("#### 您的表現")
                
                # 計算得分比較 - 直接計算與所有其他學生的平均分差異
                if 'score' in all_results.columns and all_results.shape[0] > 1:
                    # 使用所有人的平均分（包括自己）
                    all_avg = all_results['score'].mean()
                    
                    # 計算差異
                    diff_from_avg = current_score - all_avg
                    
                    # 顯示計算過程的調試信息（可選，可以在發布前移除）
                    # st.write(f"DEBUG: 您的分數={current_score}, 全班平均={all_avg}, 差異={diff_from_avg}")
                else:
                    diff_from_avg = 0
                
                # 確保差異值精確到小數點後一位
                diff_from_avg = round(diff_from_avg, 1)
                
                col1, col2 = st.columns(2)
                with col1:
                    # 計算百分位合理值
                    if all_results.shape[0] > 1:
                        disp_percentile = student_percentile
                    else:
                        disp_percentile = 50.0  # 只有一個學生時
                    
                    st.metric(
                        "班級排名百分位", 
                        f"{disp_percentile:.1f}",
                        help="表示您的成績超過了多少百分比的同學"
                    )
                
                with col2:
                    st.metric(
                        "與平均分差異",
                        f"{diff_from_avg:+.1f}分",
                        delta_color="normal"
                    )
                
                # 顯示相對位置提示
                if all_results.shape[0] <= 1:
                    st.info("目前只有您一位學生完成測驗，無法進行準確比較。")
                elif student_percentile >= 95:
                    st.success("🏆 恭喜！您的表現優異，位於班級前5%！")
                elif student_percentile >= 80:
                    st.success("🥇 太棒了！您的表現超過80%的同學！")
                elif student_percentile >= 60:
                    st.info("👍 不錯！您的表現超過60%的同學！")
                elif student_percentile >= 40:
                    st.info("🙂 您的表現接近班級中位數！")
                elif student_percentile >= 20:
                    st.warning("📚 繼續努力！您還有進步空間！")
                else:
                    st.warning("💪 加油！建議您重新複習相關內容！")
                
                # 生成分析圖表
                plots = generate_stats_plots(stats_summary, current_score)
                
                # 顯示分數分佈圖
                st.subheader("分數分佈")
                if "distribution" in plots:
                    # 檢查學生人數，給出合適的提示
                    if all_results.shape[0] <= 2:
                        st.warning("⚠️ 目前學生人數過少，統計分佈可能不具有足夠代表性")
                    st.info("圖表中紅色星星(★)和標記顯示您的成績位置")
                    st.plotly_chart(plots["distribution"], use_container_width=True)
                
                # 顯示百分位圖（改為箱形圖）
                st.subheader("班級成績分佈")
                if "percentiles" in plots:
                    # 檢查學生人數，給出合適的提示
                    if all_results.shape[0] <= 2:
                        st.warning("⚠️ 目前學生人數過少，統計分析可能不具代表性")
                    st.info("紅色星星(★)標記顯示您的成績位置，箱形圖展示班級整體分數分佈")
                    st.plotly_chart(plots["percentiles"], use_container_width=True)
                    
                    # 添加箱形圖解釋
                    with st.expander("📊 箱形圖解釋"):
                        st.markdown("""
                        ### 箱形圖解釋
                        
                        箱形圖是一種統計圖表，用於展示數據分佈的關鍵特徵：
                        
                        - **箱子**: 代表中間50%的數據範圍（從第25百分位到第75百分位）
                        - **箱子中的線**: 代表中位數（第50百分位）
                        - **菱形**: 代表平均值
                        - **上下觸鬚**: 代表數據的大致範圍
                        - **圓點**: 代表每位學生的實際分數
                        
                        通過箱形圖，您可以直觀地看到：
                        - 您的分數在班級中的位置
                        - 班級整體的分數分佈情況
                        - 班級的平均水平與中位水平
                        """)
        
        # --- 第三頁：題目分析 ---
        with tabs[2]:
            st.subheader("題目分析")
            
            # 直接從題庫計算難度分布
            difficulty_counts = questions['difficulty'].value_counts().to_dict()
            
            st.write("#### 題目難度分佈")
            cols = st.columns(3)
            with cols[0]:
                st.metric("簡單題目", difficulty_counts.get("簡單", 0))
            with cols[1]:
                st.metric("中等題目", difficulty_counts.get("中等", 0))
            with cols[2]:
                st.metric("困難題目", difficulty_counts.get("困難", 0))
            
            # 顯示各題目正確率
            st.write("#### 各題目答題情況分析")
            
            try:
                # 讀取所有學生的答題數據
                all_results = load_all_results()
                
                if all_results.empty:
                    st.warning("目前還沒有學生完成測驗，無法顯示班級統計數據。")
                    return
                
                # 計算每題的班級正確率
                class_correct_rates = {}
                difficulty_map = {}  # 存儲每個題目的難度
                
                for _, question in questions.iterrows():
                    qid = str(question['id'])
                    question_title = question['question']
                    question_difficulty = question['difficulty']
                    difficulty_map[qid] = question_difficulty
                    
                    col_name = f'q{qid}'
                    if col_name in all_results.columns:
                        correct_answer = str(question['answer']).strip().lower()
                        total_students = len(all_results)
                        if total_students > 0:
                            # 計算正確答案數量
                            correct_count = sum(
                                str(ans).strip().lower() == correct_answer 
                                for ans in all_results[col_name] if pd.notna(ans)
                            )
                            class_correct_rates[qid] = (correct_count / total_students) * 100
                        else:
                            class_correct_rates[qid] = 0
                    else:
                        class_correct_rates[qid] = 0
                
                # 創建題目分析圖表
                fig = go.Figure()
                
                # 定義難度顏色
                difficulty_colors = {
                    "簡單": "rgba(92, 184, 92, 0.8)",   # 綠色
                    "中等": "rgba(91, 192, 222, 0.8)",  # 藍色
                    "困難": "rgba(217, 83, 79, 0.8)"    # 紅色
                }
                
                # 定義難度標記符號
                difficulty_symbols = {
                    "簡單": "【簡】",
                    "中等": "【中】",
                    "困難": "【難】"
                }
                
                # 準備數據 - 按難度分組
                difficulty_groups = {
                    "簡單": {"ids": [], "x": [], "y": [], "hover": []},
                    "中等": {"ids": [], "x": [], "y": [], "hover": []},
                    "困難": {"ids": [], "x": [], "y": [], "hover": []}
                }
                
                # 整理數據
                for _, question in questions.iterrows():
                    qid = str(question['id'])
                    difficulty = difficulty_map.get(qid, "未知")
                    
                    if difficulty not in difficulty_groups:
                        continue
                    
                    # 添加難度標記
                    difficulty_label = difficulty_symbols.get(difficulty, f"【{difficulty}】")
                    
                    # 處理題目文字，如果包含程式碼區塊，只顯示題目部分
                    question_text = question['question']
                    if '\n' in question_text:
                        question_text = question_text.split('\n\n', 1)[0]
                    
                    question_display = f"Q{qid}: {difficulty_label} {question_text[:25]}..."
                    
                    difficulty_groups[difficulty]["ids"].append(qid)
                    difficulty_groups[difficulty]["y"].append(question_display)
                    difficulty_groups[difficulty]["x"].append(class_correct_rates.get(qid, 0))
                    
                    # 創建詳細的懸停文字，同樣處理程式碼區塊
                    hover_text = (f"題號: Q{qid}<br>"
                                 f"難度: {difficulty}<br>"
                                 f"正確率: {class_correct_rates.get(qid, 0):.1f}%<br>"
                                 f"題目: {question_text}")
                    
                    difficulty_groups[difficulty]["hover"].append(hover_text)
                
                # 按難度分類的列表
                all_difficulties = ["簡單", "中等", "困難"]
                
                # 按題號排序（而非難度分組）
                sorted_questions = []
                for _, question in questions.iterrows():
                    qid = str(question['id'])
                    difficulty = difficulty_map.get(qid, "未知")
                    difficulty_label = difficulty_symbols.get(difficulty, f"【{difficulty}】")
                    question_text = f"Q{qid}: {difficulty_label} {question['question'][:25]}..."
                    correct_rate = class_correct_rates.get(qid, 0)
                    
                    hover_text = (f"題號: Q{qid}<br>"
                                 f"難度: {difficulty}<br>"
                                 f"正確率: {correct_rate:.1f}%<br>"
                                 f"題目: {question['question']}")
                    
                    sorted_questions.append({
                        "qid": qid,
                        "text": question_text,
                        "difficulty": difficulty,
                        "correct_rate": correct_rate,
                        "hover": hover_text,
                        "sort_key": int(qid)  # 使用題號作為排序鍵
                    })
                
                # 按題號排序
                sorted_questions.sort(key=lambda q: q["sort_key"])
                
                # 收集所有排序後的y軸標籤
                y_axis_labels = [q["text"] for q in sorted_questions]
                
                # 為每個難度創建獨立的條形圖
                for difficulty in all_difficulties:
                    # 收集此難度的所有題目
                    bars_for_this_difficulty = []
                    y_positions = []
                    x_values = []
                    hover_texts = []
                    
                    for i, q in enumerate(sorted_questions):
                        if q["difficulty"] == difficulty:
                            y_positions.append(i)  # 使用排序後的索引位置
                            x_values.append(q["correct_rate"])
                            hover_texts.append(q["hover"])
                            bars_for_this_difficulty.append(q)
                    
                    if not y_positions:  # 如果此難度沒有題目，跳過
                        continue
                    
                    fig.add_trace(go.Bar(
                        x=x_values,
                        y=y_positions,  # 使用索引位置
                        orientation='h',
                        name=f'{difficulty}題',
                        marker_color=difficulty_colors[difficulty],
                        width=0.7,
                        text=[f"{x:.1f}%" for x in x_values],
                        textposition='auto',
                        hovertext=hover_texts,
                        hoverinfo='text'
                    ))
                
                # 使用HTML顏色標記進行Y軸標籤著色
                y_ticktext = []
                y_tickvals = list(range(len(y_axis_labels)))
                
                for i, label in enumerate(y_axis_labels):
                    # 提取難度標記，確定顏色
                    for diff in all_difficulties:
                        symbol = difficulty_symbols[diff]
                        if symbol in label:
                            color = difficulty_colors[diff].replace('0.8', '1.0')  # 加深顏色使文字清晰
                            y_ticktext.append(f'<span style="color:{color}">{label}</span>')
                            break
                    else:
                        y_ticktext.append(label)
                
                # 更新布局
                fig.update_layout(
                    title='題目答題情況分析 (依難度分類)',
                    xaxis_title='正確率 (%)',
                    yaxis_title='題目',
                    template='plotly_white',
                    height=max(600, len(y_axis_labels) * 40),  # 動態調整高度
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                        font=dict(size=14)  # 增加圖例字體大小
                    ),
                    xaxis=dict(
                        range=[0, 100],
                        tickformat='d',
                        ticksuffix='%',
                        title_font=dict(size=16),  # 增加X軸標題字體大小
                        tickfont=dict(size=14)  # 增加X軸刻度字體大小
                    ),
                    yaxis=dict(
                        tickmode='array',
                        tickvals=y_tickvals,
                        ticktext=y_ticktext,
                        autorange="reversed",  # 反轉Y軸使題號從上到下排列
                        title_font=dict(size=16),  # 增加Y軸標題字體大小
                        tickfont=dict(size=14)  # 增加Y軸刻度字體大小
                    ),
                    margin=dict(l=180),  # 增加左邊距以容納較長的Y軸標籤
                    title_font=dict(size=18),  # 增加圖表標題字體大小
                    font=dict(family="Arial, sans-serif")  # 設定全局字體
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 添加難度分析說明
                st.info("💡 上圖中按難度分類: 綠色=簡單題【簡】、藍色=中等題【中】、紅色=困難題【難】。懸停在任一題上可查看詳細資訊。")
                
                # 添加答對和答錯題目的強弱分析
                st.write("#### 答題強弱分析")
                
                # 檢查答題結果是否存在
                if not hasattr(st.session_state, 'results') or not st.session_state.results:
                    st.warning("無法獲取您的答題結果，請確保您已完成測驗。")
                    return
                
                # 計算個人答對題目和錯誤題目
                correct_questions = []
                incorrect_questions = []
                
                # 處理每個題目的答題情況
                for result in st.session_state.results:
                    try:
                        qid = str(result['id'])  # 確保 qid 是字符串
                        question_data = questions[questions['id'] == int(qid)]
                        
                        if question_data.empty:
                            continue
                            
                        question = question_data.iloc[0]
                        question_info = {
                            'id': qid,
                            'question': question['question'],
                            'category': question['category'],
                            'difficulty': question['difficulty'],
                            'correct_rate': class_correct_rates.get(qid, 0)
                        }
                        
                        if result.get('is_correct'):
                            correct_questions.append(question_info)
                        else:
                            incorrect_questions.append(question_info)
                            
                    except Exception as e:
                        print(f"處理題目 {qid} 時發生錯誤: {str(e)}")
                        continue
                
                # 顯示答對題目分析
                with st.expander("✅ 答對題目分析", expanded=True):
                    if correct_questions:
                        st.write(f"您總共答對了 {len(correct_questions)} 題")
                        for q in correct_questions:
                            st.write(f"- Q{q['id']}: {q['question']} (難度: {q['difficulty']}, 類別: {q['category']}, 全班正確率: {q['correct_rate']:.1f}%)")
                    else:
                        st.warning("沒有答對的題目")
                
                # 顯示答錯題目分析
                with st.expander("❌ 答錯題目分析", expanded=True):
                    if incorrect_questions:
                        st.write(f"您總共答錯了 {len(incorrect_questions)} 題")
                        for q in incorrect_questions:
                            st.write(f"- Q{q['id']}: {q['question']} (難度: {q['difficulty']}, 類別: {q['category']}, 全班正確率: {q['correct_rate']:.1f}%)")
                    else:
                        st.success("沒有答錯的題目")
                
                # 提供學習建議
                if incorrect_questions:
                    st.write("#### 學習建議")
                    
                    # 按類別分析錯題
                    category_mistakes = {}
                    for q in incorrect_questions:
                        category = q['category']
                        if category not in category_mistakes:
                            category_mistakes[category] = []
                        category_mistakes[category].append(q)
                    
                    st.write("根據您的答題情況，建議您加強以下知識點：")
                    for category, questions in category_mistakes.items():
                        with st.expander(f"📚 {category} ({len(questions)} 題需要加強)"):
                            st.write(f"在 {category} 類別中，您答錯了以下題目：")
                            for q in questions:
                                st.write(f"- Q{q['id']}: {q['question']}")
                            st.write("建議：")
                            st.write("1. 複習相關概念和使用方法")
                            st.write("2. 多做相關練習題")
                            st.write("3. 參考官方文檔或教材深入學習")
                else:
                    st.success("恭喜！您的表現很好，建議繼續保持！")
                    
            except Exception as e:
                st.error(f"分析題目時發生錯誤: {str(e)}")
                print(f"錯誤詳情: {str(e)}")
                st.warning("無法完成題目分析，請確保您已完成測驗並正確提交結果。")
        
        # 測驗結束提示
        st.info("測驗已經完成，請記得下載測驗結果Excel檔案，以便日後複習。")
        return
        
    # 正在測驗中
    st.warning(f"⏳ 測驗進行中，姓名：{st.session_state.name}，班級：{st.session_state.class_name}")
    
    # 顯示剩餘時間
    remaining_time = int(end_time - time.time())
    mins, secs = divmod(remaining_time, 60)
    st.info(f"⌛ 剩餘時間：{mins:02d}:{secs:02d}")
    
    st.divider()

    # 顯示題目
    for i, row in questions.iterrows():
        question_text = row['question']
        
        # 檢查是否包含程式碼區塊（通過檢查是否有換行符號）
        if '\n' in question_text:
            # 分離題目文字和程式碼區塊
            parts = question_text.split('\n\n', 1)
            if len(parts) == 2:
                st.subheader(f"Q{i+1}. {parts[0]}")
                st.code(parts[1], language='python')
            else:
                st.subheader(f"Q{i+1}. {question_text}")
        else:
            st.subheader(f"Q{i+1}. {question_text}")
        
        # 準備選項列表，包含一個空選項
        options = [
            ("", "請選擇答案..."),
            ("a", str(row["option_a"])),
            ("b", str(row["option_b"])),
            ("c", str(row["option_c"]))
        ]
        
        # 決定預設選項
        default_idx = 0  # 預設為 "請選擇答案..."
        if row["id"] in st.session_state.responses:
            ans = st.session_state.responses[row["id"]]
            if ans == "a": default_idx = 1
            elif ans == "b": default_idx = 2
            elif ans == "c": default_idx = 3
        
        choice = st.selectbox(
            "請選擇：", 
            options=options,
            format_func=lambda x: f"{x[0]}. {x[1]}" if x[0] else x[1],
            index=default_idx,
            key=f"select_{i}"
        )
        
        # 更新答案，只儲存非空選擇
        if choice and choice[0]:
            st.session_state.responses[row["id"]] = choice[0]

    # 倒數與自動繳交
    remaining_time = int(end_time - time.time())
    
    # 顯示未作答題目數量
    answered_count = len(st.session_state.responses)
    total_count = len(questions)
    if answered_count < total_count:
        st.warning(f"⚠️ 您尚有 {total_count - answered_count} 題未作答，但您可以直接提交。")
    else:
        st.success("✅ 所有題目都已作答！")
        
    if remaining_time <= 0 or st.button("✅ 提交測驗", disabled=st.session_state.is_submitted):
        try:
            # 直接使用 session_state.responses 的答案，已經由 selectbox 控件更新過
            responses = st.session_state.responses.copy()
            
            # 如果沒有任何回答，顯示警告
            if len(responses) == 0:
                st.warning("⚠️ 您尚未回答任何題目。確定要提交空白測驗嗎？")
                if not st.button("確認提交空白測驗"):
                    st.stop()
            
            # 評分與結果計算
            score, results, difficulty_stats = evaluate(questions, responses)
            st.session_state.results = results
            st.session_state.is_submitted = True
            
            # 添加調試信息，檢查用戶選擇的答案
            st.write("#### 調試信息 - 用戶答案")
            st.write(st.session_state.responses)
            
            # 計算總分和最大可能分數
            score = sum(r['score'] for r in st.session_state.results)
            total = sum(r['max_score'] for r in st.session_state.results)
            
            # 正確調用 save_result 函數
            correct_rate = save_result(
                st.session_state.name,
                st.session_state.class_name,
                score,  # 傳入計算出的分數
                total,  # 傳入計算出的總分
                st.session_state.responses  # 用戶回答
            )
            
            if correct_rate > 0:
                st.success("測驗結果已成功儲存！")
            else:
                st.error("測驗結果儲存失敗，請聯繫管理員。")
            
            # 顯示答題情況摘要，以便確認資料是否正確保存
            st.info(f"已回答 {len(responses)}/{len(questions)} 題，得分 {score:.1f} 分")
            
            st.experimental_rerun()
        except Exception as e:
            st.error(f"提交測驗時發生錯誤: {str(e)}")
            st.error(f"錯誤詳情: {type(e).__name__}")
            # 顯示目前的答案數據，幫助除錯
            st.write("目前記錄的答案:", st.session_state.responses)

    # 顯示剩餘時間（自動更新）
    with st.empty():
        try:
            while time.time() < end_time and not st.session_state.is_submitted:
                remaining = int(end_time - time.time())
                mins, secs = divmod(remaining, 60)
                
                # 更新顯示
                st.write(f"⌛ 剩餘時間：{mins:02d}:{secs:02d}")
                
                # 使用較短的睡眠時間，減少 WebSocket 超時風險
                time.sleep(0.5)
                
                # 如果時間到期，自動提交
                if remaining <= 0:
                    break
                
                # 每 5 秒才重新運行一次，減少 WebSocket 負擔
                if remaining % 5 == 0:
                    if not st.session_state.is_submitted:
                        try:
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(f"更新頁面時發生錯誤: {str(e)}")
                            break
        except Exception as e:
            st.error(f"計時器發生錯誤: {str(e)}")
            # 如果計時器出錯，自動提交測驗
            if not st.session_state.is_submitted:
                # 選擇性地在這裡添加自動提交邏輯
                pass

# --- 統計數據分析功能 ---
def load_all_results():
    """讀取所有學生的測驗結果"""
    try:
        # 使用 quoting 參數來正確處理包含換行符的欄位
        results_df = pd.read_csv('result_log.csv', 
                               encoding='utf-8',
                               quoting=csv.QUOTE_ALL,  # 使用引號包住所有欄位
                               escapechar='\\',        # 使用反斜線作為跳脫字元
                               doublequote=True)       # 使用雙引號處理引號
        return results_df
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception as e:
        print(f"讀取結果數據時出錯: {str(e)}")
        return pd.DataFrame()

def get_statistics_summary(results_df, current_score=None):
    """生成測驗統計摘要，確保所有數值反映100分制的分數"""
    if results_df.empty:
        return {
            "total_students": 0,
            "avg_score": 0,
            "median_score": 0,
            "min_score": 0,
            "max_score": 0,
            "std_dev": 0,
            "pass_rate": 0,
            "all_scores": []
        }
    
    # 確保分數欄位存在且是數值
    if 'score' not in results_df.columns:
        return {
            "total_students": len(results_df),
            "avg_score": 0,
            "median_score": 0,
            "min_score": 0,
            "max_score": 0,
            "std_dev": 0,
            "pass_rate": 0,
            "all_scores": []
        }
    
    # 提取分數，確保是數值類型
    scores = pd.to_numeric(results_df["score"], errors='coerce').fillna(0).values
    
    # 特殊處理：如果只有一位學生
    if len(scores) <= 1:
        return {
            "total_students": len(scores),
            "avg_score": scores[0] if len(scores) == 1 else 0,
            "median_score": scores[0] if len(scores) == 1 else 0,
            "min_score": scores[0] if len(scores) == 1 else 0,
            "max_score": scores[0] if len(scores) == 1 else 0,
            "std_dev": 0,
            "pass_rate": 100 if len(scores) == 1 and scores[0] >= 60 else 0,
            "all_scores": scores.tolist()
        }
    
    # 計算統計量
    total_students = len(scores)
    avg_score = np.mean(scores)
    median_score = np.median(scores)
    min_score = np.min(scores)
    max_score = np.max(scores)
    std_dev = np.std(scores)
    pass_rate = (scores >= 60).mean() * 100
    
    # 返回計算結果
    return {
        "total_students": total_students,
        "avg_score": round(avg_score, 1),
        "median_score": round(median_score, 1),
        "min_score": round(min_score, 1),
        "max_score": round(max_score, 1),
        "std_dev": round(std_dev, 1),
        "pass_rate": round(pass_rate, 1),
        "all_scores": scores.tolist()
    }

def calculate_student_percentile(student_score, all_scores):
    """計算學生在全體中的百分位排名"""
    # 確保所有分數是數值
    all_scores = np.array([float(score) for score in all_scores if not np.isnan(float(score))])
    
    # 如果沒有分數數據
    if len(all_scores) == 0:
        return 50.0
    
    # 如果只有一個分數（只有自己）
    if len(all_scores) == 1:
        return 50.0
    
    # 計算百分位
    lower_scores = sum(1 for score in all_scores if score < student_score)
    same_scores = sum(1 for score in all_scores if score == student_score) - 1  # 減去自己
    
    # 使用插值計算百分位
    percentile = (lower_scores + 0.5 * same_scores) / (len(all_scores) - 1) * 100
    
    return round(percentile, 1)

def get_question_statistics(results_df, questions):
    """分析每個題目的統計數據"""
    if results_df.empty:
        return []
    
    question_stats = []
    for _, question in questions.iterrows():
        qid = str(question['id'])
        col_name = f"q{qid}"
        
        if col_name in results_df.columns:
            # 只計算有效答案
            valid_answers = results_df[col_name].fillna('').replace('', np.nan).dropna()
            total_answered = len(valid_answers)
            
            if total_answered > 0:
                correct_answer = str(question['answer'])
                correct_count = (valid_answers == correct_answer).sum()
                correct_rate = (correct_count / total_answered) * 100
            else:
                correct_rate = 0
        else:
            correct_rate = 0
            
        question_stats.append({
            "id": qid,
            "question": question['question'],
            "correct_rate": correct_rate,
            "difficulty": question['difficulty']
        })
    
    return question_stats

def generate_stats_plots(stats_summary, student_score):
    """生成統計分析圖表，使用箱形圖呈現百分位分佈"""
    plots = {}
    
    # 生成分數分佈直方圖
    if stats_summary["total_students"] > 0:
        # 分數分佈圖
        fig_dist = go.Figure()
        
        # 定義分數區間
        score_ranges = [(0, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
        range_labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
        
        # 計算每個區間的學生人數
        scores = stats_summary.get("all_scores", [])
        if not scores:
            return plots
            
        counts = [0] * len(score_ranges)
        for score in scores:
            for i, (low, high) in enumerate(score_ranges):
                if low <= score <= high:
                    counts[i] += 1
                    break
        
        # 添加分佈柱狀圖
        fig_dist.add_trace(go.Bar(
            x=range_labels,
            y=counts,
            name='學生人數',
            text=counts,
            textposition='auto',
            marker_color='rgba(135, 206, 235, 0.7)'
        ))
        
        # 找出當前學生的分數區間
        student_range_idx = None
        for i, (low, high) in enumerate(score_ranges):
            if low <= student_score <= high:
                student_range_idx = i
                break
        
        if student_range_idx is not None:
            # 在對應的柱子上添加明顯標記
            fig_dist.add_trace(go.Scatter(
                x=[range_labels[student_range_idx]],
                y=[counts[student_range_idx]],
                mode='markers+text',
                name='您的位置',
                text=['您的位置'],
                textposition='top center',
                textfont=dict(size=14, color='red', family='Arial Black'),
                marker=dict(
                    color='red',
                    size=15,
                    symbol='star',
                    line=dict(width=2, color='darkred')
                )
            ))
            
            # 添加文本說明您的成績
            fig_dist.add_annotation(
                x=range_labels[student_range_idx],
                y=counts[student_range_idx] + 0.3,
                text=f"您的成績: {student_score}分",
                showarrow=True,
                arrowhead=1,
                arrowcolor="red",
                arrowsize=1,
                arrowwidth=2,
                font=dict(color="red", size=14),
                bgcolor="white",
                bordercolor="red",
                borderwidth=2,
                borderpad=4,
                ax=0,
                ay=-40
            )
        
        # 更新布局
        fig_dist.update_layout(
            title=f'分數分佈 (總人數: {stats_summary["total_students"]}人)',
            xaxis_title='分數區間',
            yaxis_title='學生人數',
            template='plotly_white',
            showlegend=True,
            legend=dict(
                x=1.02,  # 將圖例移到圖表右側
                y=1,
                xanchor='left',
                yanchor='top',
                font=dict(size=14)  # 增加圖例字體大小
            ),
            # 調整y軸刻度為整數
            yaxis=dict(
                dtick=1,  # 設置刻度間隔為1
                range=[0, max(counts) + 1.5],  # 擴大y軸範圍以容納標記
                title_font=dict(size=16),  # 增加Y軸標題字體大小
                tickfont=dict(size=14)  # 增加Y軸刻度字體大小
            ),
            xaxis=dict(
                title_font=dict(size=16),  # 增加X軸標題字體大小
                tickfont=dict(size=14)  # 增加X軸刻度字體大小
            ),
            # 調整邊距以容納右側圖例
            margin=dict(r=150, t=100, b=100),
            title_font=dict(size=18),  # 增加圖表標題字體大小
            font=dict(family="Arial, sans-serif")  # 設定全局字體
        )
        
        plots["distribution"] = fig_dist
        
        # 百分位圖 - 改為箱形圖呈現
        fig_perc = go.Figure()
        
        # 獲取實際分數數據
        scores = stats_summary.get("all_scores", [])
        
        # 判斷數據點數量，選擇呈現方式
        if len(scores) <= 2:  # 如果只有1-2個數據點
            # 使用散點圖而非箱形圖
            
            # 計算學生百分位（如果只有一個數據點，則設為50%）
            if len(scores) == 1:
                student_percentile = 50
            else:
                student_percentile = stats.percentileofscore(scores, student_score)
            
            # 添加說明文字
            fig_perc.add_annotation(
                x=0.5,
                y=0.95,
                xref="paper",
                yref="paper",
                text="目前數據點過少，無法生成有意義的箱形圖",
                showarrow=False,
                font=dict(size=14, color="red"),
                bgcolor="lightyellow",
                bordercolor="red",
                borderwidth=1,
                borderpad=4
            )
            
            # 只顯示當前學生的位置
            fig_perc.add_trace(
                go.Scatter(
                    x=["您的成績"],
                    y=[student_score],
                    mode='markers+text',
                    name='您的位置',
                    text=[f"{student_score}分"],
                    textposition='top center',
                    textfont=dict(size=14, color='red'),
                    marker=dict(
                        color='red',
                        size=15,
                        symbol='star',
                        line=dict(width=2, color='darkred')
                    )
                )
            )
            
            # 顯示其他學生分數（如果有）
            if len(scores) == 2:
                other_score = scores[0] if abs(scores[0] - student_score) > 0.01 else scores[1]
                fig_perc.add_trace(
                    go.Scatter(
                        x=["其他學生"],
                        y=[other_score],
                        mode='markers+text',
                        name='其他學生',
                        text=[f"{other_score}分"],
                        textposition='top center',
                        textfont=dict(size=14, color='blue'),
                        marker=dict(
                            color='blue',
                            size=15,
                            symbol='circle',
                            line=dict(width=2, color='darkblue')
                        )
                    )
                )
            
            # 顯示及格線
            fig_perc.add_shape(
                type="line",
                x0=-0.5,
                y0=60,
                x1=1.5,
                y1=60,
                line=dict(color="green", width=1, dash="dash")
            )
            fig_perc.add_annotation(
                x=0,
                y=60,
                text="及格線",
                showarrow=False,
                font=dict(color="green")
            )
            
            # 更新布局
            fig_perc.update_layout(
                title='成績分佈 (數據參考點不足)',
                yaxis_title='分數',
                template='plotly_white',
                showlegend=True,
                legend=dict(
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                    font=dict(size=14)  # 增加圖例字體大小
                ),
                yaxis=dict(
                    range=[0, 100],
                    dtick=10,
                    gridcolor='lightgray',
                    title_font=dict(size=16),  # 增加Y軸標題字體大小
                    tickfont=dict(size=14)  # 增加Y軸刻度字體大小
                ),
                xaxis=dict(
                    tickfont=dict(size=14)  # 增加X軸刻度字體大小
                ),
                margin=dict(r=150, t=100, b=100),
                plot_bgcolor='rgba(240,240,240,0.1)',
                title_font=dict(size=18),  # 增加圖表標題字體大小
                font=dict(family="Arial, sans-serif")  # 設定全局字體
            )
            
        else:
            # 足夠數據點時，使用箱形圖
            
            # 計算當前學生的百分位
            student_percentile = stats.percentileofscore(scores, student_score)
            
            # 添加箱形圖
            fig_perc.add_trace(
                go.Box(
                    y=scores,
                    name='班級成績分佈',
                    boxmean=True,  # 顯示均值
                    marker_color='lightblue',
                    boxpoints='all',  # 顯示所有點
                    jitter=0.3,  # 點的散布範圍
                    pointpos=-1.8,  # 點的位置
                    marker=dict(
                        color='royalblue',
                        size=8,
                        opacity=0.6
                    ),
                    line=dict(color='royalblue')
                )
            )
            
            # 標記當前學生的位置
            fig_perc.add_trace(
                go.Scatter(
                    x=[0],  # x=0 表示在箱形圖中央
                    y=[student_score],
                    mode='markers+text',
                    name='您的位置',
                    text=[f"{student_score}分 (第{student_percentile:.1f}百分位)"],
                    textposition='top right',
                    textfont=dict(size=14, color='red'),
                    marker=dict(
                        color='red',
                        size=15,
                        symbol='star',
                        line=dict(width=2, color='darkred')
                    )
                )
            )
            
            # 添加統計數據標記
            # 計算四分位數
            q1 = np.percentile(scores, 25)
            median = np.percentile(scores, 50)
            q3 = np.percentile(scores, 75)
            min_val = np.min(scores)
            max_val = np.max(scores)
            mean_val = np.mean(scores)
            
            # 添加均值標記
            fig_perc.add_annotation(
                x=0.25,
                y=mean_val,
                text=f"平均分: {mean_val:.1f}",
                showarrow=True,
                arrowhead=1,
                arrowcolor="blue",
                arrowsize=1,
                arrowwidth=1,
                font=dict(size=12, color="blue"),
                align="left"
            )
            
            # 添加中位數標記
            fig_perc.add_annotation(
                x=0.25,
                y=median,
                text=f"中位數: {median:.1f}",
                showarrow=True,
                arrowhead=1,
                arrowcolor="purple",
                arrowsize=1,
                arrowwidth=1,
                font=dict(size=12, color="purple"),
                align="left"
            )
            
            # 添加說明標記
            fig_perc.add_annotation(
                x=0,
                y=max_val + 5,
                text="箱形圖說明：框內範圍為中間50%的學生分數<br>中線為中位數，菱形為平均分",
                showarrow=False,
                font=dict(size=12),
                bgcolor="lightyellow",
                bordercolor="gray",
                borderwidth=1,
                borderpad=4,
                align="left"
            )
            
            # 顯示及格線
            fig_perc.add_shape(
                type="line",
                x0=-0.5,
                y0=60,
                x1=0.5,
                y1=60,
                line=dict(color="green", width=1, dash="dash")
            )
            fig_perc.add_annotation(
                x=-0.4,
                y=60,
                text="及格線",
                showarrow=False,
                font=dict(color="green")
            )
            
            # 更新布局
            fig_perc.update_layout(
                title=f'班級成績分佈 (箱形圖)',
                yaxis_title='分數',
                template='plotly_white',
                showlegend=True,
                legend=dict(
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                    font=dict(size=14)  # 增加圖例字體大小
                ),
                xaxis=dict(
                    showticklabels=False,  # 隱藏X軸刻度標籤
                    title_font=dict(size=16)  # 增加X軸標題字體大小
                ),
                yaxis=dict(
                    range=[0, max(max_val + 10, 100)],  # 確保Y軸範圍合適
                    dtick=10,
                    gridcolor='lightgray',
                    title_font=dict(size=16),  # 增加Y軸標題字體大小
                    tickfont=dict(size=14)  # 增加Y軸刻度字體大小
                ),
                margin=dict(r=150, t=100, b=50),
                plot_bgcolor='rgba(240,240,240,0.1)',
                title_font=dict(size=18),  # 增加圖表標題字體大小
                font=dict(family="Arial, sans-serif")  # 設定全局字體
            )
        
        plots["percentiles"] = fig_perc
    
    return plots

# 讀取班級設定
def load_class_config():
    if os.path.exists('class_config.json'):
        with open('class_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"total_students": 30, "class_list": []}

# 初始化或讀取考試數據
def load_quiz_data():
    if os.path.exists('quiz_data.json'):
        with open('quiz_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# 保存考試數據
def save_quiz_data(data):
    with open('quiz_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 計算統計數據
def calculate_statistics(quiz_data, total_students):
    if not quiz_data:
        return pd.DataFrame()
    
    df = pd.DataFrame(quiz_data)
    
    # 計算參加考試人數
    attended_count = len(df)
    # 計算缺考人數
    absent_count = total_students - attended_count
    
    # 基本統計
    stats = {
        '總人數': total_students,
        '參加考試人數': attended_count,
        '缺考人數': absent_count,
        '平均分數': round(df['score'].mean(), 2) if not df.empty else 0,
        '最高分': df['score'].max() if not df.empty else 0,
        '最低分': df['score'].min() if not df.empty else 0
    }
    
    # 分數區間統計
    score_ranges = {
        '90分以上': len(df[df['score'] >= 90]),
        '80-89分': len(df[(df['score'] >= 80) & (df['score'] < 90)]),
        '70-79分': len(df[(df['score'] >= 70) & (df['score'] < 80)]),
        '60-69分': len(df[(df['score'] >= 60) & (df['score'] < 70)]),
        '60分以下': len(df[df['score'] < 60]),
        '缺考': absent_count
    }
    
    return pd.DataFrame([stats]), pd.DataFrame([score_ranges])

def calculate_category_stats(questions_df, results_df, current_results):
    """計算每個類別的統計數據，確保個人和班級平均正確率計算方式統一"""
    try:
        if not isinstance(questions_df, pd.DataFrame):
            print("Warning: questions_df is not a DataFrame")
            return []
        
        # 檢查必要的列是否存在
        required_columns = ['id', 'category', 'answer', 'difficulty']
        if not all(col in questions_df.columns for col in required_columns):
            print(f"Missing required columns. Available columns: {questions_df.columns.tolist()}")
            return []
        
        # 定義難度權重（用於分數計算，但不影響正確率計算）
        difficulty_weights = {
            "簡單": 5,
            "中等": 10,
            "困難": 15
        }
        
        categories = questions_df['category'].unique()
        category_stats = []
        
        for category in categories:
            try:
                # 獲取此類別的所有題目
                cat_questions = questions_df[questions_df['category'] == category]
                cat_question_ids = cat_questions['id'].tolist()
                total_questions_in_category = len(cat_question_ids)
                
                # 計算個人在此類別的得分和答對數
                personal_points = 0
                personal_correct = 0
                questions_answered = 0
                
                # 班級統計變數
                class_correct_sum = 0
                class_total_sum = 0
                
                for _, question in cat_questions.iterrows():
                    qid = str(question['id'])
                    weight = difficulty_weights[question['difficulty']]
                    
                    # 計算個人成績
                    result = next((r for r in current_results if str(r['id']) == qid), None)
                    if result:
                        questions_answered += 1
                        if result.get('is_correct'):
                            personal_points += weight
                            personal_correct += 1
                    
                    # 計算班級平均 - 使用答對人數/總人數
                    col_name = f'q{qid}'
                    if col_name in results_df.columns:
                        correct_answer = str(question['answer']).strip().lower()
                        total_students = len(results_df)
                        
                        if total_students > 0:
                            # 計算答對此題的學生數
                            correct_count = sum(
                                str(ans).strip().lower() == correct_answer 
                                for ans in results_df[col_name] if pd.notna(ans)
                            )
                            # 累計班級答對數和題目數
                            class_correct_sum += correct_count
                            class_total_sum += total_students
                
                # 計算百分比 - 確保正確率基於答對題數除以總題數
                personal_rate = (personal_correct / total_questions_in_category * 100) if total_questions_in_category > 0 else 0
                
                # 班級平均正確率 - 使用班級總答對數除以總題數*學生數
                class_rate = (class_correct_sum / class_total_sum * 100) if class_total_sum > 0 else 0
                
                # 如果只有一位學生，班級平均應該等於個人成績
                if len(results_df) == 1:
                    class_rate = personal_rate
                
                # 計算基於權重的分數總值（僅用於顯示分數，不影響正確率）
                category_total_points = sum(difficulty_weights[q['difficulty']] 
                                         for _, q in cat_questions.iterrows())
                
                # 添加調試信息
                print(f"Category {category}: personal_correct={personal_correct}/{total_questions_in_category}={personal_rate:.1f}%, "
                      f"class_correct_sum={class_correct_sum}, class_total_sum={class_total_sum}, class_rate={class_rate:.1f}%")
                
                category_stats.append({
                    "category": category,
                    "personal_rate": round(personal_rate, 1),
                    "class_rate": round(class_rate, 1),
                    "total_questions": total_questions_in_category,
                    "personal_correct": personal_correct,
                    "total_points": category_total_points,
                    "personal_points": personal_points,
                    "answered": questions_answered,
                    "class_correct_sum": class_correct_sum,
                    "class_total_sum": class_total_sum
                })
                
            except Exception as e:
                print(f"Error processing category {category}: {str(e)}")
                continue
        
        return category_stats
        
    except Exception as e:
        print(f"Error in calculate_category_stats: {str(e)}")
        return []

# 使用 JavaScript 實現倒計時，減少伺服器端負擔
def countdown_timer(duration_sec, key="timer"):
    """使用 JavaScript 實現倒計時"""
    
    timer_js = f"""
    <div id="{key}">
        <h2 id="timer-display">剩餘時間: {duration_sec // 60:02d}:{duration_sec % 60:02d}</h2>
    </div>
    
    <script>
        // 設定倒計時
        var duration = {duration_sec};
        var timer = duration;
        var minutes, seconds;
        
        // 更新計時器顯示
        function updateTimer() {{
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);
            
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;
            
            document.getElementById("timer-display").textContent = "剩餘時間: " + minutes + ":" + seconds;
            
            if (--timer < 0) {{
                // 時間到，提交表單
                document.getElementById("timer-display").textContent = "時間到！正在提交...";
                document.getElementById("timer-display").style.color = "red";
                
                // 自動點擊提交按鈕（如果存在）
                var submitButton = document.querySelector('button[kind="primary"]');
                if (submitButton) {{
                    submitButton.click();
                }}
                
                clearInterval(interval);
            }}
        }}
        
        // 初始顯示
        updateTimer();
        
        // 每秒更新一次
        var interval = setInterval(updateTimer, 1000);
    </script>
    """
    
    st.markdown(timer_js, unsafe_allow_html=True)

# 完整實現班級知識點掌握程度圖表 - 使用50%水位線
def create_category_charts_with_baseline(categories, rates, title="班級知識點掌握程度 (由高到低排序)"):
    """創建帶有50%水位線的類別圖表"""
    # 創建條形圖
    fig = go.Figure()
    
    # 設置條形顏色：高於50%為綠色，低於為紅色
    bar_colors = ['rgba(60, 179, 113, 0.6)' if rate >= 50 else 'rgba(255, 99, 71, 0.6)' for rate in rates]
    
    # 添加條形
    fig.add_trace(go.Bar(
        x=categories,
        y=rates,
        marker_color=bar_colors,
        text=[f"{rate:.1f}%" for rate in rates],
        textposition='auto',
        hoverinfo='text',
        hovertext=[f"{cat}: {rate:.1f}%" for cat, rate in zip(categories, rates)]
    ))
    
    # 添加一條50%的水平參考線
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=50,
        x1=len(categories)-0.5,
        y1=50,
        line=dict(
            color="black",
            width=1.5,
            dash="dash",
        )
    )
    
    # 添加水位線標籤
    fig.add_annotation(
        x=len(categories)-0.5,
        y=50,
        text="及格水位線: 50.0%",
        showarrow=False,
        font=dict(
            size=12,
            color="black"
        ),
        bgcolor="white",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        xanchor="right"
    )
    
    # 更新布局
    fig.update_layout(
        title=title,
        yaxis=dict(
            title='正確率 (%)',
            range=[0, max(max(rates) + 10, 100)],
            dtick=20,
            ticksuffix="%",
            tickfont=dict(size=14)
        ),
        xaxis=dict(
            title='知識點類別',
            tickfont=dict(size=14)
        ),
        plot_bgcolor='rgba(245,245,245,0.5)',
        height=500,
        margin=dict(l=50, r=50, t=80, b=80),
        template='plotly_white',
        title_font=dict(size=18)
    )
    
    return fig

# 修改班級強弱項分析部分，使用50%作為強弱項判斷標準
def display_class_analysis(questions, results_df):
    # 顯示班級整體統計信息
    st.subheader("📊 班級強弱項分析")
    
    # 如果沒有測驗數據，顯示提示訊息
    if results_df.empty:
        st.info("暫無班級數據")
        return
    
    # 計算班級整體正確率
    class_stats = get_category_statistics(questions, results_df)
    if not class_stats:
        st.info("暫無類別數據")
        return
    
    # 計算平均正確率
    overall_rate = sum(stat['correct_rate'] for stat in class_stats.values()) / len(class_stats) if class_stats else 0
    
    # 顯示班級整體正確率
    st.info(f"📊 班級整體平均正確率: {overall_rate:.1f}%")
    
    # 計算各類別統計
    category_stats = []
    for category, stats in class_stats.items():
        category_stats.append({
            "category": category,
            "class_rate": round(stats["correct_rate"], 1),
            "total_questions": questions[questions["category"] == category].shape[0],
        })
    
    # 正確提取類別名稱和正確率
    categories = [stat["category"] for stat in category_stats]
    rates = [stat["class_rate"] for stat in category_stats]
    
    # 使用新的圖表函數，基於50%水位線
    if categories and rates:
        # 根據正確率排序（從高到低）
        sorted_indices = np.argsort(rates)[::-1]
        sorted_categories = [categories[i] for i in sorted_indices]
        sorted_rates = [rates[i] for i in sorted_indices]
        
        # 創建並顯示圖表
        strength_fig = create_category_charts_with_baseline(sorted_categories, sorted_rates)
        st.plotly_chart(strength_fig, use_container_width=True)
    else:
        st.warning("無法生成圖表：沒有足夠的類別數據")
    
    # 顯示強弱項分析文字說明
    col1, col2 = st.columns(2)
    
    # 根據50%水位線顯示強項和弱項
    strong_categories = [stat for stat in category_stats if stat["class_rate"] >= 50]
    weak_categories = [stat for stat in category_stats if stat["class_rate"] < 50]
    
    # 按正確率排序
    strong_categories.sort(key=lambda x: x["class_rate"], reverse=True)
    weak_categories.sort(key=lambda x: x["class_rate"])
    
    # 顯示強項
    with col1:
        st.write("##### 💪 班級強項")
        if strong_categories:
            for stat in strong_categories:
                st.success(f"- **{stat['category']}** (正確率: {stat['class_rate']}%, 高於及格線 {stat['class_rate']-50:.1f}%)")
        else:
            st.info("沒有高於50%及格線的類別")
    
    # 顯示弱項
    with col2:
        st.write("##### 📚 需要加強")
        if weak_categories:
            for stat in weak_categories:
                st.error(f"- **{stat['category']}** (正確率: {stat['class_rate']}%, 低於及格線 {50-stat['class_rate']:.1f}%)")
        else:
            st.info("沒有明顯的弱項類別")
    
    # 提供教學建議
    st.write("##### 📝 教學建議")
    if weak_categories:
        st.warning(f"根據分析結果，建議加強以下知識點的教學：{', '.join([cat['category'] for cat in weak_categories])}")
        st.write("可採取的措施：")
        st.write("1. 針對弱項類別提供額外的練習題")
        st.write("2. 安排專門的複習課程，針對性講解難點")
        st.write("3. 提供更多實例和應用場景，加深理解")
    else:
        st.success("所有類別都高於及格線，建議繼續鞏固現有知識並適當提高難度")

if __name__ == "__main__":
    main()
