# 繼承機制：程式碼重用的基礎

繼承是物件導向程式設計的核心機制之一，它允許你基於現有類別建立新類別，重用已有的程式碼並擴展新的功能。本教學將從基本的單一繼承開始，逐步介紹多重繼承、方法解析順序 (MRO) 以及 `super()` 的正確使用方式。

## 什麼是繼承？

繼承讓一個類別（子類別）自動獲得另一個類別（父類別）的所有屬性和方法，並且可以新增或覆寫功能。

```python
# 父類別（基底類別）
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        print(f"{self.name} 說：{self.sound}！")

    def describe(self):
        print(f"我是 {self.name}")


# 子類別（衍生類別）
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "汪汪")  # 呼叫父類別的 __init__

    def fetch(self, item):
        print(f"{self.name} 撿回了 {item}！")


class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "喵喵")

    def purr(self):
        print(f"{self.name} 發出呼嚕呼嚕的聲音")


# 使用
dog = Dog("小黑")
dog.speak()       # 小黑 說：汪汪！（繼承自 Animal）
dog.describe()    # 我是 小黑（繼承自 Animal）
dog.fetch("球")   # 小黑 撿回了 球！（Dog 自己的方法）

cat = Cat("咪咪")
cat.speak()       # 咪咪 說：喵喵！
cat.purr()        # 咪咪 發出呼嚕呼嚕的聲音
```

### 繼承的核心概念

```
Animal (父類別/基底類別)
├── name, sound          ← 屬性
├── speak()              ← 方法
└── describe()           ← 方法

Dog(Animal) (子類別)     Cat(Animal) (子類別)
├── 繼承 name, sound     ├── 繼承 name, sound
├── 繼承 speak()         ├── 繼承 speak()
├── 繼承 describe()      ├── 繼承 describe()
└── 新增 fetch()         └── 新增 purr()
```

## 方法覆寫 (Override)

子類別可以覆寫父類別的方法，提供自己的實作：

```python
class Shape:
    def __init__(self, color="black"):
        self.color = color

    def area(self):
        """計算面積（子類別應覆寫此方法）"""
        raise NotImplementedError("子類別必須實作 area() 方法")

    def describe(self):
        print(f"{self.color} 的 {self.__class__.__name__}，面積={self.area():.2f}")


class Circle(Shape):
    def __init__(self, radius, color="black"):
        super().__init__(color)
        self.radius = radius

    def area(self):
        """覆寫父類別的 area 方法"""
        import math
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height, color="black"):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


# 多型：不同物件用相同介面
shapes = [Circle(5, "紅色"), Rectangle(3, 4, "藍色")]
for shape in shapes:
    shape.describe()
# 紅色 的 Circle，面積=78.54
# 藍色 的 Rectangle，面積=12.00
```

## `super()` 的使用

`super()` 用來呼叫父類別的方法，最常見的用途是在子類別的 `__init__` 中呼叫父類別的初始化：

### 基本用法

```python
class Employee:
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id

    def get_info(self):
        return f"[{self.employee_id}] {self.name}"


class Manager(Employee):
    def __init__(self, name, employee_id, department):
        super().__init__(name, employee_id)  # 呼叫 Employee.__init__
        self.department = department
        self.team = []

    def add_member(self, employee):
        self.team.append(employee)

    def get_info(self):
        base_info = super().get_info()  # 呼叫 Employee.get_info
        return f"{base_info} - {self.department} 部門主管（團隊 {len(self.team)} 人）"


class Director(Manager):
    def __init__(self, name, employee_id, department, budget):
        super().__init__(name, employee_id, department)  # 呼叫 Manager.__init__
        self.budget = budget

    def get_info(self):
        base_info = super().get_info()  # 呼叫 Manager.get_info
        return f"{base_info}，預算 ${self.budget:,.0f}"


# 建立組織架構
emp1 = Employee("小王", "E001")
emp2 = Employee("小李", "E002")
mgr = Manager("張經理", "M001", "技術")
mgr.add_member(emp1)
mgr.add_member(emp2)
director = Director("陳總監", "D001", "研發", 5000000)

print(emp1.get_info())     # [E001] 小王
print(mgr.get_info())      # [M001] 張經理 - 技術 部門主管（團隊 2 人）
print(director.get_info())  # [D001] 陳總監 - 研發 部門主管（團隊 0 人），預算 $5,000,000
```

