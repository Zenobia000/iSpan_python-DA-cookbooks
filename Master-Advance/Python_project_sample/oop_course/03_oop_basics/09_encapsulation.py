# %% [markdown]
# # 封裝與資訊隱藏
# 
# 本節探討物件導向程式設計中的封裝概念，以及在 Python 中實現不同程度的資訊隱藏。

# %% [markdown]
# ## 1. 什麼是封裝？
# 
# 封裝是物件導向的核心原則之一，它將資料（屬性）和操作該資料的方法組合在一起，同時限制外部直接存取內部資料。

# %%
# 封裝的基本概念
print("封裝的主要目標:")
encapsulation_goals = [
    "將數據和方法綁定到單一單元（類別）中",
    "隱藏內部實現細節",
    "保護數據不被外部直接訪問",
    "只暴露必要的接口給外部",
    "減少系統各部分之間的耦合"
]

for i, goal in enumerate(encapsulation_goals, 1):
    print(f"{i}. {goal}")

# %% [markdown]
# ## 2. Python 中的封裝機制

# %%
# Python 中實現封裝的語法和約定
print("Python 中的封裝機制:")
encapsulation_methods = [
    ("公開屬性", "普通命名", "name", "完全可存取，無限制"),
    ("約定私有", "單底線前綴", "_name", "暗示不應從外部直接存取"),
    ("名稱修飾私有", "雙底線前綴", "__name", "實際會被修飾為 _ClassName__name"),
    ("特殊方法", "雙底線前後綴", "__name__", "Python 內置特殊方法，不是用於封裝")
]

import pandas as pd
from IPython.display import display

df = pd.DataFrame(encapsulation_methods, 
                  columns=["類型", "命名約定", "範例", "說明"])
display(df)

# %% [markdown]
# ## 3. 公開、保護和私有成員

