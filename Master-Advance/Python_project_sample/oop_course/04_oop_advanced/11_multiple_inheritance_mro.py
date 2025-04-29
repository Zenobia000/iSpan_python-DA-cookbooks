# 11_multiple_inheritance_mro.py
# This file is part of the OOP course

"""
多重繼承與方法解析順序 (Multiple Inheritance and MRO)
================================================
本模組展示Python中的多重繼承和方法解析順序(Method Resolution Order)機制。

主題:
1. 多重繼承基礎
2. 方法解析順序(MRO)
3. C3線性化算法
4. super()在多重繼承中的行為
"""

# 1. 多重繼承基礎
print("="*50)
print("多重繼承基礎")
print("="*50)

class A:
    def method(self):
        print("A.method() 被調用")

class B:
    def method(self):
        print("B.method() 被調用")

class C(A, B):
    pass

class D(B, A):
    pass

# 實例化並測試
c = C()
d = D()

print("C繼承順序(A, B):")
c.method()  # 輸出: A.method() 被調用

print("D繼承順序(B, A):")
d.method()  # 輸出: B.method() 被調用


# 2. 方法解析順序 (MRO)
print("\n"+"="*50)
print("方法解析順序 (MRO)")
print("="*50)

# 查看類的MRO
print(f"C的MRO: {C.__mro__}")
print(f"D的MRO: {D.__mro__}")


# 3. 複雜的繼承結構和菱形繼承問題
print("\n"+"="*50)
print("複雜的繼承結構和菱形繼承")
print("="*50)

class Base:
    def method(self):
        print("Base.method() 被調用")

class X(Base):
    def method(self):
        print("X.method() 被調用")
        super().method()

class Y(Base):
    def method(self):
        print("Y.method() 被調用")
        super().method()

class Z(X, Y):
    def method(self):
        print("Z.method() 被調用")
        super().method()

# 分析MRO
print(f"Z的MRO: {Z.__mro__}")

# 調用方法觀察執行順序
z = Z()
print("\n調用Z().method():")
z.method()
# 輸出順序:
# Z.method() 被調用
# X.method() 被調用
# Y.method() 被調用
# Base.method() 被調用


# 4. super()的進階用法
print("\n"+"="*50)
print("super()的進階用法")
print("="*50)

class A:
    def __init__(self):
        print("A.__init__() 被調用")
        self.a = "A"

class B(A):
    def __init__(self):
        print("B.__init__() 被調用")
        super().__init__()
        self.b = "B"

class C(A):
    def __init__(self):
        print("C.__init__() 被調用")
        super().__init__()
        self.c = "C"

class D(B, C):
    def __init__(self):
        print("D.__init__() 被調用")
        super().__init__()
        self.d = "D"

# 創建D的實例
print("創建D類的實例:")
d = D()
print("\nD實例的屬性:", d.__dict__)

# 顯示D的MRO
print("\nD的繼承順序:", D.__mro__)


# 5. 實際應用: Mixin模式
print("\n"+"="*50)
print("實際應用: Mixin模式")
print("="*50)

class LoggerMixin:
    """提供日誌功能的Mixin類"""
    
    def log(self, message):
        print(f"[LOG] {message}")

class SerializerMixin:
    """提供序列化功能的Mixin類"""
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    def to_json(self):
        import json
        return json.dumps(self.to_dict())

class ValidationMixin:
    """提供數據驗證功能的Mixin類"""
    
    def validate(self):
        """檢查所有必需的字段是否存在"""
        for field in getattr(self, 'required_fields', []):
            if not hasattr(self, field) or getattr(self, field) is None:
                return False
        return True

# 應用Mixin的實體類
class User(LoggerMixin, SerializerMixin, ValidationMixin):
    """結合多個Mixin的用戶類"""
    
    required_fields = ['name', 'email']
    
    def __init__(self, name=None, email=None, age=None):
        self.name = name
        self.email = email
        self.age = age
        self.log(f"創建用戶: {name}")
    
    def save(self):
        """保存用戶數據"""
        if self.validate():
            self.log(f"儲存用戶 {self.name} 的數據")
            print(f"用戶數據已保存: {self.to_json()}")
            return True
        else:
            self.log(f"用戶數據驗證失敗")
            return False

# 創建和測試User實例
valid_user = User(name="測試用戶", email="test@example.com", age=30)
valid_user.save()  # 應該成功

print()
invalid_user = User(name="未完成用戶")
invalid_user.save()  # 應該失敗，缺少email

# 顯示User的MRO
print("\nUser的MRO:", User.__mro__)

