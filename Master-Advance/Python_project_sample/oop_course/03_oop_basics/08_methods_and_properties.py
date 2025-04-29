# %% [markdown]
# # 方法與屬性
# 
# 本節將深入探討 Python 類別中的方法和屬性，以及它們在物件導向設計中的作用和應用方式。

# %% [markdown]
# ## 1. 方法的類型與特性

# %%
# 方法的不同類型回顧
class Demo:
    class_var = "類別變數"
    
    def __init__(self, value):
        self.instance_var = value
    
    # 實例方法 - 運作於實例上
    def instance_method(self):
        return f"實例方法，可存取實例變數: {self.instance_var}"
    
    # 類別方法 - 運作於類別上
    @classmethod
    def class_method(cls):
        return f"類別方法，可存取類別變數: {cls.class_var}"
    
    # 靜態方法 - 不需存取類別或實例
    @staticmethod
    def static_method(x, y):
        return f"靜態方法，參數: {x}, {y}"

# 建立實例
demo = Demo("實例值")

# 呼叫不同類型的方法
print(demo.instance_method())  # 透過實例呼叫實例方法
print(Demo.class_method())     # 透過類別呼叫類別方法
print(demo.class_method())     # 也可透過實例呼叫類別方法
print(Demo.static_method(1, 2))# 透過類別呼叫靜態方法
print(demo.static_method(3, 4))# 也可透過實例呼叫靜態方法

# 嘗試通過類別直接呼叫實例方法
try:
    Demo.instance_method()
except TypeError as e:
    print(f"錯誤: {e}")

# %% [markdown]
# ## 2. `@property` 裝飾器 - 讓方法像屬性一樣使用

# %%
# 未使用 property 的類別
class Circle1:
    def __init__(self, radius):
        self.radius = radius
    
    # 計算面積的方法
    def calculate_area(self):
        import math
        return math.pi * self.radius ** 2
    
    # 計算周長的方法
    def calculate_perimeter(self):
        import math
        return 2 * math.pi * self.radius

# 使用 property 的類別
class Circle2:
    def __init__(self, radius):
        self.radius = radius
    
    # 計算面積的 property
    @property
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    # 計算周長的 property
    @property
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

# 比較兩種使用方式
circle1 = Circle1(5)
circle2 = Circle2(5)

print("未使用 property:")
print(f"面積: {circle1.calculate_area()}")
print(f"周長: {circle1.calculate_perimeter()}")

print("\n使用 property:")
print(f"面積: {circle2.area}")  # 注意: 無需括號
print(f"周長: {circle2.perimeter}")  # 注意: 無需括號

# 主要差異
print("\nproperty 的優點:")
print("1. 使用方式像屬性，更直覺")
print("2. 可隱藏計算細節，改變實現不影響接口")
print("3. 可控制讀取和修改的邏輯")

# %% [markdown]
# ## 3. 使用 getter 和 setter 進行數據驗證

# %%
class Temperature:
    def __init__(self, celsius=0):
        # 使用私有屬性儲存溫度
        self._celsius = celsius
    
    # Getter - 讀取 celsius 屬性
    @property
    def celsius(self):
        return self._celsius
    
    # Setter - 設定 celsius 屬性，含驗證邏輯
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:  # 絕對零度檢查
            raise ValueError("溫度不能低於絕對零度 (-273.15°C)")
        self._celsius = value
    
    # 華氏溫度屬性 (依賴於攝氏溫度)
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    # 華氏溫度的 setter
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9  # 通過 celsius setter 進行驗證

# 使用 Temperature 類別
temp = Temperature(25)  # 攝氏 25 度
print(f"攝氏: {temp.celsius}°C")
print(f"華氏: {temp.fahrenheit}°F")

# 改變溫度值
temp.celsius = 30
print(f"\n更新後 - 攝氏: {temp.celsius}°C")
print(f"更新後 - 華氏: {temp.fahrenheit}°F")

temp.fahrenheit = 68
print(f"\n更新後 - 華氏: {temp.fahrenheit}°F")
print(f"更新後 - 攝氏: {temp.celsius}°C")

# 驗證邏輯測試
try:
    temp.celsius = -300  # 低於絕對零度
except ValueError as e:
    print(f"\n捕捉到錯誤: {e}")

# %% [markdown]
# ## 4. 只讀屬性和計算屬性

# %%
import math

class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._area = None  # 緩存面積
    
    # 寬度屬性 (讀寫)
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("寬度必須為正數")
        self._width = value
        self._area = None  # 更新寬度時重置面積緩存
    
    # 高度屬性 (讀寫)
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("高度必須為正數")
        self._height = value
        self._area = None  # 更新高度時重置面積緩存
    
    # 面積屬性 (只讀，帶緩存)
    @property
    def area(self):
        if self._area is None:  # 如果緩存無效
            print("計算面積...")  # 顯示計算過程
            self._area = self._width * self._height
        return self._area
    
    # 對角線屬性 (只讀，即時計算)
    @property
    def diagonal(self):
        return math.sqrt(self._width**2 + self._height**2)
    
    # 周長屬性 (只讀)
    @property
    def perimeter(self):
        return 2 * (self._width + self._height)

