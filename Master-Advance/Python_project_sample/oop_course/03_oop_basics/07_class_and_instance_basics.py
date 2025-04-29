# %% [markdown]
# # 類別與實例基礎
# 
# 本節將介紹 Python 中類別與實例的基本概念、語法和應用。

# %% [markdown]
# ## 1. 類別與實例的概念
# 
# 類別（Class）是一種使用者定義的資料型別，可以看作是建立物件的模板。
# 實例（Instance）是從類別建立的具體物件，每個實例都擁有類別定義的屬性和方法。

# %%
# 類別與實例的關係說明
class_instance_relation = """
類別： 藍圖或模板                實例： 使用藍圖建造的實際物件
---------------------              ----------------------------
|                   |              |                          |
|   Class: Car      |  建立實例=>  |  my_car = Car()          |
|   - color         |              |  - color = "red"         |
|   - brand         |              |  - brand = "Toyota"      |
|   - start_engine()|              |  - start_engine() 方法   |
|                   |              |                          |
---------------------              ----------------------------
"""

print(class_instance_relation)

print("現實世界的例子:")
examples = [
    "類別: 人類 (Human)     => 實例: John、Mary、David",
    "類別: 書籍 (Book)      => 實例: 《哈利波特》、《Python入門》",
    "類別: 車輛 (Vehicle)   => 實例: Toyota Camry、Ford Mustang"
]
for example in examples:
    print(f"  {example}")

# %% [markdown]
# ## 2. 定義類別的基本語法

# %%
# 最簡單的類別定義
class SimplestClass:
    pass

print("最簡單的類別定義:")
print("class SimplestClass:")
print("    pass")

# 建立類別實例
obj = SimplestClass()
print("\n建立實例:")
print("obj = SimplestClass()")
print(f"實例類型: {type(obj)}")
print(f"是 SimplestClass 的實例? {isinstance(obj, SimplestClass)}")

# %%
# 定義有屬性和方法的類別
class Dog:
    # 類別屬性 (所有實例共享)
    species = "Canis familiaris"
    
    # 初始化方法 (建構子)
    def __init__(self, name, age):
        # 實例屬性 (每個實例獨有)
        self.name = name
        self.age = age
    
    # 實例方法
    def description(self):
        return f"{self.name} is {self.age} years old"
    
    # 另一個實例方法
    def speak(self, sound):
        return f"{self.name} says {sound}"
    
    # 類別方法範例
    @classmethod
    def get_species(cls):
        return cls.species

# 創建實例
charlie = Dog("Charlie", 3)
buddy = Dog("Buddy", 5)

print("Dog 類別的實例:")
print(f"Charlie: {charlie.description()}")
print(f"Buddy: {buddy.description()}")
print(f"Charlie speaks: {charlie.speak('Woof!')}")
print(f"Buddy speaks: {buddy.speak('Bark!')}")
print(f"Dog species: {Dog.get_species()}")

# 顯示類別屬性與實例屬性的區別
print("\n類別屬性與實例屬性:")
print(f"通過類別存取類別屬性: {Dog.species}")
print(f"通過實例存取類別屬性: {charlie.species}")

# 修改實例屬性
charlie.age = 4
print(f"\n修改後 Charlie 的年齡: {charlie.age}")
print(f"Buddy 的年齡仍然是: {buddy.age}")

# 修改類別屬性
Dog.species = "Canine"
print(f"\n修改後的類別屬性: {Dog.species}")
print(f"所有實例都受影響: {charlie.species}, {buddy.species}")

# %% [markdown]
# ## 3. `__init__` 方法：初始化實例

# %%
# __init__ 方法的作用
class Person:
    def __init__(self, name, age, gender):
        print(f"初始化一個 Person 實例: {name}")
        self.name = name
        self.age = age
        self.gender = gender
        # 可以在初始化時執行計算或預處理
        self.birth_year = 2023 - age
    
    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old, {self.gender}."

# 建立實例時會自動呼叫 __init__
john = Person("John", 25, "male")
print(john.introduce())
print(f"John's birth year (calculated): {john.birth_year}")

# 參數預設值與可選參數
class Product:
    def __init__(self, name, price, category="General", in_stock=True):
        self.name = name
        self.price = price
        self.category = category
        self.in_stock = in_stock
    
    def display_info(self):
        stock_status = "Available" if self.in_stock else "Out of stock"
        return f"{self.name} (${self.price}) - {self.category} - {stock_status}"

# 使用不同方式建立實例
laptop = Product("Laptop", 999, "Electronics")
book = Product("Python Book", 29.99, "Books", False)
generic = Product("Generic Item", 10)

print("\n產品資訊:")
print(laptop.display_info())
print(book.display_info())
print(generic.display_info())

# %% [markdown]
# ## 4. 屬性存取與管理

# %%
# 展示如何存取和修改屬性
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self._transactions = []  # 以底線開頭表示內部使用 (非私有)
        self.__account_number = "A12345"  # 雙底線表示私有屬性 (名稱修飾)
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._transactions.append(f"Deposit: +${amount}")
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._transactions.append(f"Withdraw: -${amount}")
            return True
        return False
    
    def get_balance(self):
        return self.balance
    
    def get_transactions(self):
        return self._transactions
    
    def get_account_number(self):
        # 存取私有屬性的方法
        return self.__account_number

