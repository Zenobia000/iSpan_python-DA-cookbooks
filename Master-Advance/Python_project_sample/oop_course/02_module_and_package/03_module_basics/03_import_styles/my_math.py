# 模組層級變數
PI = 3.14159

# 模組函數
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("除數不能為零")
    return a / b

# 模組類
class Calculator:
    # self 表示的是 class 這個物件本身，因為class是設計稿，而物件是實體，
    # 所以self表示的是實體本身，而不是設計稿
    def __init__(self, initial_value=0):
        self.value = initial_value
    
    def add(self, x):
        self.value += x
        return self.value
    
    def subtract(self, x):
        self.value -= x
        return self.value
        
    def reset(self):
        self.value = 0
        return self.value