# 使用 Rectangle 類別
rect = Rectangle(3, 4)
print(f"矩形: {rect.width} x {rect.height}")
print(f"面積: {rect.area}")  # 首次計算
print(f"面積: {rect.area}")  # 使用緩存
print(f"對角線: {rect.diagonal:.2f}")
print(f"周長: {rect.perimeter}")

# 改變尺寸
rect.width = 5
print(f"\n更新尺寸後: {rect.width} x {rect.height}")
print(f"面積: {rect.area}")  # 重新計算
print(f"對角線: {rect.diagonal:.2f}")
print(f"周長: {rect.perimeter}")

# 嘗試設置只讀屬性
try:
    rect.area = 20  # 嘗試修改只讀屬性
except AttributeError as e:
    print(f"\n捕捉到錯誤: {e}")

# %% [markdown]
# ## 5. 類別層級的屬性控制: 描述器 (Descriptors)

# %%
# 自定義描述器
class Positive:
    def __init__(self, name):
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name)
    
    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError(f"{self.name} 必須為正數")
        setattr(instance, self.private_name, value)
    
    def __delete__(self, instance):
        raise AttributeError(f"{self.name} 不能被刪除")

# 使用描述器的類別
class Product:
    price = Positive("price")  # 使用描述器
    quantity = Positive("quantity")  # 使用描述器
    
    def __init__(self, name, price, quantity):
        self.name = name
        self._price = 0  # 初始化私有屬性
        self._quantity = 0  # 初始化私有屬性
        # 通過描述器設置值
        self.price = price
        self.quantity = quantity
    
    @property
    def total(self):
        return self.price * self.quantity

# 使用 Product 類別
laptop = Product("Laptop", 1200, 5)
print(f"產品: {laptop.name}")
print(f"價格: ${laptop.price}")
print(f"數量: {laptop.quantity}")
print(f"總價: ${laptop.total}")

# 更新價格
laptop.price = 1000
print(f"\n更新後價格: ${laptop.price}")
print(f"總價: ${laptop.total}")

# 驗證檢查
try:
    laptop.quantity = -2  # 數量不能為負
except ValueError as e:
    print(f"\n捕捉到錯誤: {e}")

try:
    del laptop.price  # 不能刪除
except AttributeError as e:
    print(f"捕捉到錯誤: {e}")

# %% [markdown]
# ## 6. 使用 `@property` 實現狀態轉換和依賴屬性

# %%
# 具有狀態和依賴屬性的類別
class Person:
    def __init__(self, first_name, last_name, age):
        self._first_name = first_name
        self._last_name = last_name
        self._age = age
        self._full_name = None  # 緩存全名
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        self._first_name = value
        self._full_name = None  # 重置全名緩存
    
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        self._last_name = value
        self._full_name = None  # 重置全名緩存
    
    @property
    def full_name(self):
        if self._full_name is None:
            self._full_name = f"{self._first_name} {self._last_name}"
        return self._full_name
    
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
    
    @property
    def is_adult(self):
        return self._age >= 18
    
    @property
    def age_category(self):
        if self._age < 13:
            return "兒童"
        elif self._age < 18:
            return "青少年"
        elif self._age < 65:
            return "成人"
        else:
            return "老年人"

# 使用 Person 類別
person = Person("John", "Doe", 25)
print(f"姓名: {person.full_name}")
print(f"年齡: {person.age}，類別: {person.age_category}")
print(f"是成年人嗎? {person.is_adult}")

# 更新資料
person.first_name = "Jane"
print(f"\n更新後姓名: {person.full_name}")

person.age = 15
print(f"更新後年齡: {person.age}，類別: {person.age_category}")
print(f"是成年人嗎? {person.is_adult}")

# %% [markdown]
# ## 7. 方法的鏈式調用 (Method Chaining)

# %%
# 設計支援鏈式調用的類別
class Calculator:
    def __init__(self, value=0):
        self.value = value
    
    def add(self, x):
        self.value += x
        return self  # 返回自身以支援鏈式調用
    
    def subtract(self, x):
        self.value -= x
        return self
    
    def multiply(self, x):
        self.value *= x
        return self
    
    def divide(self, x):
        if x == 0:
            raise ValueError("除數不能為零")
        self.value /= x
        return self
    
    def power(self, x):
        self.value **= x
        return self
    
    def get_result(self):
        return self.value
    
    def __str__(self):
        return f"計算結果: {self.value}"

# 使用鏈式調用
calc = Calculator(10)
result = calc.add(5).multiply(2).subtract(7).divide(3).get_result()
print(f"計算結果: {result}")

