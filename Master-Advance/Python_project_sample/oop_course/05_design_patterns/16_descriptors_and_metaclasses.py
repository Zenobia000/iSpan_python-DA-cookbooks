# 16_descriptors_and_metaclasses.py
# This file is part of the OOP course

"""
描述符與元類 (Descriptors and Metaclasses)
=====================================
本模組介紹Python中的描述符和元類的概念及應用。

主題:
1. 理解描述符協議 (__get__, __set__, __delete__)
2. 數據描述符與非數據描述符
3. 描述符的實際應用
4. 理解元類 (type與自定義元類)
5. 使用元類控制類的創建過程
6. 元類的實際應用
"""

import inspect
import types
import warnings
from datetime import datetime


# 1. 描述符協議
print("="*50)
print("描述符協議")
print("="*50)

class Descriptor:
    """基本描述符"""
    
    def __get__(self, obj, objtype=None):
        print(f"調用 __get__: obj={obj}, objtype={objtype}")
        return "描述符值"
    
    def __set__(self, obj, value):
        print(f"調用 __set__: obj={obj}, value={value}")
    
    def __delete__(self, obj):
        print(f"調用 __delete__: obj={obj}")


class SampleClass:
    """使用描述符的示例類"""
    
    # 描述符是類屬性
    descriptor = Descriptor()


# 測試描述符
print("基本描述符示例:")
sample = SampleClass()

# 獲取描述符的值
print("\n獲取描述符值:")
print(f"SampleClass.descriptor = {SampleClass.descriptor}")  # 通過類訪問
print(f"sample.descriptor = {sample.descriptor}")  # 通過實例訪問

# 設置描述符的值
print("\n設置描述符值:")
sample.descriptor = "新值"

# 刪除描述符
print("\n刪除描述符:")
try:
    del sample.descriptor
except Exception as e:
    print(f"刪除失敗: {e}")


# 2. 數據描述符與非數據描述符
print("\n"+"="*50)
print("數據描述符與非數據描述符")
print("="*50)

class DataDescriptor:
    """數據描述符: 定義了__get__和__set__"""
    
    def __get__(self, obj, objtype=None):
        print("DataDescriptor.__get__")
        return obj._value if obj and hasattr(obj, '_value') else None
    
    def __set__(self, obj, value):
        print("DataDescriptor.__set__")
        obj._value = value


class NonDataDescriptor:
    """非數據描述符: 只定義了__get__"""
    
    def __get__(self, obj, objtype=None):
        print("NonDataDescriptor.__get__")
        return "NonDataDescriptor值"


class Demo:
    """演示數據描述符和非數據描述符的區別"""
    
    data_desc = DataDescriptor()  # 數據描述符
    non_data_desc = NonDataDescriptor()  # 非數據描述符
    
    def __init__(self):
        # 實例屬性
        self.data_desc = "實例data_desc屬性"  # 不會覆蓋數據描述符
        self.non_data_desc = "實例non_data_desc屬性"  # 會覆蓋非數據描述符


# 測試描述符優先順序
print("描述符優先順序:")
demo = Demo()

print("\n訪問屬性:")
print(f"demo.data_desc = {demo.data_desc}")  # 數據描述符優先
print(f"demo.non_data_desc = {demo.non_data_desc}")  # 實例屬性優先

# 說明屬性查找順序
print("\n屬性查找順序:")
print("1. 數據描述符 (定義了__get__和__set__)")
print("2. 實例字典 (__dict__)")
print("3. 非數據描述符 (只定義了__get__)")
print("4. 類字典")
print("5. 父類查找 (__mro__)")
print("6. __getattr__方法 (如果定義了)")


# 3. 描述符的實際應用
print("\n"+"="*50)
print("描述符的實際應用")
print("="*50)

# 類型檢查描述符
class Typed:
    """類型檢查描述符"""
    
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__[self.name]
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type.__name__}, got {type(value).__name__}")
        obj.__dict__[self.name] = value


# 範圍驗證描述符
class Range:
    """範圍驗證描述符"""
    
    def __init__(self, name, min_value=None, max_value=None):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__[self.name]
    
    def __set__(self, obj, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} 不能小於 {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} 不能大於 {self.max_value}")
        obj.__dict__[self.name] = value


# 結合多個描述符
class Person:
    """使用描述符的Person類"""
    
    name = Typed("name", str)
    age = Typed("age", int)
    age = Range("age", 0, 120)  # 同時使用類型和範圍檢查
    
    def __init__(self, name, age):
        self.name = name
        self.age = age


