# 常見設計模式：經典解決方案的 Python 實現

設計模式是軟體開發中反覆出現的問題的經典解決方案。它們不是可以直接複製貼上的程式碼，而是解決特定類型問題的思路和範本。本教學將介紹幾個在 Python 中最實用的設計模式，並以具體範例說明何時以及如何使用它們。

## 為什麼要學設計模式？

設計模式幫助你：

1. **用共同語言溝通**：說「這裡用觀察者模式」比解釋整套機制更有效率
2. **避免重複犯錯**：前人已經踩過的坑，不需要再踩一次
3. **提高可維護性**：遵循已知模式的程式碼，其他開發者更容易理解

## 單例模式 (Singleton)

**意圖**：確保一個類別只有一個實例，並提供全域存取點。

**適用場景**：設定管理、日誌系統、資料庫連線池。

### 基本實作

```python
class DatabaseConnection:
    """確保全域只有一個資料庫連線"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, host="localhost", port=5432):
        if self._initialized:
            return
        self.host = host
        self.port = port
        self._connected = False
        self._initialized = True
        print(f"建立資料庫連線設定：{host}:{port}")

    def connect(self):
        if not self._connected:
            print(f"連接到 {self.host}:{self.port}")
            self._connected = True

    def query(self, sql):
        if not self._connected:
            self.connect()
        print(f"執行查詢：{sql}")


# 不管建立幾次，都是同一個實例
db1 = DatabaseConnection("db.example.com", 5432)
db2 = DatabaseConnection()  # 不會重新初始化

print(db1 is db2)  # True
db1.connect()
db2.query("SELECT * FROM users")  # 使用同一個連線
```

### 更 Pythonic 的方式：使用模組

Python 的模組天然就是單例。最簡單的做法是把共享狀態放在模組中：

```python
# config.py（模組本身就是單例）
class _Config:
    def __init__(self):
        self.debug = False
        self.database_url = "sqlite:///app.db"
        self.secret_key = None

    def load_from_env(self):
        import os
        self.debug = os.environ.get("DEBUG", "false").lower() == "true"
        self.database_url = os.environ.get("DATABASE_URL", self.database_url)
        self.secret_key = os.environ.get("SECRET_KEY")

# 模組級別的單一實例
config = _Config()

# 使用時：
# from config import config
# config.load_from_env()
# print(config.debug)
```

## 工廠模式 (Factory)

**意圖**：定義一個建立物件的介面，讓子類別或配置決定要建立哪個類別的實例。

**適用場景**：根據輸入或設定動態建立不同類型的物件。

### 簡單工廠

```python
class Notification:
    """通知基類"""
    def send(self, message):
        raise NotImplementedError


class EmailNotification(Notification):
    def __init__(self, recipient):
        self.recipient = recipient

    def send(self, message):
        print(f"寄送 Email 給 {self.recipient}：{message}")


class SMSNotification(Notification):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def send(self, message):
        print(f"寄送簡訊給 {self.phone_number}：{message}")


class PushNotification(Notification):
    def __init__(self, device_id):
        self.device_id = device_id

    def send(self, message):
        print(f"推播通知到裝置 {self.device_id}：{message}")


class NotificationFactory:
    """工廠類別：根據類型建立對應的通知物件"""

    _creators = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    @classmethod
    def create(cls, notification_type, **kwargs):
        creator = cls._creators.get(notification_type)
        if creator is None:
            raise ValueError(f"未知的通知類型：{notification_type}")
        return creator(**kwargs)

    @classmethod
    def register(cls, notification_type, creator_class):
        """註冊新的通知類型（可擴展）"""
        cls._creators[notification_type] = creator_class


# 使用工廠建立物件
notifications = [
    NotificationFactory.create("email", recipient="user@example.com"),
    NotificationFactory.create("sms", phone_number="0912345678"),
    NotificationFactory.create("push", device_id="device_abc123"),
]

for notif in notifications:
    notif.send("系統維護通知")
```

### 工廠的實用場景：資料解析器