# %%
class BankAccount:
    def __init__(self, owner, balance=0):
        # 公開屬性 - 任何地方都可以存取
        self.owner = owner
        
        # 保護屬性 (約定) - 表示不應該從外部存取
        self._balance = balance 
        
        # 私有屬性 - 透過名稱修飾防止直接存取
        self.__account_number = "A12345"
        
        # 類私有屬性
        self.__transaction_log = []
    
    # 公開方法
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self._balance += amount
            self.__log_transaction("deposit", amount)
            return True
        return False
    
    def withdraw(self, amount):
        """提款"""
        if 0 < amount <= self._balance:
            self._balance -= amount
            self.__log_transaction("withdraw", amount)
            return True
        return False
    
    def get_balance(self):
        """查詢餘額"""
        return self._balance
    
    def get_account_info(self):
        """獲取帳戶資訊"""
        return {
            "owner": self.owner,
            "balance": self._balance,
            "account_number": self.__account_number
        }
    
    # 保護方法 (約定)
    def _apply_interest(self, rate):
        """應用利息 (內部或子類使用)"""
        interest = self._balance * rate
        self._balance += interest
        self.__log_transaction("interest", interest)
    
    # 私有方法
    def __log_transaction(self, transaction_type, amount):
        """記錄交易 (僅內部使用)"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__transaction_log.append({
            "type": transaction_type,
            "amount": amount,
            "timestamp": timestamp,
            "balance": self._balance
        })
    
    def get_transaction_history(self):
        """獲取交易歷史"""
        return self.__transaction_log.copy()

# 創建銀行帳戶
account = BankAccount("John Doe", 1000)

# 使用公開方法和屬性
print(f"帳戶擁有者: {account.owner}")
account.deposit(500)
account.withdraw(200)
print(f"當前餘額: ${account.get_balance()}")
print(f"帳戶資訊: {account.get_account_info()}")

# 存取保護屬性 (技術上可行，但違反約定)
print(f"\n直接存取保護屬性 (不推薦): ${account._balance}")

# 嘗試存取私有屬性
try:
    print(account.__account_number)  # 這會引發錯誤
except AttributeError as e:
    print(f"\n無法直接存取私有屬性: {e}")

# 但仍可通過名稱修飾來存取
print(f"通過名稱修飾存取私有屬性 (不推薦): {account._BankAccount__account_number}")

# 使用保護方法
account._apply_interest(0.05)  # 技術上可行，但違反約定
print(f"\n應用利息後餘額: ${account.get_balance()}")

# 查看交易歷史
print("\n交易歷史:")
for transaction in account.get_transaction_history():
    print(f"  {transaction['timestamp']} - {transaction['type']}: ${transaction['amount']}")

# %% [markdown]
# ## 4. 使用屬性裝飾器控制存取

# %%
class Person:
    def __init__(self, name, age=0):
        self._name = name  # 保護屬性
        self._age = age    # 保護屬性
    
    # name 屬性 - 只讀
    @property
    def name(self):
        return self._name
    
    # age 屬性 - 讀寫，帶驗證
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("年齡必須是整數")
        if value < 0:
            raise ValueError("年齡不能為負數")
        self._age = value
    
    # 計算屬性 - 基於其他屬性
    @property
    def is_adult(self):
        return self._age >= 18

# 創建 Person 實例
person = Person("Alice", 25)

# 使用 property 存取屬性
print(f"姓名: {person.name}")
print(f"年齡: {person.age}")
print(f"成年人? {person.is_adult}")

# 修改年齡
person.age = 16
print(f"\n修改後 - 年齡: {person.age}")
print(f"修改後 - 成年人? {person.is_adult}")

# 嘗試修改只讀屬性
try:
    person.name = "Bob"  # 會引發錯誤
except AttributeError as e:
    print(f"\n嘗試修改只讀屬性: {e}")

# 嘗試設置無效年齡
try:
    person.age = -5  # 會引發錯誤
except ValueError as e:
    print(f"嘗試設置無效年齡: {e}")

# %% [markdown]
# ## 5. 使用描述器進行更複雜的封裝

# %%
# 描述器定義
class ValidatedField:
    def __init__(self, name, type_=None, min_value=None, max_value=None):
        self.name = name
        self.private_name = f"_{name}"
        self.type = type_
        self.min_value = min_value
        self.max_value = max_value
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)
    
    def __set__(self, instance, value):
        # 類型檢查
        if self.type is not None and not isinstance(value, self.type):
            raise TypeError(f"{self.name} 必須是 {self.type.__name__} 類型")
        
        # 範圍檢查
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} 不能小於 {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} 不能大於 {self.max_value}")
        
        # 設置值
        setattr(instance, self.private_name, value)
    
    def __delete__(self, instance):
        raise AttributeError(f"{self.name} 屬性不能被刪除")

# 使用描述器的類別
class Student:
    name = ValidatedField("name", str)
    age = ValidatedField("age", int, 0, 120)
    grade = ValidatedField("grade", int, 0, 100)
    
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    
    def __str__(self):
        return f"Student(name={self.name}, age={self.age}, grade={self.grade})"

# 使用 Student 類別
student = Student("David", 18, 92)
print(student)

# 合法更新
student.age = 19
student.grade = 95
print(f"\n更新後: {student}")

# 非法更新
try:
    student.age = -5  # 年齡不能為負數
except ValueError as e:
    print(f"\n年齡驗證錯誤: {e}")

try:
    student.grade = 101  # 成績不能超過100
except ValueError as e:
    print(f"成績驗證錯誤: {e}")

try:
    student.name = 123  # 名字必須是字符串
except TypeError as e:
    print(f"名字類型錯誤: {e}")

try:
    del student.name  # 屬性不能被刪除
except AttributeError as e:
    print(f"刪除屬性錯誤: {e}")

# %% [markdown]
# ## 6. 使用 `__slots__` 限制屬性

# %%
class CompactPerson:
    # 明確定義允許的屬性列表
    __slots__ = ['name', 'age', 'email']
    
    def __init__(self, name, age, email=None):
        self.name = name
        self.age = age
        self.email = email
    
    def __str__(self):
        return f"CompactPerson(name={self.name}, age={self.age}, email={self.email})"

# 創建實例
compact_person = CompactPerson("Charlie", 30, "charlie@example.com")
print(compact_person)

# 修改現有屬性
compact_person.age = 31
print(f"\n更新年齡後: {compact_person}")

# 嘗試添加未在 __slots__ 中定義的屬性
try:
    compact_person.phone = "123-456-7890"  # 這會引發錯誤
except AttributeError as e:
    print(f"\n錯誤: {e}")

# 比較記憶體使用
import sys

class RegularPerson:
    def __init__(self, name, age, email=None):
        self.name = name
        self.age = age
        self.email = email

# 創建兩種不同的對象
regular = RegularPerson("Test", 20, "test@example.com")
compact = CompactPerson("Test", 20, "test@example.com")

# 添加相同的屬性到常規對象
regular.name = "Test"
regular.age = 20
regular.email = "test@example.com"

# 添加額外屬性到常規對象
regular.extra1 = 1
regular.extra2 = 2
regular.extra3 = 3

# 比較大小
print(f"\n記憶體使用比較:")
print(f"Regular Person: {sys.getsizeof(regular)} bytes")
print(f"Compact Person: {sys.getsizeof(compact)} bytes")

# __slots__ 的優缺點
print("\n__slots__ 的優點:")
print("1. 減少記憶體使用")
print("2. 稍微加快屬性存取速度")
print("3. 防止意外添加新屬性")

print("\n__slots__ 的缺點:")
print("1. 不能動態添加未定義的屬性")
print("2. 使用元繼承時可能產生問題")
print("3. 無法使用弱引用")

# %% [markdown]
# ## 7. 使用上下文管理器控制資源存取

# %%
class ManagedResource:
    def __init__(self, name):
        self.name = name
        self._resource = None
        self._is_open = False
    
    def __enter__(self):
        """進入上下文時調用"""
        print(f"Opening resource: {self.name}")
        self._is_open = True
        self._resource = {"name": self.name, "data": "resource data"}
        return self._resource  # 返回資源供上下文內使用
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文時調用"""
        print(f"Closing resource: {self.name}")
        self._is_open = False
        self._resource = None
        # 如果返回 True，則會抑制異常
        return False
    
    def is_open(self):
        """檢查資源是否開啟"""
        return self._is_open
    
    def get_resource(self):
        """獲取資源 (僅在開啟狀態可用)"""
        if not self._is_open:
            raise ValueError("Resource is not open")
        return self._resource

