# 17_common_design_patterns.py
# This file is part of the OOP course

"""
常見設計模式 (Common Design Patterns)
===================================
本模組介紹Python中常見的設計模式實現及應用。

主題:
1. 創建型模式 (Creational Patterns)
2. 結構型模式 (Structural Patterns)
3. 行為型模式 (Behavioral Patterns)
4. Python特有的設計模式應用
"""

print("="*50)
print("設計模式簡介")
print("="*50)
print("設計模式是軟體設計中常見問題的可重用解決方案")
print("設計模式通常分為三類:")
print("1. 創建型模式: 處理對象創建機制")
print("2. 結構型模式: 處理類和對象的組合")
print("3. 行為型模式: 處理對象之間的通信和責任分配")

# 1. 創建型模式
print("\n"+"="*50)
print("1. 創建型模式 (Creational Patterns)")
print("="*50)

# 1.1 單例模式 (Singleton)
print("\n"+"="*40)
print("1.1 單例模式 (Singleton)")
print("="*40)
print("確保類只有一個實例，並提供一個全局訪問點")

class Singleton:
    """使用__new__方法實現單例模式"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# 測試單例模式
print("\n單例模式測試:")
s1 = Singleton()
s2 = Singleton()
print(f"s1 is s2? {s1 is s2}")  # 應該是True

# 裝飾器實現單例
print("\n裝飾器實現單例:")

def singleton(cls):
    """單例裝飾器"""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Config:
    """配置類"""
    def __init__(self):
        self.settings = {}
    
    def set(self, key, value):
        self.settings[key] = value
    
    def get(self, key, default=None):
        return self.settings.get(key, default)


# 測試裝飾器單例
config1 = Config()
config1.set("theme", "dark")

config2 = Config()
print(f"config1 is config2? {config1 is config2}")  # 應該是True
print(f"theme設置: {config2.get('theme')}")  # 應該是"dark"


# 1.2 工廠模式 (Factory)
print("\n"+"="*40)
print("1.2 工廠模式 (Factory)")
print("="*40)
print("定義創建對象的接口，但讓子類決定實例化的類")

# 簡單工廠
class Animal:
    """動物基類"""
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪!"

class Cat(Animal):
    def speak(self):
        return "喵喵!"

class AnimalFactory:
    """動物工廠"""
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"未知動物類型: {animal_type}")


# 測試簡單工廠
print("\n簡單工廠測試:")
factory = AnimalFactory()
dog = factory.create_animal("dog")
cat = factory.create_animal("cat")

print(f"狗說: {dog.speak()}")
print(f"貓說: {cat.speak()}")


# 工廠方法
class TransportFactory:
    """運輸工具工廠基類"""
    def create_transport(self):
        """創建運輸工具的工廠方法"""
        pass
    
    def deliver(self):
        """運送方法"""
        transport = self.create_transport()
        return f"使用{transport.name}運送貨物: {transport.delivery_method()}"

class Transport:
    """運輸工具基類"""
    name = "未知運輸工具"
    
    def delivery_method(self):
        pass

class Truck(Transport):
    """卡車"""
    name = "卡車"
    
    def delivery_method(self):
        return "通過公路運輸"

class Ship(Transport):
    """船舶"""
    name = "船舶"
    
    def delivery_method(self):
        return "通過海運運輸"

class TruckFactory(TransportFactory):
    """卡車工廠"""
    def create_transport(self):
        return Truck()

class ShipFactory(TransportFactory):
    """船舶工廠"""
    def create_transport(self):
        return Ship()


# 測試工廠方法
print("\n工廠方法測試:")
truck_factory = TruckFactory()
ship_factory = ShipFactory()

print(truck_factory.deliver())
print(ship_factory.deliver())


# 1.3 建造者模式 (Builder)
print("\n"+"="*40)
print("1.3 建造者模式 (Builder)")
print("="*40)
print("將複雜對象的構建與表示分離，使同一構建過程可創建不同表示")

class Computer:
    """電腦類"""
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.gpu = None
    
    def __str__(self):
        components = []
        if self.cpu:
            components.append(f"CPU: {self.cpu}")
        if self.memory:
            components.append(f"內存: {self.memory}")
        if self.storage:
            components.append(f"硬盤: {self.storage}")
        if self.gpu:
            components.append(f"顯卡: {self.gpu}")
        
        return "電腦配置:\n" + "\n".join(components)


class ComputerBuilder:
    """電腦建造者基類"""
    def __init__(self):
        self.computer = Computer()
    
    def build_cpu(self):
        pass
    
    def build_memory(self):
        pass
    
    def build_storage(self):
        pass
    
    def build_gpu(self):
        pass
    
    def get_computer(self):
        return self.computer


class GamingComputerBuilder(ComputerBuilder):
    """遊戲電腦建造者"""
    def build_cpu(self):
        self.computer.cpu = "Intel i9"
        return self
    
    def build_memory(self):
        self.computer.memory = "32GB DDR4"
        return self
    
    def build_storage(self):
        self.computer.storage = "2TB NVMe SSD"
        return self
    
    def build_gpu(self):
        self.computer.gpu = "NVIDIA RTX 3080"
        return self


class OfficeComputerBuilder(ComputerBuilder):
    """辦公電腦建造者"""
    def build_cpu(self):
        self.computer.cpu = "Intel i5"
        return self
    
    def build_memory(self):
        self.computer.memory = "16GB DDR4"
        return self
    
    def build_storage(self):
        self.computer.storage = "512GB SSD"
        return self
    
    def build_gpu(self):
        # 辦公電腦不需要獨立顯卡
        return self


class ComputerDirector:
    """電腦建造指揮者"""
    def __init__(self, builder):
        self.builder = builder
    
    def build_complete_computer(self):
        return (self.builder
                .build_cpu()
                .build_memory()
                .build_storage()
                .build_gpu()
                .get_computer())
    
    def build_minimal_computer(self):
        return (self.builder
                .build_cpu()
                .build_memory()
                .build_storage()
                .get_computer())


# 測試建造者模式
print("\n建造者模式測試:")
# 創建遊戲電腦
gaming_builder = GamingComputerBuilder()
director = ComputerDirector(gaming_builder)
gaming_pc = director.build_complete_computer()
print(gaming_pc)

print()

# 創建辦公電腦
office_builder = OfficeComputerBuilder()
director = ComputerDirector(office_builder)
office_pc = director.build_minimal_computer()
print(office_pc)


# 1.4 原型模式 (Prototype)
print("\n"+"="*40)
print("1.4 原型模式 (Prototype)")
print("="*40)
print("使用原型實例指定創建對象的種類，通過複製這些原型創建新對象")

import copy

class Prototype:
    """原型基類"""
    def clone(self):
        """淺複製"""
        return copy.copy(self)
    
    def deep_clone(self):
        """深複製"""
        return copy.deepcopy(self)


class Document(Prototype):
    """文檔類"""
    def __init__(self, title, content, authors):
        self.title = title
        self.content = content
        self.authors = authors  # 列表，引用類型
    
    def __str__(self):
        return f"文檔: {self.title}\n內容: {self.content}\n作者: {', '.join(self.authors)}"


# 測試原型模式
print("\n原型模式測試:")
original_doc = Document("設計模式", "介紹常見的設計模式...", ["張三", "李四"])
print("原始文檔:")
print(original_doc)

# 淺複製
shallow_copy = original_doc.clone()
shallow_copy.title = "設計模式副本"
shallow_copy.authors.append("王五")  # 這會影響原始文檔，因為authors是引用類型

print("\n淺複製後:")
print("原始文檔:")
print(original_doc)
print("淺複製文檔:")
print(shallow_copy)

# 深複製
deep_copy = original_doc.deep_clone()
deep_copy.title = "設計模式深複製"
deep_copy.authors.append("趙六")  # 不會影響原始文檔，因為是深複製

print("\n深複製後:")
print("原始文檔:")
print(original_doc)
print("深複製文檔:")
print(deep_copy)


# 2. 結構型模式
print("\n"+"="*50)
print("2. 結構型模式 (Structural Patterns)")
print("="*50)

# 2.1 適配器模式 (Adapter)
print("\n"+"="*40)
print("2.1 適配器模式 (Adapter)")
print("="*40)
print("將一個類的接口轉換成客戶希望的另一個接口")

# 目標接口
class Target:
    """目標接口"""
    def request(self):
        return "Target: 標準請求"

# 被適配的類
class Adaptee:
    """需要被適配的類"""
    def specific_request(self):
        return "Adaptee: 特殊請求"

# 對象適配器
class Adapter(Target):
    """對象適配器"""
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def request(self):
        return f"Adapter: (已翻譯) {self.adaptee.specific_request()}"


# 測試適配器模式
print("\n適配器模式測試:")
# 客戶端代碼
def client_code(target):
    return target.request()

# 標準目標
print(client_code(Target()))

# 無法直接使用Adaptee
adaptee = Adaptee()
print(f"Adaptee: {adaptee.specific_request()}")

# 使用適配器
adapter = Adapter(adaptee)
print(client_code(adapter))


# 2.2 橋接模式 (Bridge)
print("\n"+"="*40)
print("2.2 橋接模式 (Bridge)")
print("="*40)
print("將抽象部分與實現部分分離，使它們可以獨立變化")

# 實現部分
class DrawingAPI:
    """繪圖API接口"""
    def draw_circle(self, x, y, radius):
        pass

class SVGDrawingAPI(DrawingAPI):
    """SVG繪圖API"""
    def draw_circle(self, x, y, radius):
        return f"SVG繪製圓形: 中心({x},{y}), 半徑{radius}"

class CanvasDrawingAPI(DrawingAPI):
    """Canvas繪圖API"""
    def draw_circle(self, x, y, radius):
        return f"Canvas繪製圓形: 中心({x},{y}), 半徑{radius}"

# 抽象部分
class Shape:
    """形狀抽象類"""
    def __init__(self, drawing_api):
        self.drawing_api = drawing_api
    
    def draw(self):
        pass

class Circle(Shape):
    """圓形"""
    def __init__(self, x, y, radius, drawing_api):
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.radius = radius
    
    def draw(self):
        return self.drawing_api.draw_circle(self.x, self.y, self.radius)

class Square(Shape):
    """正方形"""
    def __init__(self, x, y, side, drawing_api):
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.side = side
    
    def draw(self):
        # 簡化實現，使用圓形API繪製
        return f"正方形: {self.drawing_api.draw_circle(self.x, self.y, self.side/2)}"


# 測試橋接模式
print("\n橋接模式測試:")
svg_api = SVGDrawingAPI()
canvas_api = CanvasDrawingAPI()

# 創建形狀
circle1 = Circle(10, 10, 5, svg_api)
circle2 = Circle(20, 20, 10, canvas_api)
square = Square(15, 15, 8, svg_api)

# 繪製
print(circle1.draw())
print(circle2.draw())
print(square.draw())


# 2.3 組合模式 (Composite)
print("\n"+"="*40)
print("2.3 組合模式 (Composite)")
print("="*40)
print("將對象組合成樹形結構表示「部分-整體」的層次關係")

# 組件接口
class Component:
    """組件接口"""
    def __init__(self, name):
        self.name = name
    
    def add(self, component):
        pass
    
    def remove(self, component):
        pass
    
    def get_child(self, index):
        pass
    
    def operation(self):
        pass

# 葉子節點
class Leaf(Component):
    """葉子節點 - 沒有子節點"""
    def add(self, component):
        print(f"無法向葉子{self.name}添加組件")
    
    def remove(self, component):
        print(f"無法從葉子{self.name}移除組件")
    
    def get_child(self, index):
        print(f"無法從葉子{self.name}獲取子組件")
    
    def operation(self):
        return f"葉子{self.name}的操作"

# 複合節點
class Composite(Component):
    """複合節點 - 可以有子節點"""
    def __init__(self, name):
        super().__init__(name)
        self.children = []
    
    def add(self, component):
        self.children.append(component)
    
    def remove(self, component):
        self.children.remove(component)
    
    def get_child(self, index):
        return self.children[index]
    
    def operation(self):
        results = [f"組合{self.name}的操作"]
        for child in self.children:
            results.append(child.operation())
        return "\n".join(results)


# 測試組合模式
print("\n組合模式測試:")
# 創建組合結構
root = Composite("根節點")
branch1 = Composite("分支1")
branch2 = Composite("分支2")
leaf1 = Leaf("葉子1")
leaf2 = Leaf("葉子2")
leaf3 = Leaf("葉子3")

# 構建樹結構
root.add(branch1)
root.add(branch2)
branch1.add(leaf1)
branch1.add(leaf2)
branch2.add(leaf3)

# 操作整個結構
print(root.operation())


# 2.4 裝飾器模式 (Decorator)
print("\n"+"="*40)
print("2.4 裝飾器模式 (Decorator)")
print("="*40)
print("動態地給對象添加額外的職責")

# 組件接口
class TextComponent:
    """文本組件接口"""
    def get_content(self):
        pass

# 具體組件
class PlainText(TextComponent):
    """純文本"""
    def __init__(self, text):
        self.text = text
    
    def get_content(self):
        return self.text

# 裝飾器基類
class TextDecorator(TextComponent):
    """文本裝飾器基類"""
    def __init__(self, component):
        self.component = component
    
    def get_content(self):
        return self.component.get_content()

# 具體裝飾器
class BoldDecorator(TextDecorator):
    """粗體裝飾器"""
    def get_content(self):
        return f"<b>{self.component.get_content()}</b>"

class ItalicDecorator(TextDecorator):
    """斜體裝飾器"""
    def get_content(self):
        return f"<i>{self.component.get_content()}</i>"

class UnderlineDecorator(TextDecorator):
    """下劃線裝飾器"""
    def get_content(self):
        return f"<u>{self.component.get_content()}</u>"


# 測試裝飾器模式
print("\n裝飾器模式測試:")
# 創建純文本
text = PlainText("Hello, World!")
print(f"原始文本: {text.get_content()}")

# 應用裝飾器
bold_text = BoldDecorator(text)
print(f"粗體文本: {bold_text.get_content()}")

italic_text = ItalicDecorator(text)
print(f"斜體文本: {italic_text.get_content()}")

# 組合多個裝飾器
bold_italic_text = BoldDecorator(ItalicDecorator(text))
print(f"粗體+斜體: {bold_italic_text.get_content()}")

# 更複雜的嵌套
complex_text = UnderlineDecorator(BoldDecorator(ItalicDecorator(text)))
print(f"下劃線+粗體+斜體: {complex_text.get_content()}")


# 2.5 外觀模式 (Facade)
print("\n"+"="*40)
print("2.5 外觀模式 (Facade)")
print("="*40)
print("為子系統中的一組接口提供一個統一的高層接口")

# 子系統類
class CPU:
    """CPU子系統"""
    def freeze(self):
        return "CPU: 凍結..."
    
    def jump(self, address):
        return f"CPU: 跳轉到地址 {address}"
    
    def execute(self):
        return "CPU: 執行指令..."

class Memory:
    """內存子系統"""
    def load(self, address, data):
        return f"內存: 加載數據 '{data}' 到地址 {address}"

class HardDrive:
    """硬盤子系統"""
    def read(self, sector, size):
        return f"硬盤: 從扇區 {sector} 讀取 {size} 字節"

# 外觀類
class ComputerFacade:
    """電腦外觀類"""
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
    
    def start(self):
        """啟動電腦的簡化過程"""
        steps = []
        steps.append(self.cpu.freeze())
        steps.append(self.hard_drive.read(0, 1024))
        steps.append(self.memory.load(0, "引導數據"))
        steps.append(self.cpu.jump(0))
        steps.append(self.cpu.execute())
        return "\n".join(steps)


# 測試外觀模式
print("\n外觀模式測試:")
computer = ComputerFacade()
print("啟動電腦:")
print(computer.start())


# 3. 行為型模式
print("\n"+"="*50)
print("3. 行為型模式 (Behavioral Patterns)")
print("="*50)

# 3.1 觀察者模式 (Observer)
print("\n"+"="*40)
print("3.1 觀察者模式 (Observer)")
print("="*40)
print("定義對象間的一種一對多依賴關係，當一個對象狀態改變時，所有依賴它的對象都會得到通知並更新")

# 主題接口
class Subject:
    """主題接口"""
    def register_observer(self, observer):
        pass
    
    def remove_observer(self, observer):
        pass
    
    def notify_observers(self):
        pass

# 觀察者接口
class Observer:
    """觀察者接口"""
    def update(self, subject, arg=None):
        pass

# 具體主題
class WeatherData(Subject):
    """天氣數據主題"""
    def __init__(self):
        self.observers = []
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
    
    def register_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)
    
    def set_measurements(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.measurements_changed()
    
    def measurements_changed(self):
        self.notify_observers()

# 具體觀察者
class CurrentConditionsDisplay(Observer):
    """當前狀況顯示器"""
    def __init__(self, weather_data):
        self.temperature = 0
        self.humidity = 0
        self.weather_data = weather_data
        # 註冊為觀察者
        weather_data.register_observer(self)
    
    def update(self, subject, arg=None):
        if isinstance(subject, WeatherData):
            self.temperature = subject.temperature
            self.humidity = subject.humidity
            self.display()
    
    def display(self):
        return f"當前狀況: 溫度 {self.temperature}°C, 濕度 {self.humidity}%"

class StatisticsDisplay(Observer):
    """統計信息顯示器"""
    def __init__(self, weather_data):
        self.max_temp = -float('inf')
        self.min_temp = float('inf')
        self.temp_sum = 0
        self.num_readings = 0
        self.weather_data = weather_data
        # 註冊為觀察者
        weather_data.register_observer(self)
    
    def update(self, subject, arg=None):
        if isinstance(subject, WeatherData):
            temp = subject.temperature
            self.temp_sum += temp
            self.num_readings += 1
            
            if temp > self.max_temp:
                self.max_temp = temp
            
            if temp < self.min_temp:
                self.min_temp = temp
            
            self.display()
    
    def display(self):
        avg_temp = self.temp_sum / self.num_readings if self.num_readings > 0 else 0
        return f"溫度統計: 平均 {avg_temp:.1f}°C, 最高 {self.max_temp}°C, 最低 {self.min_temp}°C"


# 測試觀察者模式
print("\n觀察者模式測試:")
# 創建主題
weather_data = WeatherData()

# 創建觀察者
current_display = CurrentConditionsDisplay(weather_data)
statistics_display = StatisticsDisplay(weather_data)

# 更新數據
print("更新天氣數據: 25°C, 60%, 1013hPa")
weather_data.set_measurements(25, 60, 1013)
print(current_display.display())
print(statistics_display.display())

print("\n更新天氣數據: 28°C, 70%, 1012hPa")
weather_data.set_measurements(28, 70, 1012)
print(current_display.display())
print(statistics_display.display())


# 3.2 策略模式 (Strategy)
print("\n"+"="*40)
print("3.2 策略模式 (Strategy)")
print("="*40)
print("定義一系列算法，將每個算法封裝起來，並使它們可以互換")

# 策略接口
class PaymentStrategy:
    """支付策略接口"""
    def pay(self, amount):
        pass

# 具體策略
class CreditCardPayment(PaymentStrategy):
    """信用卡支付策略"""
    def __init__(self, card_number, name, expiry, cvv):
        self.card_number = card_number
        self.name = name
        self.expiry = expiry
        self.cvv = cvv
    
    def pay(self, amount):
        return f"使用信用卡支付 ${amount}: {self.name}, 卡號 {self.card_number}"

class PayPalPayment(PaymentStrategy):
    """PayPal支付策略"""
    def __init__(self, email, password):
        self.email = email
        self.password = password  # 實際應用中不應明文儲存密碼
    
    def pay(self, amount):
        return f"使用PayPal支付 ${amount}: {self.email}"

class BitcoinPayment(PaymentStrategy):
    """比特幣支付策略"""
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def pay(self, amount):
        return f"使用比特幣支付 ${amount}: 錢包地址 {self.wallet_address}"

# 上下文
class ShoppingCart:
    """購物車 (上下文)"""
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item, price):
        self.items.append((item, price))
    
    def total(self):
        return sum(price for _, price in self.items)
    
    def set_payment_strategy(self, payment_strategy):
        self.payment_strategy = payment_strategy
    
    def checkout(self):
        total = self.total()
        if self.payment_strategy is None:
            return "請設置支付方式"
        
        result = self.payment_strategy.pay(total)
        self.items = []  # 清空購物車
        return result


# 測試策略模式
print("\n策略模式測試:")
# 創建購物車
cart = ShoppingCart()
cart.add_item("手機", 999)
cart.add_item("耳機", 199)
print(f"購物車總金額: ${cart.total()}")

# 使用不同的支付策略
cart.set_payment_strategy(CreditCardPayment("1234-5678-9012-3456", "張三", "12/24", "123"))
print(cart.checkout())

# 使用另一種支付策略
cart = ShoppingCart()
cart.add_item("筆記本電腦", 1299)
cart.set_payment_strategy(PayPalPayment("zhang@example.com", "password"))
print(cart.checkout())


# 3.3 命令模式 (Command)
print("\n"+"="*40)
print("3.3 命令模式 (Command)")
print("="*40)
print("將請求封裝成對象，使請求發送者和接收者解耦")

# 命令接口
class Command:
    """命令接口"""
    def execute(self):
        pass
    
    def undo(self):
        pass

# 接收者類
class Light:
    """燈 (接收者)"""
    def __init__(self, location):
        self.location = location
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        return f"{self.location}的燈已打開"
    
    def turn_off(self):
        self.is_on = False
        return f"{self.location}的燈已關閉"

class StereoSystem:
    """音響系統 (接收者)"""
    def __init__(self, location):
        self.location = location
        self.is_on = False
        self.volume = 0
        self.cd_inserted = False
    
    def on(self):
        self.is_on = True
        return f"{self.location}的音響已打開"
    
    def off(self):
        self.is_on = False
        return f"{self.location}的音響已關閉"
    
    def set_volume(self, volume):
        self.volume = volume
        return f"{self.location}的音響音量設置為 {volume}"
    
    def insert_cd(self):
        self.cd_inserted = True
        return f"{self.location}的音響已插入CD"
    
    def eject_cd(self):
        self.cd_inserted = False
        return f"{self.location}的音響已彈出CD"

# 具體命令
class LightOnCommand(Command):
    """打開燈命令"""
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        return self.light.turn_on()
    
    def undo(self):
        return self.light.turn_off()

class LightOffCommand(Command):
    """關閉燈命令"""
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        return self.light.turn_off()
    
    def undo(self):
        return self.light.turn_on()

class StereoOnWithCDCommand(Command):
    """打開音響並插入CD命令"""
    def __init__(self, stereo):
        self.stereo = stereo
    
    def execute(self):
        results = []
        results.append(self.stereo.on())
        results.append(self.stereo.insert_cd())
        results.append(self.stereo.set_volume(10))
        return "\n".join(results)
    
    def undo(self):
        results = []
        results.append(self.stereo.off())
        return "\n".join(results)

# 調用者
class RemoteControl:
    """遙控器 (調用者)"""
    def __init__(self):
        self.commands = {}
        self.history = []
    
    def set_command(self, button, command):
        self.commands[button] = command
    
    def press_button(self, button):
        if button in self.commands:
            result = self.commands[button].execute()
            self.history.append(self.commands[button])
            return result
        return f"按鈕 {button} 未設置命令"
    
    def undo_last_command(self):
        if self.history:
            command = self.history.pop()
            return command.undo()
        return "沒有可撤銷的命令"


# 測試命令模式
print("\n命令模式測試:")
# 創建接收者
living_room_light = Light("客廳")
bedroom_light = Light("臥室")
stereo = StereoSystem("客廳")

# 創建命令
living_room_light_on = LightOnCommand(living_room_light)
living_room_light_off = LightOffCommand(living_room_light)
bedroom_light_on = LightOnCommand(bedroom_light)
bedroom_light_off = LightOffCommand(bedroom_light)
stereo_on_with_cd = StereoOnWithCDCommand(stereo)

# 創建遙控器
remote = RemoteControl()
remote.set_command("客廳燈開", living_room_light_on)
remote.set_command("客廳燈關", living_room_light_off)
remote.set_command("臥室燈開", bedroom_light_on)
remote.set_command("臥室燈關", bedroom_light_off)
remote.set_command("音響開", stereo_on_with_cd)

# 使用遙控器
print(remote.press_button("客廳燈開"))
print(remote.press_button("音響開"))
print(remote.press_button("臥室燈開"))
print(remote.press_button("臥室燈關"))
print(remote.undo_last_command())  # 撤銷關閉臥室燈


# 3.4 模板方法模式 (Template Method)
print("\n"+"="*40)
print("3.4 模板方法模式 (Template Method)")
print("="*40)
print("定義算法的骨架，並允許子類為一個或多個步驟提供實現")

# 抽象類
class DataProcessor:
    """數據處理器抽象類"""
    
    def process(self, data):
        """模板方法 - 定義了算法骨架"""
        result = self.read_data(data)
        result = self.parse_data(result)
        result = self.process_data(result)
        result = self.analyze_data(result)
        self.send_data(result)
        
        # 鉤子方法
        if self.should_log():
            print(f"數據處理日誌: {result}")
        
        return result
    
    # 抽象方法 - 子類必須實現
    def read_data(self, data):
        raise NotImplementedError
    
    def parse_data(self, data):
        raise NotImplementedError
    
    def process_data(self, data):
        raise NotImplementedError
    
    # 子類可選擇重寫的方法
    def analyze_data(self, data):
        return data
    
    def send_data(self, data):
        print(f"發送數據: {data}")
    
    # 鉤子方法 - 子類可選擇重寫
    def should_log(self):
        return True

# 具體子類
class CSVDataProcessor(DataProcessor):
    """CSV數據處理器"""
    
    def read_data(self, data):
        print("讀取CSV數據")
        return data
    
    def parse_data(self, data):
        print("解析CSV數據")
        return data.split(",")
    
    def process_data(self, data):
        print("處理CSV數據")
        return [int(x) for x in data if x.isdigit()]
    
    def analyze_data(self, data):
        print("分析CSV數據")
        if data:
            return {"count": len(data), "sum": sum(data), "avg": sum(data) / len(data)}
        return {"count": 0, "sum": 0, "avg": 0}

class JSONDataProcessor(DataProcessor):
    """JSON數據處理器"""
    import json  # 放在實際程式中會放在文件頂部
    
    def read_data(self, data):
        print("讀取JSON數據")
        return data
    
    def parse_data(self, data):
        print("解析JSON數據")
        # 模擬解析，實際會使用json.loads
        return {"values": [1, 2, 3, 4, 5]}
    
    def process_data(self, data):
        print("處理JSON數據")
        return data["values"]
    
    def should_log(self):
        # 覆蓋鉤子方法
        return False


# 測試模板方法模式
print("\n模板方法模式測試:")
# 使用CSV處理器
csv_processor = CSVDataProcessor()
print("使用CSV處理器:")
result = csv_processor.process("1,2,3,4,5")
print(f"CSV處理結果: {result}")

print("\n使用JSON處理器:")
json_processor = JSONDataProcessor()
result = json_processor.process('{"values":[1,2,3,4,5]}')
print(f"JSON處理結果: {result}")


# 3.5 迭代器模式 (Iterator)
print("\n"+"="*40)
print("3.5 迭代器模式 (Iterator)")
print("="*40)
print("提供一種方法依次訪問聚合對象中的各個元素，而不暴露對象的內部表示")

class Iterator:
    """迭代器接口"""
    def has_next(self):
        pass
    
    def next(self):
        pass

class Container:
    """容器接口"""
    def get_iterator(self):
        pass

class BookCollection(Container):
    """書籍集合"""
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def get_iterator(self):
        return BookIterator(self.books)

class BookIterator(Iterator):
    """書籍迭代器"""
    def __init__(self, books):
        self.books = books
        self.position = 0
    
    def has_next(self):
        return self.position < len(self.books)
    
    def next(self):
        if self.has_next():
            book = self.books[self.position]
            self.position += 1
            return book
        
        raise StopIteration("沒有更多書籍")


# 測試迭代器模式
print("\n迭代器模式測試:")
# 創建書籍集合
collection = BookCollection()
collection.add_book({"title": "Python設計模式", "author": "張三"})
collection.add_book({"title": "深入理解Python", "author": "李四"})
collection.add_book({"title": "Python進階編程", "author": "王五"})

# 使用迭代器
iterator = collection.get_iterator()
print("書籍列表:")
while iterator.has_next():
    book = iterator.next()
    print(f"- {book['title']} by {book['author']}")

# 使用Python內置迭代器
print("\nPython內置迭代器:")
class PythonBookCollection:
    """支持Python迭代協議的書籍集合"""
    def __init__(self):
        self.books = []
    
    def add_book(self, book):
        self.books.append(book)
    
    def __iter__(self):
        self.position = 0
        return self
    
    def __next__(self):
        if self.position < len(self.books):
            book = self.books[self.position]
            self.position += 1
            return book
        
        raise StopIteration()

# 創建集合並添加書籍
python_collection = PythonBookCollection()
python_collection.add_book({"title": "Python設計模式", "author": "張三"})
python_collection.add_book({"title": "深入理解Python", "author": "李四"})
python_collection.add_book({"title": "Python進階編程", "author": "王五"})

# 使用for循環迭代
print("使用for循環迭代:")
for book in python_collection:
    print(f"- {book['title']} by {book['author']}")


# 4. Python特有的設計模式
print("\n"+"="*50)
print("4. Python特有的設計模式")
print("="*50)

print("\n簡述:")
print("Python作為一種動態類型語言，有一些特有的設計模式和實現方式:")
print("1. 猴子補丁 (Monkey Patching): 運行時修改類或模塊")
print("2. 元類 (Metaclasses): 控制類的創建過程")
print("3. 描述符 (Descriptors): 控制屬性訪問")
print("4. 上下文管理器 (Context Managers): 控制進入和退出上下文的代碼")

print("\n這些Python特有的模式在前面的課程中已有詳細介紹，此處不再重複。")


# 總結
print("\n"+"="*50)
print("設計模式總結")
print("="*50)

print("設計模式優點:")
print("1. 提供了經過驗證的解決方案")
print("2. 使代碼更加模塊化、可重用和可維護")
print("3. 幫助團隊使用共同的語言交流")

print("\n設計模式使用建議:")
print("1. 不要過度使用設計模式")
print("2. 應先理解問題，再選擇適當的模式")
print("3. 根據Python的特性選擇合適的實現方式")
print("4. 代碼簡潔性和可讀性優先")