# 創建帳戶並操作
account = BankAccount("John Doe", 1000)
print(f"帳戶擁有者: {account.owner}")
print(f"初始餘額: ${account.balance}")

account.deposit(500)
account.withdraw(200)

print(f"當前餘額: ${account.get_balance()}")
print(f"交易記錄: {account.get_transactions()}")

# 嘗試存取私有屬性
try:
    print(account.__account_number)  # 這會引發錯誤
except AttributeError as e:
    print(f"錯誤: {e}")

# 正確方式存取私有屬性
print(f"帳號: {account.get_account_number()}")

# 展示 Python 的名稱修飾
print(f"實際的私有屬性名稱: _BankAccount__account_number")
print(f"直接存取修飾後的名稱: {account._BankAccount__account_number}")

# %% [markdown]
# ## 5. 實例方法、類別方法與靜態方法

# %%
class MathOperations:
    # 類別變數
    pi = 3.14159
    
    def __init__(self, value):
        # 實例變數
        self.value = value
    
    # 實例方法 (需要實例才能呼叫，第一個參數是 self)
    def square(self):
        return self.value ** 2
    
    # 類別方法 (可以不透過實例呼叫，第一個參數是 cls)
    @classmethod
    def circle_area(cls, radius):
        return cls.pi * radius ** 2
    
    # 靜態方法 (不需要 self 或 cls 參數)
    @staticmethod
    def add(a, b):
        return a + b

# 建立實例
math_ops = MathOperations(5)

# 呼叫實例方法
print(f"5 的平方: {math_ops.square()}")

# 呼叫類別方法
print(f"半徑為 3 的圓面積: {MathOperations.circle_area(3)}")
print(f"經由實例呼叫類別方法: {math_ops.circle_area(3)}")  # 也可以通過實例呼叫

# 呼叫靜態方法
print(f"2 + 3 = {MathOperations.add(2, 3)}")
print(f"經由實例呼叫靜態方法: {math_ops.add(2, 3)}")  # 也可以通過實例呼叫

# %% [markdown]
# ## 6. 三種方法的比較與使用場景

# %%
import pandas as pd
from IPython.display import display

# 方法比較表格
method_comparison = {
    "特性": [
        "定義方式",
        "第一個參數",
        "可透過類別直接呼叫",
        "可透過實例呼叫",
        "可存取實例屬性",
        "可存取/修改類別屬性",
        "可不依賴實例/類別屬性",
        "典型使用場景"
    ],
    "實例方法": [
        "正常定義 (沒有裝飾器)",
        "self (實例引用)",
        "否 (需要實例)",
        "是",
        "是 (通過 self)",
        "是 (通過 self.__class__ 或類別名稱)",
        "否 (需要與特定實例關聯)",
        "操作特定實例的狀態和行為"
    ],
    "類別方法": [
        "@classmethod 裝飾器",
        "cls (類別引用)",
        "是",
        "是 (但忽略實例)",
        "否 (除非建立/存取實例)",
        "是 (通過 cls)",
        "否 (需要與類別關聯)",
        "處理類別層級的操作，如替代建構子"
    ],
    "靜態方法": [
        "@staticmethod 裝飾器",
        "無特殊參數",
        "是",
        "是 (但忽略實例)",
        "否",
        "否 (除非明確參照類別)",
        "是 (完全獨立)",
        "與類別邏輯相關但不需存取類別/實例狀態的輔助功能"
    ]
}

comparison_df = pd.DataFrame(method_comparison)
print("實例方法、類別方法與靜態方法比較:")
display(comparison_df)

