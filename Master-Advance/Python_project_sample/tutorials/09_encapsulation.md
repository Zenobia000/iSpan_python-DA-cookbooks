# 封裝與資訊隱藏：控制介面與實作的分離

封裝是物件導向程式設計的核心原則之一，它的目標是將物件的內部實作細節隱藏起來，只對外暴露必要的介面。這樣做可以防止外部程式碼直接修改物件內部狀態，降低耦合度，提高程式碼的可維護性。本教學將介紹 Python 中的封裝機制及其實用技巧。

## 為什麼需要封裝？

### 問題：直接存取屬性的風險

```python
# 沒有封裝：任何人都可以隨意修改屬性
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

account = BankAccount("小明", 10000)

# 危險操作：直接修改餘額，繞過任何驗證
account.balance = -999999  # 沒有任何檢查！
account.owner = ""          # 名字被清空！
print(account.balance)      # -999999
```

### 解決：透過方法控制存取

```python
class BankAccount:
    def __init__(self, owner, balance):
        self._owner = owner
        self._balance = balance

    def deposit(self, amount):
        """存款：有驗證邏輯"""
        if amount <= 0:
            raise ValueError("存款金額必須大於 0")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        """提款：有餘額檢查"""
        if amount <= 0:
            raise ValueError("提款金額必須大於 0")
        if amount > self._balance:
            raise ValueError(f"餘額不足，目前餘額：{self._balance}")
        self._balance -= amount
        return self._balance

    def get_balance(self):
        """取得餘額（唯讀）"""
        return self._balance

account = BankAccount("小明", 10000)
account.deposit(5000)         # 透過方法操作，有驗證
print(account.get_balance())  # 15000
# account.withdraw(20000)     # ValueError: 餘額不足
```

## Python 的命名約定

Python 不像 Java 或 C++ 有嚴格的存取修飾詞（`private`、`protected`、`public`），而是透過 **命名約定** 來表達存取意圖：

### 三種命名層級

```python
class MyClass:
    def __init__(self):
        self.public = "公開"          # 公開屬性：任何人都可以存取
        self._protected = "保護"      # 保護屬性：約定不應從外部直接存取
        self.__private = "私有"       # 私有屬性：名稱修飾，外部難以存取
```

### 1. 公開屬性（無前綴）

```python
class Point:
    def __init__(self, x, y):
        self.x = x  # 公開：外部可自由讀寫
        self.y = y

p = Point(3, 4)
print(p.x)  # 3
p.x = 10    # 直接修改
```

### 2. 保護屬性（單底線 `_`）

單底線前綴是一種 **約定**，告訴其他開發者「這個屬性是內部使用的，不建議從外部直接存取」：

```python
class DataProcessor:
    def __init__(self, data):
        self.data = data           # 公開：使用者應該存取的
        self._cache = {}           # 保護：內部快取，不建議外部直接使用
        self._is_processed = False # 保護：內部狀態

    def process(self):
        if self._is_processed:
            return self._cache.get("result")
        result = self._do_heavy_computation()
        self._cache["result"] = result
        self._is_processed = True
        return result

    def _do_heavy_computation(self):
        """保護方法：內部使用的計算邏輯"""
        return sum(x ** 2 for x in self.data)
```

> **注意**：Python 不會阻止你存取 `_` 開頭的屬性，這純粹是一種約定。但好的開發者會尊重這個約定。

### 3. 私有屬性（雙底線 `__`）

雙底線前綴會觸發 **名稱修飾 (Name Mangling)**，Python 會將屬性名稱改為 `_ClassName__attribute`：

```python
class Secret:
    def __init__(self):
        self.__hidden = "祕密資料"

    def reveal(self):
        return self.__hidden  # 內部可以正常存取

s = Secret()
print(s.reveal())          # 祕密資料

# 直接存取會失敗
# print(s.__hidden)        # AttributeError

# 但 Python 不是真正的私有，仍可透過修飾後的名稱存取（不建議）
print(s._Secret__hidden)   # 祕密資料（名稱修飾的結果）
```

### 命名約定總結

| 命名方式 | 含義 | Python 行為 | 使用場景 |
| :--- | :--- | :--- | :--- |
| `name` | 公開 | 無限制 | 設計為外部使用的 API |
| `_name` | 保護（約定） | 無限制，但表達「內部使用」 | 內部實作細節 |
| `__name` | 私有（名稱修飾） | 改名為 `_Class__name` | 避免子類別意外覆寫 |
| `__name__` | 特殊方法 | Python 內建協議 | `__init__`、`__str__` 等 |