# 測試描述符應用
print("使用描述符進行數據驗證:")
# 創建有效的Person
person = Person("張三", 30)
print(f"有效的Person: {person.name}, {person.age}歲")

# 嘗試違反類型
print("\n嘗試使用無效的類型:")
try:
    person.age = "三十"  # 應該拋出TypeError
except TypeError as e:
    print(f"類型錯誤: {e}")

# 嘗試違反範圍
print("\n嘗試使用無效的範圍:")
try:
    person.age = 150  # 應該拋出ValueError
except ValueError as e:
    print(f"值錯誤: {e}")


# 屬性描述符 (Property裝飾器的實現原理)
class Property:
    """簡單的屬性描述符"""
    
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or fget.__doc__ if fget else None
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("無法讀取屬性")
        return self.fget(obj)
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("無法設置屬性")
        self.fset(obj, value)
    
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("無法刪除屬性")
        self.fdel(obj)
    
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)
    
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)
    
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


# 使用自定義Property
class Temperature:
    """使用自定義Property描述符"""
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    def get_celsius(self):
        return self._celsius
    
    def set_celsius(self, value):
        if value < -273.15:
            raise ValueError("溫度不能低於絕對零度")
        self._celsius = value
    
    def del_celsius(self):
        raise AttributeError("無法刪除溫度")
    
    # 使用自定義的Property描述符
    celsius = Property(get_celsius, set_celsius, del_celsius, "溫度(攝氏度)")
    
    # 使用標準的property
    @property
    def fahrenheit(self):
        """溫度(華氏度)"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9


# 測試Property
print("\nProperty描述符示例:")
temp = Temperature(25)
print(f"攝氏度: {temp.celsius}°C")
print(f"華氏度: {temp.fahrenheit}°F")

temp.celsius = 30
print(f"設置新攝氏度: {temp.celsius}°C")
print(f"對應華氏度: {temp.fahrenheit}°F")

temp.fahrenheit = 68
print(f"設置新華氏度: {temp.fahrenheit}°F")
print(f"對應攝氏度: {temp.celsius}°C")

try:
    temp.celsius = -300  # 低於絕對零度
except ValueError as e:
    print(f"溫度錯誤: {e}")


# 4. 元類 (Metaclasses)
print("\n"+"="*50)
print("元類 (Metaclasses)")
print("="*50)

# 探索Python的類型系統
print("Python的類型系統:")
a = 42
print(f"a = {a}, type(a) = {type(a)}, type(type(a)) = {type(type(a))}")

class MyClass:
    pass

obj = MyClass()
print(f"obj = {obj}, type(obj) = {type(obj)}, type(type(obj)) = {type(type(obj))}")
print(f"type(MyClass) = {type(MyClass)}")
print("所有類的類型都是type，type是一個元類")

# 使用type動態創建類
print("\n使用type動態創建類:")
# type(name, bases, dict) -> 創建一個新類
DynamicClass = type("DynamicClass", (object,), {
    "x": 10,
    "say_hello": lambda self: f"Hello from {self.__class__.__name__}"
})

dynamic_obj = DynamicClass()
print(f"動態創建的類: {DynamicClass.__name__}")
print(f"屬性x: {dynamic_obj.x}")
print(f"方法say_hello: {dynamic_obj.say_hello()}")


# 5. 自定義元類
print("\n"+"="*50)
print("自定義元類")
print("="*50)

class Meta(type):
    """自定義元類"""
    
    def __new__(mcs, name, bases, namespace):
        print(f"Meta.__new__ 被調用")
        print(f"  類名: {name}")
        print(f"  父類: {bases}")
        print(f"  命名空間: {list(namespace.keys())}")
        return super().__new__(mcs, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace):
        print(f"Meta.__init__ 被調用")
        super().__init__(name, bases, namespace)
    
    def __call__(cls, *args, **kwargs):
        print(f"Meta.__call__ 被調用")
        instance = super().__call__(*args, **kwargs)
        return instance


# 使用自定義元類
print("使用自定義元類:")
class MyClassWithMeta(metaclass=Meta):
    """使用Meta作為元類的類"""
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"MyClassWithMeta({self.value})"


print("\n創建自定義元類的實例:")
instance = MyClassWithMeta(42)
print(f"instance: {instance}")


# 6. 元類的實際應用
print("\n"+"="*50)
print("元類的實際應用")
print("="*50)

# 使用元類自動註冊子類
class RegistryMeta(type):
    """自動註冊所有子類的元類"""
    
    _registry = {}
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != "PluginBase":  # 不註冊基類
            mcs._registry[name] = cls
        return cls
    
    @classmethod
    def get_registry(mcs):
        return dict(mcs._registry)


# 使用RegistryMeta
class PluginBase(metaclass=RegistryMeta):
    """插件系統的基類"""
    
    def execute(self):
        raise NotImplementedError("子類必須實現execute方法")


# 創建一些插件子類
class TextPlugin(PluginBase):
    """文本處理插件"""
    
    def execute(self):
        return "TextPlugin 正在處理文本"


class ImagePlugin(PluginBase):
    """圖片處理插件"""
    
    def execute(self):
        return "ImagePlugin 正在處理圖片"


class AudioPlugin(PluginBase):
    """音頻處理插件"""
    
    def execute(self):
        return "AudioPlugin 正在處理音頻"


# 檢查註冊表
print("元類自動註冊子類:")
registry = RegistryMeta.get_registry()
print(f"已註冊的插件: {list(registry.keys())}")

# 使用註冊表動態加載插件
print("\n動態加載和使用插件:")
for name, plugin_cls in registry.items():
    plugin = plugin_cls()
    print(f"使用 {name}: {plugin.execute()}")


# 使用元類實現單例模式
class SingletonMeta(type):
    """實現單例模式的元類"""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# 使用SingletonMeta
class Database(metaclass=SingletonMeta):
    """數據庫連接器 (單例)"""
    
    def __init__(self, host="localhost"):
        print(f"連接到數據庫: {host}")
        self.host = host
    
    def query(self, sql):
        print(f"在 {self.host} 上執行: {sql}")


# 測試單例模式
print("\n元類實現單例模式:")
db1 = Database("server1")
db2 = Database("server2")  # 不會創建新實例

print(f"db1 is db2? {db1 is db2}")
db1.query("SELECT * FROM users")
db2.query("SELECT * FROM products")


# 使用元類實現屬性驗證
class ValidateMeta(type):
    """用於驗證類屬性的元類"""
    
    def __new__(mcs, name, bases, namespace):
        # 獲取字段驗證規則
        validators = namespace.get('__validators__', {})
        
        # 創建新的__init__方法，添加驗證邏輯
        original_init = namespace.get('__init__', lambda self, *args, **kwargs: None)
        
        def validated_init(self, *args, **kwargs):
            # 調用原來的__init__
            original_init(self, *args, **kwargs)
            
            # 驗證字段
            for field, validator in validators.items():
                if hasattr(self, field):
                    value = getattr(self, field)
                    if not validator(value):
                        raise ValueError(f"字段 '{field}' 驗證失敗: {value}")
        
        namespace['__init__'] = validated_init
        return super().__new__(mcs, name, bases, namespace)


# 使用ValidateMeta
class ModelWithValidation(metaclass=ValidateMeta):
    """帶有字段驗證的模型基類"""
    
    __validators__ = {
        'age': lambda x: isinstance(x, int) and 0 <= x <= 120,
        'email': lambda x: isinstance(x, str) and '@' in x
    }
    
    def __init__(self, age, email):
        self.age = age
        self.email = email


# 測試屬性驗證
print("\n元類實現屬性驗證:")
try:
    # 有效模型
    model = ModelWithValidation(30, "user@example.com")
    print(f"有效模型: age={model.age}, email={model.email}")
    
    # 無效模型
    invalid_model = ModelWithValidation(150, "invalid-email")
except ValueError as e:
    print(f"驗證錯誤: {e}")


# 7. 實際應用: ORM (對象關係映射)
print("\n"+"="*50)
print("實際應用: 簡單的ORM")
print("="*50)

class Field:
    """數據庫欄位描述符基類"""
    
    def __init__(self, name=None, primary_key=False):
        self.name = name  # 欄位名稱
        self.primary_key = primary_key
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._data.get(self.name)
    
    def __set__(self, instance, value):
        instance._data[self.name] = value


class IntegerField(Field):
    """整數類型欄位"""
    
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"字段 {self.name} 必須是整數")
        super().__set__(instance, value)


class StringField(Field):
    """字符串類型欄位"""
    
    def __init__(self, name=None, primary_key=False, max_length=None):
        super().__init__(name, primary_key)
        self.max_length = max_length
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"字段 {self.name} 必須是字符串")
        if self.max_length and len(value) > self.max_length:
            raise ValueError(f"字段 {self.name} 長度不能超過 {self.max_length}")
        super().__set__(instance, value)


class ModelMeta(type):
    """ORM模型的元類"""
    
    def __new__(mcs, name, bases, namespace):
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)
        
        # 收集欄位信息
        fields = {}
        table_name = name.lower()
        
        for key, value in namespace.items():
            if isinstance(value, Field):
                fields[key] = value
                value.name = key
        
        # 更新命名空間
        namespace['__fields__'] = fields
        namespace['__table__'] = table_name
        
        # 創建新類
        cls = super().__new__(mcs, name, bases, namespace)
        return cls


class Model(metaclass=ModelMeta):
    """ORM模型基類"""
    
    def __init__(self, **kwargs):
        self._data = {}
        for key, value in kwargs.items():
            if key in self.__fields__:
                setattr(self, key, value)
    
    @classmethod
    def table_name(cls):
        return cls.__table__
    
    def save(self):
        """保存模型到數據庫 (模擬)"""
        fields = []
        values = []
        for name, field in self.__fields__.items():
            fields.append(name)
            values.append(repr(getattr(self, name)))
        
        sql = f"INSERT INTO {self.__table__} ({', '.join(fields)}) VALUES ({', '.join(values)})"
        print(f"執行SQL: {sql}")
    
    @classmethod
    def all(cls):
        """從數據庫獲取所有記錄 (模擬)"""
        print(f"SELECT * FROM {cls.__table__}")
        return []


# 使用ORM模型
class User(Model):
    """用戶模型"""
    
    id = IntegerField(primary_key=True)
    name = StringField(max_length=100)
    email = StringField(max_length=200)
    age = IntegerField()


# 測試ORM
print("簡單ORM示例:")
# 創建模型實例
user = User(id=1, name="張三", email="zhang@example.com", age=30)

# 顯示模型信息
print(f"表名: {User.table_name()}")
print(f"欄位: {list(User.__fields__.keys())}")

# 保存模型
user.save()

# 獲取所有用戶
User.all()

# 嘗試設置無效值
try:
    user.age = "三十"  # 應該拋出TypeError
except TypeError as e:
    print(f"類型錯誤: {e}")

try:
    user.name = "x" * 200  # 應該拋出ValueError
except ValueError as e:
    print(f"值錯誤: {e}")


# 8. 高級描述符: 管理對象生命周期
print("\n"+"="*50)
print("高級描述符: 管理對象生命周期")
print("="*50)

class LazyProperty:
    """延遲加載的屬性描述符"""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # 延遲計算並緩存結果
        value = self.func(obj)
        setattr(obj, self.name, value)  # 替換描述符
        return value


class ExpirableProperty:
    """具有過期時間的屬性描述符"""
    
    def __init__(self, expires_in_secs=60):
        self.expires_in_secs = expires_in_secs
        self.name = None
        self.cache_name = None
        self.timestamp_name = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.cache_name = f"_{name}_cache"
        self.timestamp_name = f"_{name}_timestamp"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        now = datetime.now().timestamp()
        timestamp = getattr(obj, self.timestamp_name, 0)
        
        # 檢查是否過期
        if now - timestamp > self.expires_in_secs:
            # 過期或不存在，需要重新生成
            cache = getattr(obj, self.name + "_generate")()
            setattr(obj, self.cache_name, cache)
            setattr(obj, self.timestamp_name, now)
            return cache
        
        # 未過期，使用緩存
        return getattr(obj, self.cache_name)


# 測試延遲加載屬性
class DataManager:
    """使用延遲加載屬性的數據管理器"""
    
    def __init__(self):
        self.name = "DataManager"
    
    @LazyProperty
    def expensive_data(self):
        print("計算昂貴數據...")
        time.sleep(1)  # 模擬昂貴的計算
        return [i**2 for i in range(1000)]
    
    # 使用過期屬性
    weather = ExpirableProperty(expires_in_secs=10)
    
    def weather_generate(self):
        print("獲取最新天氣數據...")
        return {"temp": 25, "cond": "晴天", "timestamp": datetime.now().strftime("%H:%M:%S")}


# 測試延遲加載和過期屬性
print("延遲加載和過期屬性示例:")
dm = DataManager()

print("\n延遲加載屬性:")
print("訪問前...")
start = time.time()
data = dm.expensive_data
print(f"首次訪問 (耗時: {time.time() - start:.2f}秒): {len(data)} 項")

start = time.time()
data = dm.expensive_data
print(f"再次訪問 (耗時: {time.time() - start:.2f}秒): {len(data)} 項")

print("\n過期屬性:")
print("首次訪問weather:")
print(dm.weather)
print("短時間內再次訪問:")
print(dm.weather)  # 應該使用緩存

print("等待屬性過期...")
time.sleep(11)  # 等待超過10秒
print("過期後訪問:")
print(dm.weather)  # 應該重新獲取