# %%
# 三種方法的實際使用範例
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    # 實例方法 - 操作特定實例
    def is_leap_year(self):
        """判斷此日期的年份是否為閏年"""
        year = self.year
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    # 類別方法 - 替代建構子
    @classmethod
    def from_string(cls, date_string):
        """從字串建立日期物件 (格式: YYYY-MM-DD)"""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @classmethod
    def today(cls):
        """建立代表今天的日期物件"""
        import datetime
        today = datetime.datetime.now()
        return cls(today.year, today.month, today.day)
    
    # 靜態方法 - 與類別相關但不需要存取類別/實例屬性
    @staticmethod
    def is_valid_date(year, month, day):
        """檢查日期是否有效"""
        if not (1 <= month <= 12):
            return False
        
        # 檢查日期範圍
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # 閏年二月有 29 天
        if month == 2 and (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            days_in_month[2] = 29
            
        return 1 <= day <= days_in_month[month]
    
    def __str__(self):
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

# 使用實例方法
date1 = Date(2020, 1, 1)
print(f"{date1} 是閏年? {date1.is_leap_year()}")

# 使用類別方法作為替代建構子
date2 = Date.from_string("2021-05-15")
print(f"從字串建立: {date2}")

date3 = Date.today()
print(f"今天: {date3}")

# 使用靜態方法
print(f"2022-02-29 是有效日期? {Date.is_valid_date(2022, 2, 29)}")
print(f"2020-02-29 是有效日期? {Date.is_valid_date(2020, 2, 29)}")

# %% [markdown]
# ## 7. 類別變數與實例變數

# %%
class Counter:
    # 類別變數 - 所有實例共享
    count = 0
    
    def __init__(self, name):
        # 實例變數 - 每個實例獨有
        self.name = name
        # 修改類別變數
        Counter.count += 1
        # 實例變數與類別變數同名
        self.count = 0  # 這會隱藏類別變數
    
    def increment(self):
        # 修改實例變數
        self.count += 1
    
    def reset(self):
        # 重設實例變數
        self.count = 0
    
    @classmethod
    def get_total_count(cls):
        # 獲取類別變數
        return cls.count
    
    def __str__(self):
        return f"Counter({self.name}): {self.count}"

# 建立計數器
counter1 = Counter("First")
counter2 = Counter("Second")
counter3 = Counter("Third")

print(f"已建立的計數器總數: {Counter.get_total_count()}")

# 增加各計數器的計數
counter1.increment()
counter1.increment()
counter2.increment()

print(counter1)
print(counter2)
print(counter3)

# 展示實例變數與類別變數的區別
print(f"\n計數器 1 的計數 (實例變數): {counter1.count}")
print(f"計數器類別的計數 (類別變數): {Counter.count}")

# 修改類別變數
Counter.count = 10
print(f"修改後的類別變數: {Counter.count}")
print(f"新建立的計數器會使用修改後的類別變數")
counter4 = Counter("Fourth")
print(f"現在的類別變數: {Counter.count}")

# %% [markdown]
# ## 8. 實例之間的關係與協作

# %%
# 實例之間的關係範例
class Author:
    def __init__(self, name):
        self.name = name
        self.books = []  # 關聯到 Book 物件的列表
    
    def write_book(self, title, year):
        # 建立新書並建立雙向關係
        book = Book(title, year, self)
        self.books.append(book)
        return book
    
    def get_books(self):
        return self.books
    
    def __str__(self):
        return f"Author: {self.name}"

class Book:
    def __init__(self, title, year, author):
        self.title = title
        self.year = year
        self.author = author  # 關聯到 Author 物件
    
    def get_author(self):
        return self.author
    
    def __str__(self):
        return f"'{self.title}' ({self.year}) by {self.author.name}"

# 建立關係
rowling = Author("J.K. Rowling")
hp1 = rowling.write_book("Harry Potter and the Philosopher's Stone", 1997)
hp2 = rowling.write_book("Harry Potter and the Chamber of Secrets", 1998)

# 查詢關係
print(f"作者: {rowling}")
print(f"書籍: {hp1}")
print(f"書籍: {hp2}")

print("\n作者的所有著作:")
for book in rowling.get_books():
    print(f"  {book}")

print(f"\n書籍 {hp1.title} 的作者是 {hp1.get_author().name}")

# 更複雜的關係示例
class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []  # 一對多關係
    
    def add_employee(self, employee):
        if employee not in self.employees:
            self.employees.append(employee)
            employee.department = self  # 更新員工的部門
    
    def get_employee_count(self):
        return len(self.employees)
    
    def __str__(self):
        return f"Department: {self.name} ({self.get_employee_count()} 位員工)"

class Employee:
    def __init__(self, name, role, department=None):
        self.name = name
        self.role = role
        self.department = None  # 預設無部門
        if department:
            department.add_employee(self)  # 關聯部門
    
    def assign_to(self, department):
        # 變更部門
        if self.department:
            self.department.employees.remove(self)
        department.add_employee(self)
    
    def __str__(self):
        dept_info = f", {self.department.name}" if self.department else ""
        return f"{self.name} ({self.role}{dept_info})"

# 建立部門與員工
it_dept = Department("IT")
hr_dept = Department("HR")

alice = Employee("Alice", "Developer", it_dept)
bob = Employee("Bob", "Manager", it_dept)
charlie = Employee("Charlie", "HR Specialist", hr_dept)

# 顯示關係
print("\n部門與員工:")
print(it_dept)
print(hr_dept)

print("\nIT 部門員工:")
for emp in it_dept.employees:
    print(f"  {emp}")

print("\nHR 部門員工:")
for emp in hr_dept.employees:
    print(f"  {emp}")

# 變更關係
print("\n變更 Bob 的部門:")
bob.assign_to(hr_dept)

print(it_dept)
print(hr_dept)

# %% [markdown]
# ## 9. 實作練習
# 
# 1. 設計一個 `Student` 類別，包含姓名、學號、課程列表等屬性，以及選課、退課等方法。
# 
# 2. 設計一個 `Course` 類別，包含課程代碼、名稱、學分等屬性，以及加入學生、移除學生等方法。
# 
# 3. 建立學生和課程之間的關聯關係，使它們能夠互相引用。
# 
# 4. 建立一個 `School` 類別來管理多個學生和課程，包含註冊學生、開設課程、產生班級報表等功能。 