## Property 裝飾器

`@property` 讓你用屬性的語法來呼叫方法，是 Python 中實現封裝最優雅的方式：

### 基本用法

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius  # 內部以攝氏儲存

    @property
    def celsius(self):
        """取得攝氏溫度（getter）"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """設定攝氏溫度（setter），包含驗證"""
        if value < -273.15:
            raise ValueError("溫度不能低於絕對零度 (-273.15°C)")
        self._celsius = value

    @property
    def fahrenheit(self):
        """取得華氏溫度（計算屬性，唯讀）"""
        return self._celsius * 9 / 5 + 32


# 使用起來像普通屬性
temp = Temperature(25)
print(temp.celsius)      # 25（呼叫 getter）
print(temp.fahrenheit)   # 77.0（計算屬性）

temp.celsius = 30        # 呼叫 setter（有驗證）
print(temp.celsius)      # 30

# temp.celsius = -300    # ValueError: 溫度不能低於絕對零度
# temp.fahrenheit = 100  # AttributeError: 唯讀屬性
```

### 實用範例：使用者資料

```python
import re
from datetime import date


class User:
    def __init__(self, username, email, birth_date):
        self.username = username      # 使用 setter 驗證
        self.email = email            # 使用 setter 驗證
        self._birth_date = birth_date

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not value or len(value) < 3:
            raise ValueError("使用者名稱至少需要 3 個字元")
        if not value.isalnum():
            raise ValueError("使用者名稱只能包含字母和數字")
        self._username = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValueError(f"無效的 email 格式：{value}")
        self._email = value

    @property
    def age(self):
        """計算屬性：根據生日計算年齡"""
        today = date.today()
        age = today.year - self._birth_date.year
        if (today.month, today.day) < (self._birth_date.month, self._birth_date.day):
            age -= 1
        return age

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', age={self.age})"


# 使用
user = User("alice123", "alice@example.com", date(1995, 6, 15))
print(user)         # User('alice123', 'alice@example.com', age=...)
print(user.age)     # 計算屬性

user.email = "new@example.com"  # setter 驗證通過
# user.email = "invalid"         # ValueError: 無效的 email 格式
# user.username = "ab"           # ValueError: 使用者名稱至少需要 3 個字元
```

### Property 的進階技巧：刪除器

```python
class CachedData:
    def __init__(self, raw_data):
        self._raw_data = raw_data
        self._processed = None

    @property
    def processed(self):
        """惰性計算：首次存取時才處理"""
        if self._processed is None:
            print("正在處理資料...")
            self._processed = [x ** 2 for x in self._raw_data]
        return self._processed

    @processed.deleter
    def processed(self):
        """清除快取，下次存取時重新計算"""
        print("清除快取")
        self._processed = None


data = CachedData([1, 2, 3, 4, 5])
print(data.processed)  # 正在處理資料... [1, 4, 9, 16, 25]
print(data.processed)  # [1, 4, 9, 16, 25]（使用快取，不再重新計算）

del data.processed     # 清除快取
print(data.processed)  # 正在處理資料... [1, 4, 9, 16, 25]（重新計算）
```

## 設計穩定的公共介面

好的封裝意味著設計清晰的公共介面，讓使用者不需要了解內部實作：

```python
class EmailSender:
    """對外暴露簡單的介面，隱藏複雜的實作"""

    def __init__(self, smtp_host, smtp_port, username, password):
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._username = username
        self._password = password
        self._connection = None

    # === 公共介面（使用者應該使用的） ===

    def send(self, to, subject, body):
        """寄送郵件（簡單的公共方法）"""
        self._connect()
        message = self._build_message(to, subject, body)
        self._transmit(message)
        self._disconnect()
        print(f"郵件已寄送至 {to}")

    # === 內部實作（使用者不需要知道的） ===

    def _connect(self):
        """建立 SMTP 連線"""
        print(f"連接到 {self._smtp_host}:{self._smtp_port}...")
        self._connection = True  # 簡化示範

    def _build_message(self, to, subject, body):
        """組裝郵件格式"""
        return {
            "from": self._username,
            "to": to,
            "subject": subject,
            "body": body
        }

    def _transmit(self, message):
        """傳送郵件"""
        if not self._connection:
            raise RuntimeError("未建立連線")
        # 實際傳送邏輯...

    def _disconnect(self):
        """關閉連線"""
        self._connection = None


# 使用者只需要知道 send() 方法
sender = EmailSender("smtp.example.com", 587, "user@example.com", "password")
sender.send("friend@example.com", "問候", "你好！")
```

## 封裝與繼承的配合

```python
class BaseRepository:
    """基礎資料存取層"""

    def __init__(self, connection_string):
        self._connection_string = connection_string
        self._connected = False

    def save(self, entity):
        """公共方法：儲存實體"""
        self._ensure_connected()
        data = self._serialize(entity)
        self._write(data)

    def find(self, entity_id):
        """公共方法：查詢實體"""
        self._ensure_connected()
        data = self._read(entity_id)
        return self._deserialize(data)

    # 子類別應該覆寫這些方法
    def _serialize(self, entity):
        raise NotImplementedError

    def _deserialize(self, data):
        raise NotImplementedError

    def _write(self, data):
        raise NotImplementedError

    def _read(self, entity_id):
        raise NotImplementedError

    def _ensure_connected(self):
        if not self._connected:
            self._connect()

    def _connect(self):
        print(f"連接到 {self._connection_string}")
        self._connected = True


class JsonRepository(BaseRepository):
    """JSON 檔案實作"""

    def __init__(self, file_path):
        super().__init__(f"file://{file_path}")
        self._file_path = file_path

    def _serialize(self, entity):
        import json
        return json.dumps(entity, ensure_ascii=False)

    def _deserialize(self, data):
        import json
        return json.loads(data)

    def _write(self, data):
        print(f"寫入 JSON 資料到 {self._file_path}")

    def _read(self, entity_id):
        print(f"從 {self._file_path} 讀取 ID={entity_id}")
        return '{}'
```

## 常見錯誤

### 錯誤 1：過度使用 getter/setter

```python
# 不好：為每個屬性都寫 getter/setter，沒有額外邏輯
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value

    def get_y(self):
        return self._y

    def set_y(self, value):
        self._y = value

# 正確：如果沒有額外邏輯，直接用公開屬性
class Point:
    def __init__(self, x, y):
        self.x = x  # 簡單直接
        self.y = y
```

> **Python 哲學**：先用公開屬性，等到需要驗證或計算邏輯時，再用 `@property` 升級，完全不影響呼叫端的程式碼。

### 錯誤 2：混淆 `_` 和 `__` 的用途

```python
class Parent:
    def __init__(self):
        self._protected = "保護的"    # 子類別可以存取
        self.__private = "私有的"     # 名稱修飾，子類別也不易存取

class Child(Parent):
    def show(self):
        print(self._protected)   # 可以存取
        # print(self.__private)  # AttributeError！（已被修飾為 _Parent__private）
```

**何時用 `__`**：當你明確想要防止子類別意外覆寫某個屬性時才使用雙底線。大多數情況下，單底線 `_` 就足夠了。

### 錯誤 3：在 `__init__` 外定義屬性

```python
# 不好：屬性分散在各處，難以追蹤
class BadExample:
    def __init__(self):
        self.name = "test"

    def some_method(self):
        self.new_attr = "surprise"  # 只有呼叫此方法後才存在

# 正確：所有屬性在 __init__ 中初始化
class GoodExample:
    def __init__(self):
        self.name = "test"
        self.new_attr = None  # 先初始化為 None

    def some_method(self):
        self.new_attr = "now it has a value"
```

## 結論

| 概念 | 重點 |
| :--- | :--- |
| 封裝目的 | 隱藏內部實作，暴露穩定介面 |
| `_name` | 約定為保護成員，表達「內部使用」 |
| `__name` | 名稱修飾，防止子類別意外覆寫 |
| `@property` | 用屬性語法呼叫方法，優雅的存取控制 |
| getter/setter | 只在需要驗證或計算時才使用 |
| 公共介面設計 | 簡單、穩定、隱藏複雜度 |
| Python 哲學 | 先公開，需要時再用 property 升級 |

## 下一步學習

掌握封裝之後，你已經了解了物件導向的三大核心概念（封裝、繼承、多型）中的兩個。接下來我們將學習[設計模式](./10_design_patterns.md)——這些是前人總結的經典解決方案，幫助你在實際專案中更好地運用物件導向技術。
