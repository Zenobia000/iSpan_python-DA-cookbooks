# S4 講師講稿 — 時間序列 + EDA 實戰

> 對應 notebook：`M3_Pandas_Advanced/S4_timeseries_eda.ipynb`
> 節次時長：120 分鐘（講授 70 + 練習 40 + 收斂 10）

---

## 1. 本節目標

1. 讓學員理解「商業問題幾乎都有時間維度」，能用 `.dt` accessor 快速拆年月日。
2. 掌握 `resample`（需 datetime index）與 `groupby + to_period` 兩條路徑的差別與適用場景。
3. 會用 `rolling(window).mean()` 對雜訊資料做平滑並解讀趨勢。
4. 熟練 EDA 三板斧：`describe`、`value_counts`、`corr`，並能口語化解讀相關係數。
5. 能產出一張「月度經營報表」，把技術能力對應到真實 DA 工作產出。

## 2. 時間切分表

| 時間 | 內容 | 備註 |
|---|---|---|
| 0~10 | 上節回顧 + 情境引入（老闆四問） | 強調「時間維度」是所有 DA 問題的底層 |
| 10~20 | 日期操作：`to_datetime`、`.dt.year/month/day_name/to_period` | 現場示範 Excel vs Pandas |
| 20~35 | `resample` 三種粒度（D/W/ME），強調 index 必須是 datetime | 示範 sort_index 必要性 |
| 35~45 | `rolling` 移動平均，平滑日資料雜訊 | 對比 window=3 與 window=7 |
| 45~60 | EDA 三招：`describe` / `value_counts` / `corr` | 解讀相關係數的三段式口訣 |
| 60~70 | 實務 Case：月度、星期幾、地區×品類熱點 | 產出 monthly_revenue.csv 給 S5/S6 接手 |
| 70~110 | 課堂練習（送分/核心/挑戰三層） | 挑戰題 = 月度經營報表 |
| 110~120 | 小結、速查表、S5 預告 | 強調「數字不會說話，圖會」 |

## 3. 關鍵教學點

- **`resample` vs `groupby + to_period`**：`resample` 只能用在 datetime index 且支援填補空缺日期（頻率型），適合時序；`groupby('year_mon')` 則是把期間當作類別鍵，缺月份不會自動補 0。教學時兩種都示範，讓學員理解報表類用後者、趨勢圖類用前者。
- **`'M'` vs `'ME'`**：pandas 2.2+ 後 `'M'` 被 deprecation 警告，改用 `'ME'`（Month End）、`'QE'`、`'YE'`。務必當場秀出警告訊息。
- **`rolling` 的 window 意義**：N=7 代表包含當日往前數 7 天，前 N-1 列為 NaN，這是學員常問的點。
- **相關係數解讀**：用「>0.7 強 / 0.3~0.7 中 / <0.3 弱」三段式，不要讓學員只看數字不說結論。

## 4. 學員常犯錯誤

1. **忘了 `sort_index()`**：`resample` 或 `rolling` 在未排序的 index 上會得到錯誤結果，要求所有人先 `set_index('order_date').sort_index()`。
2. **`parse_dates` 漏掉**：`pd.read_csv` 沒帶 `parse_dates=['order_date']` 直接用 `.dt` 會噴 `AttributeError: Can only use .dt accessor with datetimelike values`。
3. **`resample` 誤用在沒有 datetime index 的 DataFrame**：錯誤訊息 `TypeError: Only valid with DatetimeIndex`。
4. **星期排序混亂**：`groupby('weekday')` 後直接畫圖會變成字母序（Friday 排在最前），要 `.reindex(week_order)`。
5. **`to_period('M')` 的型別陷阱**：`Period` 物件在寫入 CSV 或 merge 時常出狀況，若要視覺化記得 `.astype(str)`。

## 5. 提問設計

1. 「如果我想知道『每週一的平均銷售』，該用 `resample` 還是 `groupby`？為什麼？」
2. 「相關係數 0.65 算強還是中？你會怎麼對老闆描述這個關係？」
3. 「為什麼挑戰題的月度報表裡，第一個月的成長率會是 NaN？這個 NaN 要不要補 0？」

## 6. 延伸資源

- pandas 官方文件：Time series / date functionality 章節（搜尋 "pandas timeseries user guide"）。
- 書籍：《Python for Data Analysis》3rd ed.（Wes McKinney）第 11 章 Time Series。

## 7. 常見 Q&A

- **Q：`resample('M')` 和 `resample('ME')` 到底差在哪？**
  A：結果相同，但 `'M'` 從 pandas 2.2 起會警告並在未來版本移除，請直接用 `'ME'`。
- **Q：`rolling(7).mean()` 前 6 列是 NaN，要怎麼處理？**
  A：畫圖時可以 `.dropna()`；若要保留長度可加 `min_periods=1`，但要提醒學員這會讓前幾個值失真。
- **Q：`corr()` 只算數值欄，類別欄要怎麼看相關？**
  A：本節不深入，可先提「類別看 `crosstab` 或卡方檢定」，留給進階課。

## 8. 收斂金句

「S4 教你把時間變成一條軸、把 EDA 變成一種直覺。下一節 S5，我們把這些數字畫出來，才算真正完成一份 DA 作品。」
