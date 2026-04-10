# 從函數到類別：物件導向思維的轉變

在前面的教學中，我們學習了如何使用模組、套件和路徑管理來組織 Python 程式碼。隨著專案規模擴大，單純使用函數來管理程式邏輯會變得越來越困難。本教學將帶你從函數式思維過渡到物件導向思維，理解為什麼以及何時應該使用類別。

## 函數式風格 vs 物件導向風格

### 函數式風格：以「動作」為中心

函數式風格將程式拆解為一系列獨立的函數，每個函數執行特定的操作：

```python
# 函數式風格：管理學生資料
def create_student(name, age, grades=None):
    """建立學生資料字典"""
    return {
        "name": name,
        "age": age,
        "grades": grades or []
    }

def add_grade(student, subject, score):
    """新增成績"""
    return {
        **student,
        "grades": [*student["grades"], {"subject": subject, "score": score}]
    }

def get_average(student):
    """計算平均成績"""
    if not student["grades"]:
        return 0.0
    total = sum(g["score"] for g in student["grades"])
    return total / len(student["grades"])

def display_student(student):
    """顯示學生資訊"""
    avg = get_average(student)
    print(f"學生：{student['name']}，年齡：{student['age']}，平均成績：{avg:.1f}")

# 使用方式
student = create_student("小明", 18)
student = add_grade(student, "數學", 85)
student = add_grade(student, "英文", 92)
display_student(student)
```

### 物件導向風格：以「事物」為中心

物件導向風格將資料和操作資料的方法綁定在一起，形成一個完整的「物件」：

```python
# 物件導向風格：管理學生資料
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.grades = []

    def add_grade(self, subject, score):
        """新增成績"""
        self.grades.append({"subject": subject, "score": score})

    def get_average(self):
        """計算平均成績"""
        if not self.grades:
            return 0.0
        total = sum(g["score"] for g in self.grades)
        return total / len(self.grades)

    def display(self):
        """顯示學生資訊"""
        avg = self.get_average()
        print(f"學生：{self.name}，年齡：{self.age}，平均成績：{avg:.1f}")

# 使用方式
student = Student("小明", 18)
student.add_grade("數學", 85)
student.add_grade("英文", 92)
student.display()
```

### 關鍵差異

| 面向 | 函數式風格 | 物件導向風格 |
| :--- | :--- | :--- |
| 資料與行為 | 分離（字典 + 函數） | 結合（類別封裝） |
| 狀態管理 | 每次回傳新字典 | 物件內部維護狀態 |
| 呼叫方式 | `get_average(student)` | `student.get_average()` |
| 擴展性 | 新增函數即可 | 透過繼承或新增方法 |
| 適用場景 | 簡單邏輯、資料轉換 | 複雜狀態、多種行為 |

## 為什麼需要類別？

### 問題 1：狀態散落各處

當函數需要共享多個相關的資料時，你會發現自己不斷在函數間傳遞大量參數：

```python
# 問題：參數越來越多，管理困難
def process_order(customer_name, customer_email, customer_address,
                  items, discount_rate, tax_rate, shipping_method):
    # ...處理訂單邏輯
    pass

def calculate_total(items, discount_rate, tax_rate, shipping_method):
    # ...計算總價
    pass

def send_confirmation(customer_name, customer_email, order_id, total):
    # ...寄送確認信
    pass
```

使用類別可以將相關資料組織在一起：

```python
class Order:
    def __init__(self, customer, items, discount_rate=0, tax_rate=0.05):
        self.customer = customer
        self.items = items
        self.discount_rate = discount_rate
        self.tax_rate = tax_rate
        self.order_id = None

    def calculate_total(self):
        subtotal = sum(item["price"] * item["qty"] for item in self.items)
        discount = subtotal * self.discount_rate
        tax = (subtotal - discount) * self.tax_rate
        return subtotal - discount + tax

    def process(self, shipping_method="standard"):
        self.order_id = self._generate_order_id()
        total = self.calculate_total()
        print(f"訂單 {self.order_id} 已處理，總計：${total:.2f}")
        return self.order_id

    def _generate_order_id(self):
        import random
        return f"ORD-{random.randint(10000, 99999)}"
```

### 問題 2：相似功能重複撰寫

當你有多種相似但略有不同的資料類型時，函數式風格容易產生重複代碼：