# 使用上下文管理器
print("上下文管理器範例:")
resource = ManagedResource("database")

# 檢查初始狀態
print(f"初始狀態 - 資源開啟? {resource.is_open()}")

# 使用 with 語句自動管理資源
with resource as res:
    print(f"在上下文中 - 資源開啟? {resource.is_open()}")
    print(f"資源數據: {res}")
    
    # 也可以使用 get_resource 方法
    print(f"通過方法取得的資源: {resource.get_resource()}")

# 檢查退出上下文後的狀態
print(f"上下文後 - 資源開啟? {resource.is_open()}")

# 嘗試在上下文外存取資源
try:
    resource.get_resource()
except ValueError as e:
    print(f"錯誤: {e}")

# 異常處理範例
try:
    with resource as res:
        print("在上下文中進行操作...")
        raise RuntimeError("發生錯誤")
except RuntimeError as e:
    print(f"捕獲到異常: {e}")

# 確認資源已正確關閉
print(f"異常後 - 資源開啟? {resource.is_open()}")

# %% [markdown]
# ## 8. 封裝的設計模式

# %%
# 展示常見的封裝設計模式

# 1. 外觀模式 (Facade) - 簡化複雜子系統
class ComputerFacade:
    def __init__(self):
        self._cpu = CPU()
        self._memory = Memory()
        self._hardDrive = HardDrive()
    
    def start(self):
        print("啟動電腦...")
        self._cpu.freeze()
        self._memory.load(self._hardDrive.read("boot_sector", 0, 512))
        self._cpu.jump(0)
        self._cpu.execute()
        print("電腦已啟動完成")

