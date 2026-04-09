# S6 講師講稿 — Plotly 互動 + 完整 Capstone 案例

> 對應 notebook：`M6_Plotly_Projects/S6_plotly_capstone.ipynb`
> 節次時長：120 分鐘（講授 60 + 實作 50 + 成果發表 10）

---

## 1. 本節目標

1. 學會 Plotly Express 6 個常用函式：`px.line / px.bar / px.scatter / px.box / px.histogram / px.pie`。
2. 理解「靜態圖（S5）vs 互動圖（S6）」的使用場景與交付差異（.png vs .html）。
3. 會用 `make_subplots + add_trace` 組合 2x2 互動儀表板，包含 xy 與 domain 混合。
4. 能從 `orders_raw.csv` 獨立走一遍 S2→S3→S4→S6 全流程，輸出 `dashboard.html`。
5. 透過 3 分鐘成果發表，培養用一句話講清楚「發現、行動、價值」的溝通力。

## 2. 時間切分表（60 + 50 + 10）

| 時間 | 區段 | 內容 |
|---|---|---|
| 0~5 | 講授 | 為什麼這是 Capstone：把 S1~S5 串成一個產品 |
| 5~10 | 講授 | Plotly 與 matplotlib/seaborn 的核心差異（互動、hover、HTML） |
| 10~35 | 講授 | Part A：6 個 px 函式現場示範（line/bar/scatter/box/hist/pie） |
| 35~50 | 講授 | Part B Step1~3：clean → merge → KPIs |
| 50~60 | 講授 | Part B Step4~5：`make_subplots` 2x2 + `write_html` |
| 60~110 | 實作 | 學員獨立跑完整流程，講師巡場答疑 |
| 110~120 | 成果發表 | 每人 30 秒：發現、下一步、應用場景 |

## 3. 關鍵教學點

- **Plotly Express vs graph_objects**：px 是高階 API（一行畫一張），go 是底層可完全客製。`make_subplots` 必須搭 go。
- **`specs` 的 domain vs xy**：`px.pie` 使用 domain 類型，放進 subplot 時 `specs` 要寫 `{'type':'domain'}`，其他圖是 `{'type':'xy'}`。這是本節最常出錯的點。
- **`write_html` 的魔力**：輸出一個可寄出去的單一 HTML 檔，不需要對方裝 Python。強調這是 DA 的「成品交付」標準動作。
- **Capstone 的精神**：不要開 S2/S3 的 notebook 抄，逼學員從頭寫一次 `load_and_clean_orders` 函式，驗證是否真的學會。

## 4. 成果發表流程（10 min）

1. **每人 30 秒、依座位順序**，不提問以節省時間。
2. 三個必答問題：
   - 今天儀表板**最關鍵的發現**是什麼？（1 個數字 + 1 個解讀）
   - 再給你 1 小時，你會新增哪張圖？
   - 這個流程在你未來工作會用在哪？
3. 講師現場打分（見下方評分建議）。
4. 最後 2 分鐘選 1~2 位示範作品，投影到大螢幕輪播。

## 5. 成果發表評分建議（簡易版，與 GRADING_RUBRIC 呼應）

| 面向 | 配分 | 評分重點 |
|---|---|---|
| 技術完成度 | 40% | 流程是否跑完 S2→S6，dashboard.html 能否開啟、4 張子圖都有資料 |
| 洞察品質 | 30% | 是否指出至少 1 個具體數字結論（非「營收不錯」這種空話） |
| 視覺呈現 | 20% | 排版、配色、subplot_titles、hover 是否有意義 |
| 口語表達 | 10% | 30 秒內是否講清楚「發現 + 行動」 |

- A (90+)：全部 4 面向達標，洞察有驚喜
- B (75~89)：技術完成、洞察普通
- C (60~74)：儀表板能跑但有明顯錯誤或缺圖
- F (<60)：未完成或僅複製貼上

## 6. 學員常犯錯誤

1. **Plotly subplot 混 domain/xy 時 `specs` 寫錯**：`px.pie`/`go.Pie` 放進 subplot 一定要指定 `{'type':'domain'}`，否則會出 `ValueError: Trace type 'pie' is not compatible with subplot type 'xy'`。
2. **`px` 圖直接 `add_trace` 到 subplot**：`px` 回傳的是 Figure 而不是 trace，正確做法是取出 `fig.data[0]` 或直接用 `go.Scatter`、`go.Bar`。
3. **`write_html` 存檔後在瀏覽器打不開**：路徑相對於 notebook 目錄，請用絕對路徑或先 `os.path.abspath` 確認。
4. **`load_and_clean_orders` 忘了 `errors='coerce'`**：遇到髒日期直接噴錯，讓學員體會「為什麼要 coerce」。
5. **subplot 只有一張圖顯示**：忘了 `row`、`col` 參數或所有 trace 都指到 `row=1, col=1`。
6. **hover_data 塞太多欄**：變成一坨資訊牆，建議挑 2~3 個最有商業意義的欄位。

## 7. 提問設計

1. 「S5 的 matplotlib 儀表板可以做成 HTML 嗎？如果老闆要一個『能自己點』的版本，你會怎麼給他？」
2. 「為什麼 Capstone 不讓你直接 import S3 的 notebook，而是要重寫一次？」
3. 「這份 dashboard.html 寄給非技術的行銷主管，你會在 email 裡附上哪 3 句話來引導他看？」

## 8. 延伸資源

- Plotly 官方 Python 文件的 Plotly Express 章節（搜尋 "plotly express python"）。
- Plotly 官方的 subplots 與 mixed subplot types 教學頁（搜尋 "plotly python subplots"）。

## 9. 常見 Q&A

- **Q：Plotly 圖太慢，資料超過 10 萬筆怎麼辦？**
  A：px 預設會把所有點塞進 HTML，資料量大請先 `.sample()` 或聚合後再畫，或改用 `plotly.graph_objects` + `scattergl`。
- **Q：dashboard.html 可以放到公司內網嗎？**
  A：可以，它是純靜態 HTML + JS，丟到任何 static hosting 都能開。
- **Q：Capstone 做完還想更進階，下一步學什麼？**
  A：Streamlit（把 notebook 變 Web App）、Dash（Plotly 官方框架）、或學 SQL 把資料源從 CSV 換成資料庫。

## 10. 收斂金句

「12 小時課程的終點不是『你會用 Plotly』，而是『你能獨立把一份髒 CSV 變成老闆願意轉寄的 dashboard』。這才是 DA 的商業價值。」