```python
# 函數式風格：為不同形狀重複撰寫類似邏輯
def calculate_circle_area(radius):
    import math
    return math.pi * radius ** 2

def calculate_rectangle_area(width, height):
    return width * height

def calculate_triangle_area(base, height):
    return 0.5 * base * height

def describe_circle(radius):
    area = calculate_circle_area(radius)
    print(f"圓形：半徑={radius}，面積={area:.2f}")

def describe_rectangle(width, height):
    area = calculate_rectangle_area(width, height)
    print(f"矩形：寬={width}，高={height}，面積={area:.2f}")

def describe_triangle(base, height):
    area = calculate_triangle_area(base, height)
    print(f"三角形：底={base}，高={height}，面積={area:.2f}")
```

物件導向可以透過共用介面來統一處理：

```python
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def describe(self):
        print(f"圓形：半徑={self.radius}，面積={self.area():.2f}")

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def describe(self):
        print(f"矩形：寬={self.width}，高={self.height}，面積={self.area():.2f}")

# 統一操作不同形狀
shapes = [Circle(5), Rectangle(3, 4)]
for shape in shapes:
    shape.describe()  # 每個物件知道如何描述自己
```

## 類別的基本語法

### 定義類別與 `__init__`

`__init__` 是初始化方法，在建立物件時自動被呼叫：

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        """初始化銀行帳戶"""
        self.owner = owner        # 實例屬性：帳戶持有人
        self.balance = balance    # 實例屬性：餘額
        self.transactions = []    # 實例屬性：交易紀錄

    def deposit(self, amount):
        """存款"""
        if amount <= 0:
            raise ValueError("存款金額必須大於 0")
        self.balance += amount
        self.transactions.append(("存款", amount))
        return self.balance

    def withdraw(self, amount):
        """提款"""
        if amount <= 0:
            raise ValueError("提款金額必須大於 0")
        if amount > self.balance:
            raise ValueError("餘額不足")
        self.balance -= amount
        self.transactions.append(("提款", amount))
        return self.balance

    def get_statement(self):
        """取得對帳單"""
        print(f"=== {self.owner} 的帳戶對帳單 ===")
        for tx_type, amount in self.transactions:
            print(f"  {tx_type}: ${amount:,.2f}")
        print(f"  目前餘額: ${self.balance:,.2f}")


# 使用類別
account = BankAccount("王小明", 1000)
account.deposit(500)
account.withdraw(200)
account.get_statement()
```

### 理解 `self`

`self` 代表物件本身，讓方法能存取同一個物件的屬性和其他方法：

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1      # 透過 self 存取屬性
        self._log("increment")  # 透過 self 呼叫其他方法

    def decrement(self):
        self.count -= 1
        self._log("decrement")

    def _log(self, action):
        print(f"[{action}] count = {self.count}")


# 每個實例有自己的狀態
counter_a = Counter()
counter_b = Counter()

counter_a.increment()  # [increment] count = 1
counter_a.increment()  # [increment] count = 2
counter_b.increment()  # [increment] count = 1

# counter_a.count = 2, counter_b.count = 1（互不影響）
```

### 實例方法、類別方法與靜態方法

```python
class DateUtils:
    date_format = "%Y-%m-%d"  # 類別屬性：所有實例共享

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # 實例方法：操作實例資料，第一個參數是 self
    def to_string(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    # 類別方法：操作類別層級的資料，第一個參數是 cls
    @classmethod
    def from_string(cls, date_string):
        """從字串建立日期物件（替代建構子）"""
        parts = date_string.split("-")
        return cls(int(parts[0]), int(parts[1]), int(parts[2]))

    @classmethod
    def set_format(cls, fmt):
        """設定所有實例共用的日期格式"""
        cls.date_format = fmt

    # 靜態方法：與類別相關但不需要存取實例或類別資料
    @staticmethod
    def is_leap_year(year):
        """判斷是否為閏年"""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# 使用範例
d1 = DateUtils(2024, 3, 15)
print(d1.to_string())           # 2024-03-15

d2 = DateUtils.from_string("2025-01-01")  # 類別方法作為替代建構子
print(d2.to_string())           # 2025-01-01

print(DateUtils.is_leap_year(2024))  # True（靜態方法）
```

## 何時使用函數，何時使用類別？

### 適合使用函數的場景

- **無狀態的資料轉換**：輸入資料、回傳結果，不需要記住任何東西
- **簡單的工具函數**：如格式化、驗證、計算
- **一次性的腳本邏輯**

```python
# 適合用函數：無狀態的資料轉換
def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

def validate_email(email):
    return "@" in email and "." in email.split("@")[1]

def format_currency(amount, currency="TWD"):
    return f"{currency} {amount:,.2f}"
```

### 適合使用類別的場景