```python
import csv
import json
from pathlib import Path


class DataParser:
    """資料解析器基類"""
    def parse(self, filepath):
        raise NotImplementedError


class CSVParser(DataParser):
    def parse(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)


class JSONParser(DataParser):
    def parse(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            return json.load(f)


class TextParser(DataParser):
    def parse(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            return f.readlines()


def create_parser(filepath):
    """根據副檔名自動選擇解析器"""
    suffix = Path(filepath).suffix.lower()
    parsers = {
        ".csv": CSVParser,
        ".json": JSONParser,
        ".txt": TextParser,
    }
    parser_class = parsers.get(suffix)
    if parser_class is None:
        raise ValueError(f"不支援的檔案格式：{suffix}")
    return parser_class()


# 使用：不需要知道具體的解析器類別
# parser = create_parser("data.csv")
# data = parser.parse("data.csv")
```

## 觀察者模式 (Observer)

**意圖**：定義物件之間的一對多依賴關係，當一個物件狀態改變時，所有依賴它的物件都會收到通知。

**適用場景**：事件系統、訊息通知、資料同步。

### 基本實作

```python
class EventEmitter:
    """事件發射器：觀察者模式的核心"""

    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        """註冊事件監聽器"""
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def off(self, event, callback):
        """移除事件監聽器"""
        if event in self._listeners:
            self._listeners[event] = [
                cb for cb in self._listeners[event] if cb != callback
            ]

    def emit(self, event, *args, **kwargs):
        """觸發事件，通知所有監聽器"""
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)


# 實際應用：訂單系統
class OrderSystem(EventEmitter):
    def __init__(self):
        super().__init__()
        self.orders = []

    def place_order(self, order):
        self.orders.append(order)
        self.emit("order_placed", order)

    def cancel_order(self, order_id):
        self.orders = [o for o in self.orders if o["id"] != order_id]
        self.emit("order_cancelled", order_id)


# 不同的監聽器（觀察者）
def send_confirmation_email(order):
    print(f"[Email] 訂單確認信已寄出：#{order['id']}")

def update_inventory(order):
    print(f"[庫存] 更新庫存：{order['items']}")

def log_order(order):
    print(f"[日誌] 新訂單：#{order['id']}，金額 ${order['total']}")

def notify_cancelled(order_id):
    print(f"[通知] 訂單 #{order_id} 已取消")


# 組裝系統
system = OrderSystem()
system.on("order_placed", send_confirmation_email)
system.on("order_placed", update_inventory)
system.on("order_placed", log_order)
system.on("order_cancelled", notify_cancelled)

# 下訂單時，所有監聽器自動被通知
system.place_order({"id": 1001, "items": ["書", "筆"], "total": 625})
# [Email] 訂單確認信已寄出：#1001
# [庫存] 更新庫存：['書', '筆']
# [日誌] 新訂單：#1001，金額 $625

system.cancel_order(1001)
# [通知] 訂單 #1001 已取消
```

## 策略模式 (Strategy)

**意圖**：定義一系列演算法，將每個演算法封裝起來，讓它們可以互換。

**適用場景**：需要根據情境切換不同算法或行為的場合。

### 基本實作

```python
class PricingStrategy:
    """定價策略基類"""
    def calculate(self, base_price):
        raise NotImplementedError


class RegularPricing(PricingStrategy):
    """一般定價"""
    def calculate(self, base_price):
        return base_price


class MemberPricing(PricingStrategy):
    """會員定價：9 折"""
    def calculate(self, base_price):
        return base_price * 0.9


class VIPPricing(PricingStrategy):
    """VIP 定價：8 折"""
    def calculate(self, base_price):
        return base_price * 0.8


class HolidayPricing(PricingStrategy):
    """節日定價：75 折"""
    def calculate(self, base_price):
        return base_price * 0.75


class ShoppingCart:
    def __init__(self, pricing_strategy=None):
        self.items = []
        self.pricing = pricing_strategy or RegularPricing()

    def set_pricing(self, strategy):
        """動態切換定價策略"""
        self.pricing = strategy

    def add_item(self, name, price):
        self.items.append({"name": name, "price": price})

    def get_total(self):
        subtotal = sum(item["price"] for item in self.items)
        return self.pricing.calculate(subtotal)

    def checkout(self):
        total = self.get_total()
        strategy_name = self.pricing.__class__.__name__
        print(f"結帳（{strategy_name}）：${total:.2f}")


# 使用不同的策略
cart = ShoppingCart()
cart.add_item("Python 書", 580)
cart.add_item("滑鼠", 450)

cart.checkout()                           # 結帳（RegularPricing）：$1030.00

cart.set_pricing(MemberPricing())
cart.checkout()                           # 結帳（MemberPricing）：$927.00

cart.set_pricing(HolidayPricing())
cart.checkout()                           # 結帳（HolidayPricing）：$772.50
```

