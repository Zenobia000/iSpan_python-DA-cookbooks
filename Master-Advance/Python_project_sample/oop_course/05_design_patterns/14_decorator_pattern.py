# 14_decorator_pattern.py
# This file is part of the OOP course

"""
裝飾器模式 (Decorator Pattern)
============================
本模組介紹Python中的裝飾器模式，包括函數裝飾器和類裝飾器。

主題:
1. 函數裝飾器基礎
2. 帶參數的裝飾器
3. 裝飾類方法
4. 使用functools.wraps保留元數據
5. 裝飾器鏈與堆疊
6. 裝飾器模式在設計模式中的應用
"""

import functools
import time
from datetime import datetime


# 1. 基本函數裝飾器
print("="*50)
print("基本函數裝飾器")
print("="*50)

def simple_decorator(func):
    """基本裝飾器: 在函數執行前後增加日誌"""
    
    def wrapper(*args, **kwargs):
        print(f"[INFO] 準備執行 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[INFO] {func.__name__} 執行完成")
        return result
    
    return wrapper


@simple_decorator
def greet(name):
    """向用戶打招呼"""
    print(f"Hello, {name}!")


print("使用基本裝飾器:")
greet("小明")

# 演示不使用語法糖
def say_goodbye(name):
    print(f"Goodbye, {name}!")

decorated_say_goodbye = simple_decorator(say_goodbye)

print("\n不使用語法糖裝飾:")
decorated_say_goodbye("小紅")


# 2. 帶參數的裝飾器
print("\n"+"="*50)
print("帶參數的裝飾器")
print("="*50)

def repeat(n=1):
    """帶參數的裝飾器: 重複執行函數n次"""
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    
    return decorator


@repeat(3)
def say_hi(name):
    return f"Hi, {name}!"


print("重複裝飾器:")
results = say_hi("小李")
for i, result in enumerate(results, 1):
    print(f"第{i}次: {result}")


# 3. 保留函數元數據
print("\n"+"="*50)
print("使用functools.wraps保留元數據")
print("="*50)

def timer(func):
    """測量函數執行時間的裝飾器"""
    
    @functools.wraps(func)  # 保留原函數的元數據
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 執行時間: {end_time - start_time:.6f}秒")
        return result
    
    return wrapper


@timer
def slow_function(n):
    """一個故意執行得較慢的函數"""
    time.sleep(n)
    return f"完成{n}秒的操作"


print("帶計時器的函數:")
print(slow_function(1))

print("\n不使用@functools.wraps:")
print(f"裝飾前的函數名: slow_function")
print(f"裝飾後的函數名: {slow_function.__name__}")
print(f"裝飾後的文檔字符串: {slow_function.__doc__}")


# 4. 裝飾器鏈與堆疊
print("\n"+"="*50)
print("裝飾器鏈與堆疊")
print("="*50)

def bold(func):
    """將結果加粗的裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper


def italic(func):
    """將結果斜體化的裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper


def underline(func):
    """將結果加下劃線的裝飾器"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"
    return wrapper


@bold
@italic
@underline
def format_text(text):
    return text


print("裝飾器鏈 (從內到外執行):")
formatted = format_text("Hello, World!")
print(f"原始文本: Hello, World!")
print(f"格式化後: {formatted}")
print("執行順序: underline -> italic -> bold")


# 5. 裝飾類方法
print("\n"+"="*50)
print("裝飾類方法")
print("="*50)

def log_method(func):
    """記錄方法調用的裝飾器"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
              f"調用 {self.__class__.__name__}.{func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.is_active = False
    
    @log_method
    def activate(self):
        self.is_active = True
        return f"用戶 {self.username} 已激活"
    
    @log_method
    def deactivate(self):
        self.is_active = False
        return f"用戶 {self.username} 已停用"
    
    @staticmethod
    def validate_email(email):
        """驗證郵箱格式"""
        return '@' in email and '.' in email.split('@')[-1]


print("裝飾類方法:")
user = User("zhang_san", "zhang_san@example.com")
print(user.activate())
print(user.deactivate())


# 6. 類裝飾器
print("\n"+"="*50)
print("類裝飾器")
print("="*50)

def add_greeting(cls):
    """為類添加問候方法的類裝飾器"""
    
    def say_hello(self):
        return f"{self} says: Hello!"
    
    cls.say_hello = say_hello
    return cls


@add_greeting
class Person:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name


print("類裝飾器示例:")
person = Person("李明")
print(person.say_hello())


# 7. 裝飾器的實際應用
print("\n"+"="*50)
print("裝飾器的實際應用")
print("="*50)

# 7.1 認證裝飾器
def login_required(func):
    """檢查用戶是否已登入的裝飾器"""
    @functools.wraps(func)
    def wrapper(user, *args, **kwargs):
        if not getattr(user, 'is_authenticated', False):
            return "請先登入以訪問此功能"
        return func(user, *args, **kwargs)
    return wrapper


# 7.2 緩存裝飾器
def memoize(func):
    """緩存函數結果的裝飾器"""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"從緩存獲取結果: {args}")
            return cache[args]
        
        result = func(*args)
        cache[args] = result
        print(f"計算新結果: {args} -> {result}")
        return result
    
    return wrapper