- **需要管理狀態**：物件需要記住資料並在多次操作間保持一致
- **有多個相關操作**：一組函數都操作相同的資料
- **需要多個實例**：同一種結構要建立多個獨立的個體
- **需要擴展和組合**：透過繼承或組合來擴展功能

```python
# 適合用類別：需要管理狀態和多個相關操作
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price, quantity=1):
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def remove_item(self, name):
        self.items = [item for item in self.items if item["name"] != name]

    def get_total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    def display(self):
        print("購物車內容：")
        for item in self.items:
            subtotal = item["price"] * item["quantity"]
            print(f"  {item['name']} x{item['quantity']} = ${subtotal:.2f}")
        print(f"總計：${self.get_total():.2f}")


# 每個使用者有自己的購物車
cart_a = ShoppingCart()
cart_a.add_item("Python 教科書", 580)
cart_a.add_item("筆記本", 45, quantity=3)

cart_b = ShoppingCart()
cart_b.add_item("耳機", 1200)

cart_a.display()
cart_b.display()
```

## 實作練習：重構函數為類別

將以下函數式代碼重構為物件導向風格：

### 原始函數式代碼

```python
# 函數式：簡易記事本
def create_notebook():
    return {"notes": [], "created_at": "2024-01-01"}

def add_note(notebook, title, content):
    note = {"title": title, "content": content, "tags": []}
    return {**notebook, "notes": [*notebook["notes"], note]}

def search_notes(notebook, keyword):
    return [n for n in notebook["notes"]
            if keyword in n["title"] or keyword in n["content"]]

def count_notes(notebook):
    return len(notebook["notes"])
```

### 重構後的物件導向代碼

```python
from datetime import datetime

class Notebook:
    def __init__(self):
        self.notes = []
        self.created_at = datetime.now()

    def add_note(self, title, content):
        """新增筆記"""
        self.notes.append({
            "title": title,
            "content": content,
            "tags": [],
            "created_at": datetime.now()
        })

    def search(self, keyword):
        """搜尋包含關鍵字的筆記"""
        return [n for n in self.notes
                if keyword in n["title"] or keyword in n["content"]]

    def count(self):
        """取得筆記數量"""
        return len(self.notes)

    def display_all(self):
        """顯示所有筆記"""
        print(f"=== 記事本（共 {self.count()} 則）===")
        for i, note in enumerate(self.notes, 1):
            print(f"{i}. {note['title']}")
            print(f"   {note['content'][:50]}...")


# 使用
nb = Notebook()
nb.add_note("會議記錄", "討論 Q2 專案進度和人力分配")
nb.add_note("學習筆記", "Python 物件導向的三大特性：封裝、繼承、多型")
nb.display_all()

results = nb.search("Python")
print(f"搜尋到 {len(results)} 筆相關筆記")
```

## 常見錯誤

### 錯誤 1：忘記 `self`

```python
class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, value):
        # 錯誤：忘記用 self 存取實例屬性
        # result += value  # NameError: name 'result' is not defined

        # 正確：
        self.result += value
```

### 錯誤 2：在類別方法中修改實例屬性

```python
class Config:
    default_timeout = 30

    @classmethod
    def set_timeout(cls, value):
        # 錯誤：classmethod 中沒有 self
        # self.timeout = value  # NameError

        # 正確：修改類別屬性
        cls.default_timeout = value
```

### 錯誤 3：可變預設值陷阱

```python
class Team:
    # 錯誤：所有實例共享同一個 list
    # def __init__(self, name, members=[]):
    #     self.name = name
    #     self.members = members

    # 正確：使用 None 作為預設值
    def __init__(self, name, members=None):
        self.name = name
        self.members = members if members is not None else []
```

## 結論

| 概念 | 重點 |
| :--- | :--- |
| 函數式風格 | 以動作為中心，適合無狀態操作 |
| 物件導向風格 | 以事物為中心，適合有狀態的複雜系統 |
| `__init__` | 初始化方法，建立物件時自動執行 |
| `self` | 代表物件本身，存取屬性和方法 |
| 實例方法 | 操作實例資料，第一個參數是 `self` |
| 類別方法 | 操作類別資料，用 `@classmethod`，第一個參數是 `cls` |
| 靜態方法 | 與類別相關但不需存取實例/類別資料，用 `@staticmethod` |

## 下一步學習

現在你已經理解了從函數到類別的轉變，接下來我們將學習物件導向的核心機制之一——[繼承](./08_inheritance.md)，它讓你能夠基於現有類別建立新類別，實現程式碼的重用和擴展。