### `super()` 的常見錯誤

```python
class Parent:
    def __init__(self, value):
        self.value = value

class Child(Parent):
    def __init__(self, value, extra):
        # 錯誤 1：忘記呼叫 super().__init__
        # self.extra = extra  # self.value 不存在！

        # 錯誤 2：直接用類別名稱呼叫（可以運作但不推薦）
        # Parent.__init__(self, value)  # 多重繼承時會出問題

        # 正確：使用 super()
        super().__init__(value)
        self.extra = extra
```

## 多重繼承

Python 支援一個類別同時繼承多個父類別：

```python
class Printable:
    """提供列印功能的混入類別"""
    def print_info(self):
        attrs = vars(self)
        print(f"--- {self.__class__.__name__} ---")
        for key, value in attrs.items():
            if not key.startswith("_"):
                print(f"  {key}: {value}")


class Serializable:
    """提供序列化功能的混入類別"""
    def to_dict(self):
        return {k: v for k, v in vars(self).items() if not k.startswith("_")}

    def to_json(self):
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class Product(Printable, Serializable):
    """同時繼承 Printable 和 Serializable"""
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock


product = Product("Python 入門書", 450, 100)
product.print_info()     # 來自 Printable
print(product.to_json()) # 來自 Serializable
```

### Mixin 模式

上面的 `Printable` 和 `Serializable` 就是 **Mixin（混入）** 類別。Mixin 是一種設計慣例：

- 提供特定功能，不代表「是什麼」的關係
- 通常不定義 `__init__`
- 可以自由搭配組合

```python
class TimestampMixin:
    """自動記錄建立和更新時間"""
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def mark_created(self):
        from datetime import datetime
        self._created_at = datetime.now()

    def mark_updated(self):
        from datetime import datetime
        self._updated_at = datetime.now()

    @property
    def created_at(self):
        return getattr(self, "_created_at", None)


class ValidationMixin:
    """提供資料驗證功能"""
    def validate(self):
        errors = []
        for field, rules in getattr(self, "_validation_rules", {}).items():
            value = getattr(self, field, None)
            if "required" in rules and not value:
                errors.append(f"{field} 是必填欄位")
            if "min_length" in rules and value and len(str(value)) < rules["min_length"]:
                errors.append(f"{field} 至少需要 {rules['min_length']} 個字元")
        return errors


class User(TimestampMixin, ValidationMixin):
    _validation_rules = {
        "username": {"required": True, "min_length": 3},
        "email": {"required": True},
    }

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.mark_created()
```

## 方法解析順序 (MRO)

當多個父類別有相同的方法時，Python 使用 **C3 線性化演算法** 決定呼叫順序：

```python
class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        print("Hello from B")

class C(A):
    def greet(self):
        print("Hello from C")

class D(B, C):
    pass

# 查看 MRO
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

d = D()
d.greet()  # Hello from B（按 MRO 順序，B 排在 C 前面）
```

### MRO 的規則

```
D 的 MRO: D → B → C → A → object

搜尋方法時，按此順序找到第一個實作就停止
```

```python
# 用 super() 串聯所有父類別
class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        print("Hello from B")
        super().greet()  # 呼叫 MRO 中的下一個

class C(A):
    def greet(self):
        print("Hello from C")
        super().greet()

class D(B, C):
    def greet(self):
        print("Hello from D")
        super().greet()

d = D()
d.greet()
# Hello from D
# Hello from B
# Hello from C
# Hello from A
```

## 繼承的使用原則

### 使用繼承的好時機

- **「是一種 (is-a)」關係**：`Dog` 是一種 `Animal`
- **共用大量行為**：子類別需要父類別的大部分功能
- **框架和抽象基類**：定義統一介面

### 優先考慮組合的場景

- **「有一個 (has-a)」關係**：`Car` 有一個 `Engine`，而非 `Car` 是一種 `Engine`
- **只需要部分功能**：不需要繼承整個類別

