# S1 — NumPy 與向量化思維｜講師講稿

> **課程時長**：2 小時（講授 70 min + 課堂練習 40 min + QA 10 min）
> **對應 Notebook**：`M1_Numpy_Basic/S1_numpy_vectorization.ipynb`

---

## 1. 本節目標 (Learning Objectives)

完成本節後，學員應能：

1. 使用 `np.array()` 建立 1D/2D ndarray，並說明 `.shape`、`.dtype`、`.ndim` 的意義。
2. 運用切片、布林遮罩（boolean mask）與 fancy indexing 篩選陣列資料。
3. 解釋「向量化 (vectorization)」為何比 Python `for-loop` 快 10~100 倍，並實際量測證明。
4. 運用 broadcasting 對不同形狀的陣列進行逐元素運算。
5. 在電商商品資料集上，用 1~2 行 NumPy 回答「總庫存價值」「低庫存商品數」等商業問題。

---

## 2. 時間切分表

```
00:00-00:05  開場暖身：上節回顧（Python 基礎）＋ 為什麼資料分析要學 NumPy
00:05-00:20  核心觀念 1/3：ndarray 基本概念 + shape/dtype demo
00:20-00:40  核心觀念 2/3：索引、切片、布林遮罩（重點：& | 與括號）
00:40-01:00  核心觀念 3/3：向量化運算、broadcasting、效能比較 live demo
01:00-01:10  實務 Case：電商庫存分析（3 個商業問題各 1 行解決）
01:10-01:50  課堂練習（40 min）：🟡 核心題 + 🔴 雙 11 折扣挑戰題
01:50-02:00  QA + 下節預告（S2 Pandas I/O 與清理）
```

---

## 3. 關鍵教學點 (Key Teaching Points)

1. **向量化的「感覺」比語法重要**：學員常能背出 `np.array()`，但遇到迴圈題目時仍會寫 `for`。務必在第 3 段用 `time.time()` 實測對比 100 萬筆加總，讓學員「親眼看到」快 50 倍以上。
2. **布林遮罩的括號陷阱**：`a[(a>10) & (a<20)]` 括號不可省，`and` / `or` 在 NumPy 裡會報 `ValueError`。這是本節最常見 bug，講到這裡請停下來寫錯誤版讓學員看 traceback。
3. **dtype 決定一切**：`np.array([1, 2, 3])` 是 int64，但 `/` 後會變 float64；`int8` 溢位時不會報錯而是回繞（wrap-around）。這點若不強調，後面 Pandas 章節也會踩到。
4. **Broadcasting 規則**：從右邊對齊、維度為 1 可擴展。畫一張 shape 對齊圖會比講 10 分鐘有用。
5. **NumPy 的心智模型**：把 ndarray 想成「一塊連續記憶體 + 一層 view」，切片是 view 不是 copy，修改會互相影響——這個觀念在做特徵工程時很關鍵。

---

## 4. 學員常犯錯誤 (Common Pitfalls)

- **用 Python list 寫 for-loop 處理大量數字**：`total = 0; for x in data: total += x*2`——應該改成 `(data*2).sum()`。
- **混用 `and` 與 `&`**：`a[a>0 and a<10]` 會直接爆炸；正確是 `a[(a>0) & (a<10)]`。
- **以為切片是 copy**：`b = a[:3]; b[0] = 99` 會改到 `a`，要用 `.copy()`。
- **shape 搞錯**：`(3,)` 與 `(3,1)` 在 broadcasting 結果完全不同。
- **用 `==` 比較浮點數**：應改用 `np.isclose()`。

---

## 5. 提問設計 (Discussion Prompts)

1. 如果現在手上有 1000 萬筆感測器讀數要計算移動平均，你會用 Python list 還是 NumPy？為什麼？預期效能差多少？
2. 為什麼 NumPy 要求 ndarray 裡元素型別一致（homogeneous），這個限制帶來什麼好處？
3. 布林遮罩和 SQL 的 `WHERE` 子句有什麼異同？哪一個比較彈性？

---

## 6. 延伸資源 (Further Reading)

- NumPy 官方 User Guide「Absolute Basics for Beginners」與「Broadcasting」章節（可在 numpy.org 搜尋）。
- Jake VanderPlas《Python Data Science Handbook》第 2 章 NumPy（線上免費版可搜尋章節標題）。

---

## 7. 常見 Q&A

**Q1：NumPy 跟 Pandas 有什麼差別？要全部學嗎？**
A：NumPy 處理「同質型數值陣列」，Pandas 在 NumPy 上加了「欄名 + 索引 + 異質型別」。做資料分析兩個都要會，但 Pandas 底層就是 NumPy，所以 S1 是地基。

**Q2：向量化是不是只要加個 `np.` 就好？**
A：不是。關鍵是「用陣列運算取代 Python 層的迴圈」。如果你在 `for` 裡面呼叫 `np.sum()`，還是慢。要想辦法讓整個運算一次送進 NumPy。

**Q3：`np.array` 和 `np.asarray` 差在哪？**
A：`np.array` 預設會 copy，`np.asarray` 若輸入已是 ndarray 則不 copy。效能敏感時用 `asarray`。