# 更複雜的例子
result = (
    Calculator(2)
    .power(3)        # 2^3 = 8
    .add(10)         # 8 + 10 = 18
    .multiply(2)     # 18 * 2 = 36
    .divide(4)       # 36 / 4 = 9
    .subtract(4.5)   # 9 - 4.5 = 4.5
    .get_result()
)
print(f"\n複雜計算結果: {result}")

# %% [markdown]
# ## 8. 使用 `__call__` 方法讓實例變成可調用對象

# %%
# 設計可調用的類別
class Counter:
    def __init__(self, start=0, step=1):
        self.value = start
        self.step = step
    
    # 讓實例可以像函數一樣調用
    def __call__(self, inc=None):
        if inc is None:
            # 無參數調用時，增加預設步長
            self.value += self.step
        else:
            # 有參數調用時，增加指定的值
            self.value += inc
        return self.value
    
    def reset(self, value=0):
        self.value = value
        return self
    
    def __str__(self):
        return f"Counter: {self.value}"

# 使用可調用實例
counter = Counter(start=10, step=2)
print(f"初始值: {counter.value}")

print(f"第一次調用: {counter()}")  # 使用預設步長
print(f"第二次調用: {counter()}")
print(f"使用指定增量: {counter(5)}")
print(f"重置後: {counter.reset(100)}")
print(f"重置後調用: {counter()}")

# 另一個例子: 可配置的格式化器
class Formatter:
    def __init__(self, format_str="{}"): 
        self.format_str = format_str
    
    def __call__(self, *args, **kwargs):
        return self.format_str.format(*args, **kwargs)
    
    def set_format(self, format_str):
        self.format_str = format_str
        return self

# 使用可調用的格式化器
money_fmt = Formatter("${:.2f}")
print(f"\n格式化金額: {money_fmt(123.456)}")

date_fmt = Formatter("{0:%Y-%m-%d}")
import datetime
print(f"格式化日期: {date_fmt(datetime.datetime.now())}")

# 改變格式
money_fmt.set_format("€{:.2f}")
print(f"更改格式後: {money_fmt(123.456)}")

# %% [markdown]
# ## 9. 自定義容器類別的方法

# %%
# 自定義列表類別
class BetterList:
    def __init__(self, items=None):
        self.items = [] if items is None else list(items)
    
    # 讓實例表現得像列表
    def __getitem__(self, index):
        return self.items[index]
    
    def __setitem__(self, index, value):
        self.items[index] = value
    
    def __delitem__(self, index):
        del self.items[index]
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)
    
    def __contains__(self, item):
        return item in self.items
    
    # 添加自定義方法
    def append(self, item):
        self.items.append(item)
        return self  # 支援鏈式調用
    
    def extend(self, items):
        self.items.extend(items)
        return self
    
    def pop(self, index=-1):
        return self.items.pop(index)
    
    def clear(self):
        self.items.clear()
        return self
    
    # 添加額外功能
    def sum(self):
        return sum(self.items)
    
    def average(self):
        if not self.items:
            return None
        return sum(self.items) / len(self.items)
    
    def map(self, func):
        # 返回新的 BetterList，原實例不變
        return BetterList(map(func, self.items))
    
    def filter(self, func):
        # 返回新的 BetterList，原實例不變
        return BetterList(filter(func, self.items))
    
    def __str__(self):
        return f"BetterList({self.items})"
    
    def __repr__(self):
        return self.__str__()

# 使用 BetterList 類別
bl = BetterList([1, 2, 3, 4, 5])
print(f"列表: {bl}")
print(f"第一個元素: {bl[0]}")
print(f"列表長度: {len(bl)}")
print(f"總和: {bl.sum()}")
print(f"平均值: {bl.average()}")

# 修改元素
bl[0] = 10
print(f"\n修改後: {bl}")

# 添加元素 (鏈式調用)
bl.append(6).append(7)
print(f"添加後: {bl}")

# 使用函數式方法
squares = bl.map(lambda x: x**2)
print(f"\n平方後: {squares}")

evens = bl.filter(lambda x: x % 2 == 0)
print(f"僅偶數: {evens}")

# 迭代
print("\n迭代元素:")
for item in bl:
    print(f"  {item}")

# %% [markdown]
# ## 10. 實作練習
# 
# 1. 設計一個 `Book` 類別，使用 `@property` 裝飾器實現書籍基本資訊的存取控制:
#    - 書名和作者一旦設置就不能改變 (只讀屬性)
#    - 頁數只能設為正數
#    - 價格必須在合理範圍內
#    - 提供借閱狀態的管理機制
# 
# 2. 設計一個 `EmailValidator` 描述器，用於驗證郵箱格式，並將它應用於一個 `User` 類別中。
# 
# 3. 實現一個支援鏈式調用的 `StringBuilder` 類別，包含添加文本、清除、替換等操作方法。 