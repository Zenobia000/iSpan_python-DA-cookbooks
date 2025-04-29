# 13_special_methods_operator_overloading.py
# This file is part of the OOP course

"""
特殊方法與運算符重載 (Special Methods and Operator Overloading)
===================================================
本模組展示Python中的特殊方法(魔術方法)和運算符重載。

主題:
1. 基本特殊方法: __str__, __repr__
2. 數值運算符重載
3. 比較運算符重載
4. 容器類型的特殊方法
5. 可調用對象和上下文管理器
"""

# 1. 基本特殊方法
print("="*50)
print("基本特殊方法: __str__, __repr__")
print("="*50)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        """對象的字符串表示，適合終端用戶閱讀"""
        return f"{self.name}, {self.age}歲"
    
    def __repr__(self):
        """對象的官方字符串表示，適合開發人員，應該可以重建對象"""
        return f"Person('{self.name}', {self.age})"


# 測試字符串表示
person = Person("張三", 30)
print(f"str(person): {str(person)}")
print(f"repr(person): {repr(person)}")

# 在容器中的表現
persons = [Person("張三", 30), Person("李四", 25)]
print(f"列表中的對象: {persons}")  # 使用__repr__


# 2. 數值運算符重載
print("\n"+"="*50)
print("數值運算符重載")
print("="*50)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    # 加法運算符 +
    def __add__(self, other):
        """實現向量加法: v1 + v2"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    # 減法運算符 -
    def __sub__(self, other):
        """實現向量減法: v1 - v2"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    # 數乘運算符 *
    def __mul__(self, scalar):
        """實現向量數乘: v * 標量"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    # 反向數乘運算符 *
    def __rmul__(self, scalar):
        """實現反向數乘: 標量 * v"""
        return self.__mul__(scalar)
    
    # 點積運算符 @
    def __matmul__(self, other):
        """實現向量點積: v1 @ v2"""
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        return NotImplemented
    
    # 絕對值運算符 abs()
    def __abs__(self):
        """實現向量的模: abs(v)"""
        import math
        return math.sqrt(self.x**2 + self.y**2)


# 測試數值運算符
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 - v2 = {v1 - v2}")
print(f"v1 * 2 = {v1 * 2}")
print(f"3 * v2 = {3 * v2}")
print(f"v1 @ v2 = {v1 @ v2}")  # 點積
print(f"|v1| = {abs(v1)}")  # 模


# 3. 比較運算符重載
print("\n"+"="*50)
print("比較運算符重載")
print("="*50)

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def __str__(self):
        return f"{self.width}x{self.height} 矩形"
    
    def area(self):
        return self.width * self.height
    
    # 等於運算符 ==
    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() == other.area()
    
    # 不等於運算符 !=
    def __ne__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() != other.area()
    
    # 小於運算符 <
    def __lt__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() < other.area()
    
    # 小於等於運算符 <=
    def __le__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() <= other.area()
    
    # 大於運算符 >
    def __gt__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() > other.area()
    
    # 大於等於運算符 >=
    def __ge__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.area() >= other.area()


# 測試比較運算符
rect1 = Rectangle(5, 4)  # 面積 = 20
rect2 = Rectangle(10, 2)  # 面積 = 20
rect3 = Rectangle(3, 6)  # 面積 = 18

print(f"rect1 = {rect1}, 面積 = {rect1.area()}")
print(f"rect2 = {rect2}, 面積 = {rect2.area()}")
print(f"rect3 = {rect3}, 面積 = {rect3.area()}")

print(f"rect1 == rect2? {rect1 == rect2}")
print(f"rect1 > rect3? {rect1 > rect3}")
print(f"rect3 < rect2? {rect3 < rect2}")

# 排序比較
rects = [rect1, rect2, rect3]
sorted_rects = sorted(rects)  # 基於__lt__排序
print(f"按面積排序: {[f'{r.width}x{r.height}' for r in sorted_rects]}")


# 4. 容器類型的特殊方法
print("\n"+"="*50)
print("容器類型的特殊方法")
print("="*50)

class ShoppingCart:
    def __init__(self):
        self.items = {}
    
    def add_item(self, item, price, quantity=1):
        """添加商品到購物車"""
        if item in self.items:
            self.items[item]['quantity'] += quantity
        else:
            self.items[item] = {'price': price, 'quantity': quantity}
    
    def remove_item(self, item, quantity=1):
        """從購物車移除商品"""
        if item in self.items:
            if self.items[item]['quantity'] <= quantity:
                del self.items[item]
            else:
                self.items[item]['quantity'] -= quantity
    
    # 長度運算符 len()
    def __len__(self):
        """返回購物車中的商品總數"""
        return sum(item['quantity'] for item in self.items.values())
    
    # 項目訪問 cart[key]
    def __getitem__(self, item):
        """獲取購物車中的商品信息"""
        if item in self.items:
            return self.items[item]
        raise KeyError(f"購物車中沒有 {item}")
    
    # 項目賦值 cart[key] = value
    def __setitem__(self, item, value):
        """設置購物車中的商品信息"""
        if not isinstance(value, dict) or 'price' not in value or 'quantity' not in value:
            raise ValueError("值必須是包含price和quantity的字典")
        self.items[item] = value
    
    # 項目刪除 del cart[key]
    def __delitem__(self, item):
        """從購物車中刪除商品"""
        if item in self.items:
            del self.items[item]
        else:
            raise KeyError(f"購物車中沒有 {item}")
    
    # 成員檢測 item in cart
    def __contains__(self, item):
        """檢查購物車是否包含商品"""
        return item in self.items
    
    # 迭代器 for item in cart
    def __iter__(self):
        """迭代購物車中的商品"""
        return iter(self.items)
    
    # 計算總價
    def total(self):
        """計算購物車總價"""
        return sum(item['price'] * item['quantity'] for item in self.items.values())


# 測試容器方法
cart = ShoppingCart()
cart.add_item("蘋果", 5.0, 3)
cart.add_item("香蕉", 3.5, 2)
cart.add_item("橙子", 4.0, 1)

print(f"購物車中有 {len(cart)} 件商品")
print(f"購物車中的商品: {list(cart)}")
print(f"購物車中是否有蘋果: {'蘋果' in cart}")
print(f"購物車中是否有葡萄: {'葡萄' in cart}")

# 訪問商品信息
print(f"蘋果的價格和數量: {cart['蘋果']}")

# 修改商品信息
cart["蘋果"] = {'price': 5.5, 'quantity': 4}
print(f"修改後蘋果的價格和數量: {cart['蘋果']}")

# 刪除商品
del cart["橙子"]
print(f"刪除橙子後的商品: {list(cart)}")

print(f"購物車總價: ${cart.total():.2f}")


# 5. 可調用對象和上下文管理器
print("\n"+"="*50)
print("可調用對象和上下文管理器")
print("="*50)

class Counter:
    def __init__(self, start=0):
        self.count = start
    
    # 可調用對象 __call__
    def __call__(self, increment=1):
        """每次調用時增加計數"""
        self.count += increment
        return self.count
    
    def reset(self):
        """重置計數器"""
        self.count = 0


# 測試可調用對象
counter = Counter(10)
print(f"初始計數: {counter.count}")
print(f"第一次調用: {counter()}")  # 增加1
print(f"第二次調用: {counter(5)}")  # 增加5
print(f"第三次調用: {counter()}")  # 增加1
counter.reset()
print(f"重置後: {counter.count}")


# 上下文管理器
class DatabaseConnection:
    def __init__(self, host, username):
        self.host = host
        self.username = username
        self.connected = False
    
    # 進入上下文 with
    def __enter__(self):
        """連接到數據庫"""
        print(f"連接到 {self.host} 數據庫，用戶名: {self.username}")
        self.connected = True
        return self
    
    # 退出上下文
    def __exit__(self, exc_type, exc_val, exc_tb):
        """關閉數據庫連接"""
        print(f"關閉到 {self.host} 的連接")
        self.connected = False
        # 如果有異常，返回True表示異常已處理
        if exc_type is not None:
            print(f"處理異常: {exc_type.__name__}: {exc_val}")
            return True
    
    def execute(self, query):
        """執行SQL查詢"""
        if not self.connected:
            raise RuntimeError("未連接到數據庫")
        print(f"執行查詢: {query}")


# 測試上下文管理器
print("\n正常使用上下文管理器:")
with DatabaseConnection("localhost", "admin") as db:
    db.execute("SELECT * FROM users")
    db.execute("UPDATE users SET active = 1")
print("數據庫操作完成")

print("\n處理上下文中的異常:")
try:
    with DatabaseConnection("remote-server", "root") as db:
        db.execute("SELECT * FROM products")
        # 故意引發異常
        raise ValueError("模擬一個錯誤")
        db.execute("這條不會執行")
    print("異常被上下文管理器處理")
except:
    print("異常未被處理")  # 如果__exit__返回True，不會執行到這裡

print("\n在上下文外使用連接:")
db = DatabaseConnection("testdb", "guest")
try:
    db.execute("這會失敗")
except RuntimeError as e:
    print(f"錯誤: {e}")


# 實際應用: 自定義數值類
if __name__ == "__main__":
    print("\n"+"="*50)
    print("實際應用: 實現分數類")
    print("="*50)
    
    class Fraction:
        def __init__(self, numerator, denominator):
            if denominator == 0:
                raise ZeroDivisionError("分母不能為零")
            
            # 計算最大公約數來簡化分數
            def gcd(a, b):
                while b:
                    a, b = b, a % b
                return a
            
            g = gcd(abs(numerator), abs(denominator))
            self.numerator = numerator // g
            self.denominator = denominator // g
            
            # 處理符號
            if self.denominator < 0:
                self.numerator = -self.numerator
                self.denominator = -self.denominator
        
        def __str__(self):
            if self.denominator == 1:
                return str(self.numerator)
            return f"{self.numerator}/{self.denominator}"
        
        def __repr__(self):
            return f"Fraction({self.numerator}, {self.denominator})"
        
        def __add__(self, other):
            if isinstance(other, Fraction):
                return Fraction(
                    self.numerator * other.denominator + other.numerator * self.denominator,
                    self.denominator * other.denominator
                )
            if isinstance(other, int):
                return Fraction(
                    self.numerator + other * self.denominator,
                    self.denominator
                )
            return NotImplemented
        
        def __radd__(self, other):
            return self.__add__(other)
        
        def __sub__(self, other):
            if isinstance(other, Fraction):
                return Fraction(
                    self.numerator * other.denominator - other.numerator * self.denominator,
                    self.denominator * other.denominator
                )
            if isinstance(other, int):
                return Fraction(
                    self.numerator - other * self.denominator,
                    self.denominator
                )
            return NotImplemented
        
        def __rsub__(self, other):
            if isinstance(other, int):
                return Fraction(
                    other * self.denominator - self.numerator,
                    self.denominator
                )
            return NotImplemented
        
        def __mul__(self, other):
            if isinstance(other, Fraction):
                return Fraction(
                    self.numerator * other.numerator,
                    self.denominator * other.denominator
                )
            if isinstance(other, int):
                return Fraction(self.numerator * other, self.denominator)
            return NotImplemented
        
        def __rmul__(self, other):
            return self.__mul__(other)
        
        def __truediv__(self, other):
            if isinstance(other, Fraction):
                return Fraction(
                    self.numerator * other.denominator,
                    self.denominator * other.numerator
                )
            if isinstance(other, int):
                return Fraction(self.numerator, self.denominator * other)
            return NotImplemented
        
        def __rtruediv__(self, other):
            if isinstance(other, int):
                return Fraction(other * self.denominator, self.numerator)
            return NotImplemented
        
        def __eq__(self, other):
            if isinstance(other, Fraction):
                return (self.numerator == other.numerator and 
                        self.denominator == other.denominator)
            if isinstance(other, int):
                return self.numerator == other * self.denominator
            return NotImplemented
        
        def __lt__(self, other):
            if isinstance(other, Fraction):
                return (self.numerator * other.denominator < 
                        other.numerator * self.denominator)
            if isinstance(other, int):
                return self.numerator < other * self.denominator
            return NotImplemented
        
        def __float__(self):
            return self.numerator / self.denominator
    
    
    # 測試分數運算
    f1 = Fraction(1, 4)  # 1/4
    f2 = Fraction(1, 2)  # 1/2
    
    print(f"f1 = {f1}")
    print(f"f2 = {f2}")
    print(f"f1 + f2 = {f1 + f2}")
    print(f"f2 - f1 = {f2 - f1}")
    print(f"f1 * f2 = {f1 * f2}")
    print(f"f2 / f1 = {f2 / f1}")
    
    print(f"f1 + 1 = {f1 + 1}")
    print(f"2 * f2 = {2 * f2}")
    print(f"1 - f1 = {1 - f1}")
    
    print(f"f1 == f2? {f1 == f2}")
    print(f"f1 < f2? {f1 < f2}")
    print(f"float(f1) = {float(f1)}")
    
    # 分數列表排序
    fractions = [Fraction(3, 4), Fraction(1, 2), Fraction(1, 8), Fraction(2, 3)]
    print(f"排序前: {fractions}")
    fractions.sort()
    print(f"排序後: {fractions}")