class CPU:
    def freeze(self):
        print("CPU: 凍結當前執行程序")
    
    def jump(self, position):
        print(f"CPU: 跳轉到位置 {position}")
    
    def execute(self):
        print("CPU: 執行指令")

class Memory:
    def load(self, data):
        print(f"Memory: 加載數據 - {data[:20]}...")

class HardDrive:
    def read(self, sector, position, size):
        print(f"HardDrive: 從 {sector} 讀取數據，位置={position}，大小={size}")
        return "0101010101010101010101010101010101010101..."

# 使用外觀模式
print("外觀模式範例:")
computer = ComputerFacade()
computer.start()  # 用戶只需要知道如何啟動電腦，不需要了解內部細節

# 2. 代理模式 (Proxy) - 控制對另一個對象的存取
print("\n代理模式範例:")

class Subject:
    """定義 RealSubject 和 Proxy 共同的接口"""
    def request(self):
        pass

class RealSubject(Subject):
    """定義 Proxy 所代表的真實對象"""
    def request(self):
        print("RealSubject: 處理請求")

class Proxy(Subject):
    """控制對 RealSubject 對象的存取"""
    def __init__(self):
        self._real_subject = None
    
    def request(self):
        """在轉發請求前可以執行額外的控制邏輯"""
        if self._check_access():
            if self._real_subject is None:
                self._real_subject = RealSubject()
            
            self._before_request()
            self._real_subject.request()
            self._after_request()
    
    def _check_access(self):
        print("Proxy: 檢查存取權限")
        return True
    
    def _before_request(self):
        print("Proxy: 預處理請求")
    
    def _after_request(self):
        print("Proxy: 後處理請求")

# 使用代理模式
client_code = lambda subject: subject.request()
proxy = Proxy()
client_code(proxy)

# %% [markdown]
# ## 9. 封裝不是安全措施

# %%
print("Python 中的封裝限制:")
encapsulation_notes = [
    "Python 沒有真正的私有屬性或方法",
    "雙底線前綴 (__name) 只是通過名稱修飾提供有限的保護",
    "任何屬性都可以通過反射或名稱修飾來存取",
    "封裝在 Python 中主要是一種約定，而非強制機制",
    "良好的 API 設計比命名約定更重要"
]

for i, note in enumerate(encapsulation_notes, 1):
    print(f"{i}. {note}")

# 演示存取「私有」成員
class PrivateDemo:
    def __init__(self):
        self.__private_attr = "這是私有的"
    
    def __private_method(self):
        return "這是私有方法"
    
    def public_method(self):
        return self.__private_method()

# 創建實例
demo = PrivateDemo()

# 使用公開方法間接存取私有方法
print(f"\n通過公開方法存取: {demo.public_method()}")

# 直接存取「私有」屬性和方法
print("\n「繞過」封裝存取私有成員:")
print(f"私有屬性: {demo._PrivateDemo__private_attr}")
print(f"私有方法: {demo._PrivateDemo__private_method()}")

# 使用反射動態存取
import inspect

print("\n使用反射檢視類:")
for name, member in inspect.getmembers(demo):
    if not name.startswith('__'):
        print(f"{name}: {member}")

# %% [markdown]
# ## 10. 實作練習
# 
# 1. 設計一個 `CreditCard` 類別，使用封裝來確保:
#    - 卡號和持卡人姓名只能在創建時設置，之後不可修改
#    - 信用額度可以增加但不能減少
#    - 消費記錄為私有屬性，只能通過特定方法查看
#    - 實現 `charge(amount)` 和 `payment(amount)` 方法，處理消費和還款
# 
# 2. 設計一個 `FileManager` 類別作為上下文管理器，確保檔案在操作完畢後自動關閉，並在開啟檔案失敗時提供適當的錯誤處理。
# 
# 3. 使用描述器實現一個 `Range` 類別，可以用來驗證數值類型的屬性在指定範圍內，並套用到一個 `Thermostat` 類別上。 