### Pythonic 方式：使用函數作為策略

Python 是多範式語言，簡單的策略不一定要用類別，函數也可以：

```python
def sort_by_name(items):
    return sorted(items, key=lambda x: x["name"])

def sort_by_price(items):
    return sorted(items, key=lambda x: x["price"])

def sort_by_price_desc(items):
    return sorted(items, key=lambda x: x["price"], reverse=True)


class ProductList:
    def __init__(self, products):
        self.products = products

    def display(self, sort_strategy=None):
        """使用函數作為策略"""
        items = sort_strategy(self.products) if sort_strategy else self.products
        for p in items:
            print(f"  {p['name']}: ${p['price']}")


products = ProductList([
    {"name": "耳機", "price": 1200},
    {"name": "鍵盤", "price": 800},
    {"name": "滑鼠", "price": 450},
])

print("依名稱排序：")
products.display(sort_by_name)

print("依價格排序（高到低）：")
products.display(sort_by_price_desc)
```

## 裝飾器模式 (Decorator)

**意圖**：動態地為物件添加額外功能，不需要修改原始類別。

**適用場景**：在不改變原有程式碼的情況下擴展功能，如日誌、權限檢查、快取。

### 使用 Python 裝飾器語法

```python
import time
import functools


def timer(func):
    """計時裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[計時] {func.__name__} 耗時 {elapsed:.4f} 秒")
        return result
    return wrapper


def retry(max_attempts=3, delay=1):
    """重試裝飾器（帶參數）"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"[重試] {func.__name__} 第 {attempt} 次失敗：{e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


def validate_positive(*param_names):
    """參數驗證裝飾器：確保指定參數為正數"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for name in param_names:
                value = bound.arguments.get(name)
                if value is not None and value <= 0:
                    raise ValueError(f"參數 '{name}' 必須為正數，收到 {value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 使用裝飾器
@timer
def slow_computation(n):
    """模擬耗時計算"""
    total = sum(i ** 2 for i in range(n))
    return total


@retry(max_attempts=3, delay=0.5)
def unreliable_api_call():
    """模擬不穩定的 API 呼叫"""
    import random
    if random.random() < 0.7:
        raise ConnectionError("連線失敗")
    return {"status": "success"}


@validate_positive("width", "height")
def calculate_area(width, height):
    return width * height


result = slow_computation(1000000)
print(f"結果：{result}")

print(calculate_area(5, 3))    # 15
# calculate_area(-1, 3)        # ValueError: 參數 'width' 必須為正數
```

## 模式選擇指南

| 場景 | 推薦模式 | 原因 |
| :--- | :--- | :--- |
| 全域唯一的資源（設定、連線） | 單例 / 模組 | 確保只有一個實例 |
| 根據條件建立不同物件 | 工廠 | 解耦建立邏輯 |
| 一個事件需要通知多個模組 | 觀察者 | 鬆耦合的事件處理 |
| 同一功能有多種實作方式 | 策略 | 動態切換算法 |
| 為現有功能增加額外行為 | 裝飾器 | 不修改原始程式碼 |

## 實作練習：綜合運用

以下範例綜合運用了多個設計模式：

