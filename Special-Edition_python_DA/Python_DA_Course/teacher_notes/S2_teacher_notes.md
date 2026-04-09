# S2 — Pandas I/O 與資料清理｜講師講稿

> **課程時長**：2 小時（講授 70 min + 課堂練習 40 min + QA 10 min）
> **對應 Notebook**：`M2_Pandas_Basic/S2_pandas_io_cleaning.ipynb`

---

## 1. 本節目標 (Learning Objectives)

完成本節後，學員應能：

1. 區分 `DataFrame` 與 `Series`，並說明「索引 (index)」在 Pandas 中扮演的角色。
2. 使用 `read_csv` / `read_excel` 讀檔，並用「五件事探索法」（`shape` / `head` / `info` / `describe` / `isna().sum()`）快速盤點資料狀況。
3. 正確使用 `loc` 與 `iloc` 進行列／欄選取，理解「標籤 vs 位置」差異。
4. 執行資料清理四大手法：欄名標準化、型別轉換、缺值處理、重複列移除。
5. 把真實髒檔 `orders_raw.csv` 清成可分析的乾淨 DataFrame，並輸出 `orders_clean.csv` 完成一次微型 ETL。

---

## 2. 時間切分表

```
00:00-00:05  開場暖身：上節 NumPy 回顧 + 「資料科學家 80% 時間在清資料」的現實
00:05-00:20  核心觀念 1/4：DataFrame / Series / Index 三件套
00:20-00:35  核心觀念 2/4：read_csv 常用參數（encoding, sep, dtype, parse_dates）
00:35-00:50  核心觀念 3/4：loc vs iloc（最易混淆，務必 demo 清楚）
00:50-01:10  核心觀念 4/4：清理四大手法 + orders_raw 實務 Case 走一次 Step 1~7
01:10-01:50  課堂練習（40 min）：🟡 核心清理題 + 🔴 封裝 clean_orders() 函式挑戰題
01:50-02:00  QA + 下節預告（S3 groupby / merge / pivot）
```

---

## 3. 關鍵教學點 (Key Teaching Points)

1. **拿到新檔案的 SOP**：永遠先跑 `df.shape → df.head() → df.info() → df.describe() → df.isna().sum()` 這五行。這是 senior 和 junior 的差別。
2. **`errors='coerce'` 的哲學**：`pd.to_datetime(x, errors='coerce')` 與 `pd.to_numeric(x, errors='coerce')` 會把不合法值轉成 `NaT` / `NaN` 而不是爆掉。這是處理髒資料的救命符，但也意味著「失敗會悄悄發生」——清完務必檢查缺值數。
3. **`loc` vs `iloc`**：`loc` 是標籤 (label-based)、`iloc` 是位置 (integer-based)。`df.loc[0]` 在 index 被重設後會是不同的列。務必用 `df.set_index('id')` 後的情境展示差異。
4. **欄名標準化是「免費」的投資**：`df.columns.str.strip().str.lower().str.replace(' ', '_')` 三行下去，後面所有程式碼都不會因為 `Customer ID` vs `customer_id` 而崩潰。
5. **缺值處理沒有標準答案**：要依欄位意義決定——訂單日期缺失無法做時序分析，直接丟；金額缺失可用中位數補；類別缺失可補 `'Unknown'`。不要無腦 `dropna()` 或 `fillna(0)`。

---

## 4. 學員常犯錯誤 (Common Pitfalls)

- **忘了 `errors='coerce'`**：`pd.to_datetime(df['date'])` 遇到一筆 `'2023/13/45'` 就整批 raise，導致以為清完但什麼都沒動。
- **字串金額直接 astype(float)**：`'$1,355'` 會爆炸；要先 `.str.replace('$','').str.replace(',','')`。
- **`loc` 寫成 `iloc`**：`df.iloc[df['age']>18]` 會 raise（布林條件要用 `loc`）。
- **inplace=True 的濫用**：`df.drop(..., inplace=True)` 在新版 Pandas 已不建議，且常讓人搞不清楚變數狀態；改用賦值寫法。
- **`df.append()`**：已 deprecated，請用 `pd.concat()`。
- **讀 CSV 不指定 encoding**：Windows 中文檔常需 `encoding='utf-8-sig'` 或 `'big5'`。

---

## 5. 提問設計 (Discussion Prompts)

1. 如果一份 100 萬筆的訂單檔，有 5% 訂單缺 `amount`、3% 缺 `order_date`、1% 缺 `customer_id`，你會如何決定各欄位的處理策略？依據是什麼？
2. `loc` 和 `iloc` 看起來很像，為什麼 Pandas 要故意設計兩個？只保留一個會有什麼問題？
3. 清完的資料要不要覆蓋原始檔？還是另存新檔？在團隊協作時哪種做法比較安全？

---

## 6. 延伸資源 (Further Reading)

- Pandas 官方 User Guide「IO tools (text, CSV, HDF5, …)」與「Working with missing data」章節（可在 pandas.pydata.org 搜尋）。
- 查詢 Pandas 官方 Cookbook 的 Data Cleaning 範例。

---

## 7. 常見 Q&A

**Q1：`dropna()` 和 `fillna()` 哪個比較好？**
A：沒有絕對答案，要看「缺值原因」。如果缺值是隨機的小比例（< 5%），`dropna` 省事；如果是系統性缺失或資料稀缺，`fillna` 配合領域知識（中位數、前值、分群平均）更好。

**Q2：`pd.read_csv` 讀超大檔案記憶體爆掉怎辦？**
A：用 `chunksize=100000` 分批讀、`usecols=[...]` 只讀需要的欄、`dtype={...}` 指定型別（字串欄改 `category` 可省很多記憶體）。

**Q3：清理完該存 CSV 還是 Parquet？**
A：給其他人看用 CSV、自己跑分析用 Parquet（檔案小 5~10 倍、讀取快、保留 dtype）。本課為了簡單都用 CSV。
