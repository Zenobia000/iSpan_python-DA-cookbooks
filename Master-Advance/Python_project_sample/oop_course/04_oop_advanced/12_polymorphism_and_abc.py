# 12_polymorphism_and_abc.py
# This file is part of the OOP course

"""
多態和抽象基類 (Polymorphism and ABC)
====================================
本模組展示Python中的多態概念和抽象基類的使用。

主題:
1. 多態基礎
2. 鴨子類型 (Duck Typing)
3. 抽象基類 (Abstract Base Classes, ABC)
4. 介面設計與實現
"""

import abc
from abc import ABC, abstractmethod

# 1. 多態基礎
print("="*50)
print("多態基礎")
print("="*50)

class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪!"

class Cat(Animal):
    def speak(self):
        return "喵喵!"

class Duck(Animal):
    def speak(self):
        return "嘎嘎!"

# 多態函數
def animal_sound(animal):
    print(animal.speak())

# 測試多態
dog = Dog()
cat = Cat()
duck = Duck()

print("不同動物的叫聲:")
animal_sound(dog)
animal_sound(cat)
animal_sound(duck)

# 2. 鴨子類型 (Duck Typing)
print("\n"+"="*50)
print("鴨子類型 (Duck Typing)")
print("="*50)

class Person:
    def speak(self):
        return "你好!"

# 注意Person不是Animal的子類，但它有speak方法
person = Person()
print("person.speak():", person.speak())
print("使用相同的animal_sound函數處理Person:")
animal_sound(person)  # 這裡展示了鴨子類型 - 只要有speak方法即可

# 3. 抽象基類 (ABC)
print("\n"+"="*50)
print("抽象基類 (ABC)")
print("="*50)

class Shape(ABC):
    @abstractmethod
    def area(self):
        """計算面積"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """計算周長"""
        pass
    
    def description(self):
        """形狀的通用描述"""
        return f"這是一個{type(self).__name__}形狀"


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius


try:
    # 嘗試實例化抽象類
    shape = Shape()
except TypeError as e:
    print(f"無法實例化Shape: {e}")

# 實例化具體類
rectangle = Rectangle(5, 3)
circle = Circle(4)

print(f"\n矩形描述: {rectangle.description()}")
print(f"矩形面積: {rectangle.area()}")
print(f"矩形周長: {rectangle.perimeter()}")

print(f"\n圓形描述: {circle.description()}")
print(f"圓形面積: {circle.area():.2f}")
print(f"圓形周長: {circle.perimeter():.2f}")


# 4. 介面設計
print("\n"+"="*50)
print("介面設計")
print("="*50)

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        """繪製對象"""
        pass

class Resizable(ABC):
    @abstractmethod
    def resize(self, factor):
        """調整對象大小"""
        pass

# 實現多個介面
class DrawableRectangle(Rectangle, Drawable):
    def draw(self):
        print(f"繪製一個 {self.width}x{self.height} 的矩形")

class ResizableCircle(Circle, Resizable):
    def resize(self, factor):
        self.radius *= factor
        print(f"圓的半徑調整為 {self.radius}")

# 同時實現多個介面
class DrawableResizableCircle(Circle, Drawable, Resizable):
    def draw(self):
        print(f"繪製一個半徑為 {self.radius} 的圓")
    
    def resize(self, factor):
        self.radius *= factor
        print(f"圓的半徑調整為 {self.radius}")

# 測試介面
drawable_rect = DrawableRectangle(10, 5)
drawable_rect.draw()
print(f"矩形面積: {drawable_rect.area()}")

print()
resizable_circle = ResizableCircle(3)
print(f"圓形面積: {resizable_circle.area():.2f}")
resizable_circle.resize(2)
print(f"調整後的圓形面積: {resizable_circle.area():.2f}")

print()
super_circle = DrawableResizableCircle(4)
super_circle.draw()
print(f"圓形面積: {super_circle.area():.2f}")
super_circle.resize(0.5)
super_circle.draw()
print(f"調整後的圓形面積: {super_circle.area():.2f}")


# 5. 實際應用: 插件系統
print("\n"+"="*50)
print("實際應用: 抽象基類實現插件系統")
print("="*50)

class Plugin(ABC):
    @abstractmethod
    def activate(self):
        """激活插件"""
        pass
    
    @abstractmethod
    def deactivate(self):
        """停用插件"""
        pass
    
    @property
    @abstractmethod
    def name(self):
        """插件名稱"""
        pass


class TextFormatterPlugin(Plugin):
    @property
    def name(self):
        return "文本格式化器"
    
    def activate(self):
        print(f"[{self.name}] 已激活")
    
    def deactivate(self):
        print(f"[{self.name}] 已停用")
    
    def format_text(self, text):
        return text.strip().title()


class SpellCheckerPlugin(Plugin):
    @property
    def name(self):
        return "拼寫檢查器"
    
    def activate(self):
        print(f"[{self.name}] 已激活")
    
    def deactivate(self):
        print(f"[{self.name}] 已停用")
    
    def check_spelling(self, text):
        print(f"[{self.name}] 檢查 '{text}' 的拼寫")
        return "拼寫正確"


class PluginManager:
    def __init__(self):
        self.plugins = {}
    
    def register_plugin(self, plugin):
        if not isinstance(plugin, Plugin):
            raise TypeError("只能註冊Plugin子類")
        self.plugins[plugin.name] = plugin
        print(f"已註冊插件: {plugin.name}")
    
    def activate_all(self):
        for plugin in self.plugins.values():
            plugin.activate()
    
    def deactivate_all(self):
        for plugin in self.plugins.values():
            plugin.deactivate()
    
    def get_plugin(self, name):
        return self.plugins.get(name)


# 使用插件系統
manager = PluginManager()
manager.register_plugin(TextFormatterPlugin())
manager.register_plugin(SpellCheckerPlugin())

manager.activate_all()
print()

# 使用特定插件
formatter = manager.get_plugin("文本格式化器")
if formatter:
    sample_text = "  這是一個示例文本   "
    print(f"原始文本: '{sample_text}'")
    print(f"格式化後: '{formatter.format_text(sample_text)}'")

spellchecker = manager.get_plugin("拼寫檢查器")
if spellchecker:
    result = spellchecker.check_spelling("Python是一種程式語言")
    print(f"拼寫檢查結果: {result}")

print()
manager.deactivate_all()