@memoize
def fibonacci(n):
    """計算斐波那契數列的第n項"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


# 7.3 限速裝飾器
def rate_limit(max_calls, period=60):
    """限制函數在指定時間內的調用次數"""
    calls = []
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            # 清除超過時間周期的調用記錄
            while calls and calls[0] < current_time - period:
                calls.pop(0)
            
            if len(calls) >= max_calls:
                return f"調用頻率過高，請稍後再試 ({max_calls}次/{period}秒)"
            
            calls.append(current_time)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@rate_limit(max_calls=3, period=10)
def send_message(message):
    return f"發送消息: {message}"


# 展示各種裝飾器的應用
print("\n認證裝飾器示例:")
class User:
    def __init__(self, username, is_authenticated=False):
        self.username = username
        self.is_authenticated = is_authenticated

@login_required
def view_profile(user):
    return f"{user.username}的個人資料: ..."

user1 = User("guest")
user2 = User("admin", is_authenticated=True)

print(view_profile(user1))
print(view_profile(user2))

print("\n緩存裝飾器示例 (斐波那契):")
print(f"fibonacci(5) = {fibonacci(5)}")
print(f"fibonacci(5) (再次調用) = {fibonacci(5)}")
print(f"fibonacci(6) = {fibonacci(6)}")  # 會重用之前fibonacci(5)的結果

print("\n限速裝飾器示例:")
for i in range(5):
    print(f"調用 {i+1}: {send_message(f'消息 {i+1}')}")


# 8. 設計模式中的裝飾器模式
print("\n"+"="*50)
print("設計模式中的裝飾器模式")
print("="*50)

# 組件接口
class Component:
    """組件接口"""
    def operation(self):
        pass


# 具體組件
class ConcreteComponent(Component):
    """具體組件"""
    def operation(self):
        return "ConcreteComponent"


# 裝飾器基類
class Decorator(Component):
    """裝飾器基類"""
    def __init__(self, component):
        self._component = component
    
    def operation(self):
        return self._component.operation()


# 具體裝飾器A
class ConcreteDecoratorA(Decorator):
    """具體裝飾器A"""
    def operation(self):
        return f"ConcreteDecoratorA({super().operation()})"


# 具體裝飾器B
class ConcreteDecoratorB(Decorator):
    """具體裝飾器B"""
    def operation(self):
        return f"ConcreteDecoratorB({super().operation()})"


# 使用裝飾器模式
print("設計模式中的裝飾器模式示例:")
# 創建具體組件
simple = ConcreteComponent()
print(f"簡單組件: {simple.operation()}")

# 用裝飾器A裝飾組件
decorated_a = ConcreteDecoratorA(simple)
print(f"裝飾器A: {decorated_a.operation()}")

# 用裝飾器B裝飾已經被裝飾器A裝飾過的組件
decorated_ab = ConcreteDecoratorB(decorated_a)
print(f"裝飾器B(裝飾器A): {decorated_ab.operation()}")

# 也可以直接堆疊裝飾
decorated_ba = ConcreteDecoratorA(ConcreteDecoratorB(simple))
print(f"裝飾器A(裝飾器B): {decorated_ba.operation()}")


# 9. 實際應用: 咖啡訂購系統
print("\n"+"="*50)
print("實際應用: 咖啡訂購系統")
print("="*50)

# 飲料組件接口
class Beverage:
    """飲料接口"""
    def __init__(self):
        self._description = "未知飲料"
    
    def get_description(self):
        return self._description
    
    def cost(self):
        pass


# 具體飲料
class Espresso(Beverage):
    """濃縮咖啡"""
    def __init__(self):
        super().__init__()
        self._description = "濃縮咖啡"
    
    def cost(self):
        return 30.0


class HouseBlend(Beverage):
    """混合咖啡"""
    def __init__(self):
        super().__init__()
        self._description = "混合咖啡"
    
    def cost(self):
        return 25.0


# 調料裝飾器基類
class CondimentDecorator(Beverage):
    """調料裝飾器基類"""
    def __init__(self, beverage):
        super().__init__()
        self._beverage = beverage
    
    def get_description(self):
        return self._beverage.get_description()


# 具體調料裝飾器
class Milk(CondimentDecorator):
    """牛奶調料"""
    def __init__(self, beverage):
        super().__init__(beverage)
    
    def get_description(self):
        return f"{self._beverage.get_description()}, 加牛奶"
    
    def cost(self):
        return self._beverage.cost() + 5.0


class Mocha(CondimentDecorator):
    """摩卡調料"""
    def __init__(self, beverage):
        super().__init__(beverage)
    
    def get_description(self):
        return f"{self._beverage.get_description()}, 加摩卡"
    
    def cost(self):
        return self._beverage.cost() + 8.0


class Whip(CondimentDecorator):
    """鮮奶油調料"""
    def __init__(self, beverage):
        super().__init__(beverage)
    
    def get_description(self):
        return f"{self._beverage.get_description()}, 加鮮奶油"
    
    def cost(self):
        return self._beverage.cost() + 7.0


# 使用咖啡訂購系統
print("咖啡訂購系統示例:")

# 訂購一杯濃縮咖啡
beverage1 = Espresso()
print(f"{beverage1.get_description()}: ${beverage1.cost():.2f}")

# 訂購一杯加摩卡和鮮奶油的混合咖啡
beverage2 = HouseBlend()
beverage2 = Mocha(beverage2)
beverage2 = Whip(beverage2)
print(f"{beverage2.get_description()}: ${beverage2.cost():.2f}")

# 訂購一杯雙份摩卡加牛奶的濃縮咖啡
beverage3 = Espresso()
beverage3 = Mocha(beverage3)
beverage3 = Mocha(beverage3)  # 雙份摩卡
beverage3 = Milk(beverage3)
print(f"{beverage3.get_description()}: ${beverage3.cost():.2f}")