```python
import functools
from datetime import datetime


# 觀察者模式：事件系統
class EventMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    def _init_events(self):
        self._listeners = {}

    def on(self, event, callback):
        if not hasattr(self, "_listeners"):
            self._init_events()
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args, **kwargs):
        if not hasattr(self, "_listeners"):
            return
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)


# 策略模式：折扣計算
def no_discount(price):
    return price

def percentage_discount(rate):
    def apply(price):
        return price * (1 - rate)
    return apply

def fixed_discount(amount):
    def apply(price):
        return max(0, price - amount)
    return apply


# 工廠模式：建立折扣策略
def create_discount(discount_type, value=0):
    strategies = {
        "none": lambda: no_discount,
        "percentage": lambda: percentage_discount(value),
        "fixed": lambda: fixed_discount(value),
    }
    creator = strategies.get(discount_type)
    if creator is None:
        raise ValueError(f"未知的折扣類型：{discount_type}")
    return creator()


# 整合：商店系統
class Store(EventMixin):
    def __init__(self, name):
        self.name = name
        self.products = {}
        self.discount = no_discount
        self._init_events()

    def add_product(self, name, price, stock):
        self.products[name] = {"price": price, "stock": stock}

    def set_discount(self, discount_type, value=0):
        self.discount = create_discount(discount_type, value)

    def purchase(self, product_name, quantity=1):
        product = self.products.get(product_name)
        if product is None:
            raise ValueError(f"找不到商品：{product_name}")
        if product["stock"] < quantity:
            raise ValueError(f"庫存不足：{product_name}")

        unit_price = self.discount(product["price"])
        total = unit_price * quantity
        product["stock"] -= quantity

        order = {
            "product": product_name,
            "quantity": quantity,
            "unit_price": unit_price,
            "total": total,
            "time": datetime.now().isoformat()
        }

        self.emit("purchase", order)
        return order


# 使用
store = Store("Python 書店")
store.add_product("Python 入門", 480, 50)
store.add_product("設計模式", 620, 30)

# 註冊觀察者
store.on("purchase", lambda o: print(f"[收據] {o['product']} x{o['quantity']} = ${o['total']:.0f}"))
store.on("purchase", lambda o: print(f"[庫存] 已更新"))

# 一般價格購買
order = store.purchase("Python 入門", 2)

# 切換為 8 折策略
store.set_discount("percentage", 0.2)
order = store.purchase("設計模式", 1)
```

## 常見錯誤

### 錯誤 1：過度設計

```python
# 不好：只有一種通知方式，卻用了工廠模式
# class NotificationFactory:
#     def create(self, type):
#         if type == "email":
#             return EmailNotification()
#         raise ValueError("不支援")

# 正確：只有一種實作時，直接使用即可
class EmailNotification:
    def send(self, message):
        print(f"Email: {message}")

# 等真的需要多種通知方式時再引入工廠
```

### 錯誤 2：錯用單例

```python
# 不好：把所有全域狀態都塞進單例
# class AppState:  # 單例
#     user = None
#     cart = []
#     settings = {}
#     logs = []
#     ...

# 正確：各司其職，只有真正需要唯一實例的才用單例
# 設定 → 單例或模組
# 使用者 → 普通類別
# 購物車 → 普通類別
```

### 錯誤 3：觀察者不清理

```python
# 注意：長期運行的系統中，記得移除不再需要的監聽器
class View:
    def __init__(self, model):
        self.model = model
        self._handler = lambda data: self.render(data)
        model.on("change", self._handler)

    def destroy(self):
        """銷毀時移除監聽器，避免記憶體洩漏"""
        self.model.off("change", self._handler)

    def render(self, data):
        print(f"渲染：{data}")
```

## 結論

| 模式 | 核心思想 | Python 偏好的實作方式 |
| :--- | :--- | :--- |
| 單例 | 全域唯一實例 | 模組變數或 `__new__` |
| 工廠 | 解耦物件建立 | 工廠函數或 `@classmethod` |
| 觀察者 | 事件驅動的鬆耦合 | 回調函數列表 |
| 策略 | 可互換的算法 | 函數或類別皆可 |
| 裝飾器 | 動態擴展功能 | `@decorator` 語法 |

**Python 的設計模式哲學**：Python 是多範式語言，許多在 Java 中需要完整類別結構的模式，在 Python 中可以用函數、模組或裝飾器更簡潔地實現。選擇最簡單、最 Pythonic 的方式即可。

## 延伸學習

恭喜你完成了整個教學系列！你已經從模組和套件的基礎，一路學到了物件導向程式設計和設計模式。建議的下一步：

1. 回顧課程大綱中的[進階主題](../oop_course/00_course_outline.md)，如特殊方法、迭代器與生成器
2. 在自己的專案中實踐這些概念
3. 閱讀優秀的開源專案程式碼，觀察設計模式的實際運用