```python
# 不好的設計：使用繼承表達「has-a」關係
class Engine:
    def start(self):
        print("引擎啟動")

# 錯誤：汽車不是引擎
# class Car(Engine):
#     pass

# 正確：使用組合
class Car:
    def __init__(self, brand):
        self.brand = brand
        self.engine = Engine()  # 組合：汽車「有」引擎

    def start(self):
        print(f"{self.brand} 汽車準備啟動")
        self.engine.start()


car = Car("Toyota")
car.start()
# Toyota 汽車準備啟動
# 引擎啟動
```

## 實用範例：日誌系統

```python
from datetime import datetime


class Logger:
    """基本日誌類別"""
    def __init__(self, name):
        self.name = name
        self.logs = []

    def log(self, level, message):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "logger": self.name,
            "message": message
        }
        self.logs.append(entry)
        self._output(entry)

    def _output(self, entry):
        """輸出日誌（子類別可覆寫）"""
        print(f"[{entry['level']}] {entry['logger']}: {entry['message']}")

    def info(self, message):
        self.log("INFO", message)

    def warning(self, message):
        self.log("WARNING", message)

    def error(self, message):
        self.log("ERROR", message)


class FileLogger(Logger):
    """輸出到檔案的日誌類別"""
    def __init__(self, name, filepath):
        super().__init__(name)
        self.filepath = filepath

    def _output(self, entry):
        """覆寫：改為寫入檔案"""
        line = f"[{entry['timestamp']}] [{entry['level']}] {entry['logger']}: {entry['message']}\n"
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(line)


class FilteredLogger(Logger):
    """可過濾等級的日誌類別"""
    LEVELS = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}

    def __init__(self, name, min_level="INFO"):
        super().__init__(name)
        self.min_level = min_level

    def log(self, level, message):
        """覆寫：加入等級過濾"""
        if self.LEVELS.get(level, 0) >= self.LEVELS.get(self.min_level, 0):
            super().log(level, message)


# 使用不同的日誌器
logger = Logger("app")
logger.info("應用程式啟動")

filtered = FilteredLogger("app", min_level="WARNING")
filtered.info("這條不會顯示")
filtered.warning("這條會顯示")
```

## 使用 `isinstance` 和 `issubclass`

```python
class Vehicle:
    pass

class Car(Vehicle):
    pass

class ElectricCar(Car):
    pass

ec = ElectricCar()

# isinstance 檢查物件是否為某個類別的實例（包含繼承鏈）
print(isinstance(ec, ElectricCar))  # True
print(isinstance(ec, Car))          # True
print(isinstance(ec, Vehicle))      # True

# issubclass 檢查類別之間的繼承關係
print(issubclass(ElectricCar, Car))      # True
print(issubclass(ElectricCar, Vehicle))  # True
print(issubclass(Car, ElectricCar))      # False
```

## 常見錯誤

### 錯誤 1：過深的繼承層次

```python
# 不好的設計：繼承層次太深，難以理解和維護
# class A: ...
# class B(A): ...
# class C(B): ...
# class D(C): ...
# class E(D): ...  # 層次太深！

# 建議：繼承層次控制在 2-3 層以內
```

### 錯誤 2：為了重用而濫用繼承

```python
# 不好：只是為了重用 save() 方法就使用繼承
# class DatabaseSaver:
#     def save(self): ...

# class User(DatabaseSaver): ...      # 使用者不是一種「資料庫儲存器」
# class Product(DatabaseSaver): ...

# 正確：使用組合或 Mixin
class DatabaseMixin:
    def save(self):
        print(f"儲存 {self.__class__.__name__} 到資料庫")

class User(DatabaseMixin):
    def __init__(self, name):
        self.name = name

class Product(DatabaseMixin):
    def __init__(self, title):
        self.title = title
```

## 結論

| 概念 | 重點 |
| :--- | :--- |
| 繼承 | 子類別自動獲得父類別的屬性和方法 |
| 方法覆寫 | 子類別可以提供自己的方法實作 |
| `super()` | 呼叫父類別的方法，建議優先使用 |
| 多重繼承 | 一個類別可以繼承多個父類別 |
| Mixin | 提供特定功能的可組合類別 |
| MRO | Python 用 C3 演算法決定方法搜尋順序 |
| is-a vs has-a | 繼承用於「是一種」，組合用於「有一個」 |

## 下一步學習

掌握繼承之後，接下來我們將學習[封裝](./09_encapsulation.md)——物件導向的另一個核心概念，它教你如何控制類別內部資料的存取，設計穩定的公共介面。
