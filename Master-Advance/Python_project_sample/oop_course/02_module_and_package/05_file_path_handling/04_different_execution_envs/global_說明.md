# Python Global 變數完整說明

---

## 📘 什麼是 Global 變數？

> **Global 變數**是指：**定義在程式最外層（模組層級）**的變數，  
> 可以在整個模組內自由存取。

- 通常宣告在 `.py` 檔案的最外層，不屬於任何函數或類別之內。
- 不需要特別聲明，Python 直譯器會自動將它放進「全域命名空間」。

---

## 🧠 什麼是全域命名空間（Global Namespace）？

> 全域命名空間就是一個字典，管理了**所有定義在模組最外層的變數、函數、類別等**。

可以用 `globals()` 函數看到它的內容。

```python
a = 100
print(globals())
```

輸出會包含 `'a': 100`。

---

## ✍️ 如何使用 Global 變數？

### 1. 在函數中讀取 Global 變數

可以直接在函數中讀取，不需要額外處理。

```python
x = 10

def show_x():
    print(x)

show_x()  # 輸出 10
```

---

### 2. 在函數中修改 Global 變數

要在函數內**修改**全域變數，必須用 `global` 關鍵字聲明，告訴 Python：

> "我要用的是外層的變數，不是創建新的區域變數"

```python
count = 0

def increment():
    global count
    count += 1

increment()
print(count)  # 輸出 1
```

如果不加 `global`，會被當成函數內部新定義的區域變數，導致錯誤。

---

## 🔥 小技巧：用 `globals()` 動態操作全域變數

### 1. 讀取全域變數

```python
x = 5
print(globals()['x'])  # 5
```

### 2. 修改全域變數

```python
globals()['x'] = 10
print(x)  # 10
```

### 3. 新增全域變數

```python
globals()['y'] = 20
print(y)  # 20
```

✅ 注意：動態修改 global namespace 是可以的，但實務上需要謹慎使用，避免難以追蹤錯誤。

---

## 📎 小結：Global 變數使用原則

| 行為 | 需要 `global` 嗎？ |
|:---|:---|
| 只讀取全域變數 | ❌ 不需要 |
| 修改全域變數 | ✅ 需要用 `global` 宣告 |
| 建立新的全域變數（動態） | ✅ 用 `globals()` |

---

## ⚠️ 注意事項

- **盡量少用全域變數修改**：容易導致大型程式碼錯誤難追蹤。
- **推薦用函數傳參數、回傳值**來取代直接操作全域變數。
- **設定檔、常數（例如 API_URL）**例外，可以用全大寫作為全域常數宣告。

---

## 🎯 實戰小範例：良好 vs 不良 Global 使用

### ❌ 不良示範

```python
score = 0

def play_game():
    global score
    score += 10

def reset_game():
    global score
    score = 0
```

（容易錯亂，debug困難）

---

### ✅ 良好示範（推薦）

```python
def play_game(score):
    return score + 10

def reset_game():
    return 0

# 主程式控制變數
score = 0
score = play_game(score)
print(score)
score = reset_game()
print(score)
```

（變數由主程式控制，函數保持純粹）

---

