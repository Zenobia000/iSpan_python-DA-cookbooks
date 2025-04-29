# %% [markdown]
# # 從函數到類別：轉變程式設計思維
# 
# 本節將探討函數式編程與物件導向編程的差異，並介紹如何從函數式設計轉變為物件導向設計思維。

# %% [markdown]
# ## 1. 兩種程式設計範式

# %%
paradigms = {
    "函數式編程 (Functional Programming)": [
        "專注於函數運算和轉換",
        "避免狀態變化和可變數據",
        "函數是一等公民，可作為參數傳遞",
        "強調表達式而非語句",
        "避免副作用，相同輸入始終產生相同輸出"
    ],
    "物件導向編程 (Object-Oriented Programming)": [
        "專注於創建對象模型",
        "數據和行為封裝為類別和物件",
        "強調狀態管理和對象間交互",
        "通過繼承和多態實現代碼重用",
        "將問題領域映射到對象世界"
    ]
}

for paradigm, features in paradigms.items():
    print(f"{paradigm}的特點:")
    for i, feature in enumerate(features, 1):
        print(f"  {i}. {feature}")
    print()

# %% [markdown]
# ## 2. 函數式程式設計範例

# %%
# 使用函數式風格處理學生成績數據的範例
student_data = [
    {"name": "Alice", "id": "A001", "scores": [85, 90, 78]},
    {"name": "Bob", "id": "A002", "scores": [92, 88, 95]},
    {"name": "Charlie", "id": "A003", "scores": [76, 70, 82]},
    {"name": "David", "id": "A004", "scores": [88, 91, 86]},
]

# 計算平均分數
def calculate_average(scores):
    return sum(scores) / len(scores) if scores else 0

# 計算學生成績
def process_student_score(student):
    avg_score = calculate_average(student["scores"])
    return {
        "id": student["id"],
        "name": student["name"],
        "average": avg_score,
        "grade": get_grade(avg_score)
    }

# 根據分數確定等級
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# 獲取所有學生的成績報告
def get_all_reports(students):
    return [process_student_score(student) for student in students]

# 找出表現最佳的學生
def find_top_student(reports):
    return max(reports, key=lambda report: report["average"])

# 篩選通過考試的學生 (平均分 >= 60)
def filter_passing_students(reports):
    return [report for report in reports if report["average"] >= 60]

# 執行分析
student_reports = get_all_reports(student_data)
top_student = find_top_student(student_reports)
passing_students = filter_passing_students(student_reports)

print("函數式風格處理學生數據:")
print(f"學生報告: {student_reports}")
print(f"最佳學生: {top_student['name']} (平均: {top_student['average']:.1f})")
print(f"通過考試的學生數量: {len(passing_students)}")

# %% [markdown]
# ## 3. 物件導向設計範例

# %%
# 使用物件導向風格處理相同的學生成績數據
class Student:
    def __init__(self, student_id, name, scores=None):
        self.student_id = student_id
        self.name = name
        self.scores = scores or []
        self._average = None  # 緩存計算結果
        self._grade = None
    
    def add_score(self, score):
        """添加一個新的分數"""
        self.scores.append(score)
        # 清除緩存，因為數據已變更
        self._average = None
        self._grade = None
    
    @property
    def average(self):
        """計算並返回平均分數"""
        if self._average is None:  # 如果緩存無效
            self._average = sum(self.scores) / len(self.scores) if self.scores else 0
        return self._average
    
    @property
    def grade(self):
        """根據平均分數確定等級"""
        if self._grade is None:  # 如果緩存無效
            avg = self.average  # 使用 average 屬性獲取平均分
            if avg >= 90:
                self._grade = "A"
            elif avg >= 80:
                self._grade = "B"
            elif avg >= 70:
                self._grade = "C"
            elif avg >= 60:
                self._grade = "D"
            else:
                self._grade = "F"
        return self._grade
    
    def is_passing(self):
        """檢查學生是否通過考試"""
        return self.average >= 60
    
    def get_report(self):
        """生成學生成績報告"""
        return {
            "id": self.student_id,
            "name": self.name,
            "average": self.average,
            "grade": self.grade
        }
    
    def __str__(self):
        """返回學生的字符串表示"""
        return f"{self.name} ({self.student_id}): {self.average:.1f} - {self.grade}"


class StudentRegistry:
    def __init__(self):
        self.students = {}  # 使用字典儲存學生對象
    
    def add_student(self, student):
        """添加學生到註冊表"""
        self.students[student.student_id] = student
    
    def get_student(self, student_id):
        """根據 ID 獲取學生"""
        return self.students.get(student_id)
    
    def get_all_students(self):
        """獲取所有學生列表"""
        return list(self.students.values())
    
    def get_all_reports(self):
        """獲取所有學生的成績報告"""
        return [student.get_report() for student in self.students.values()]
    
    def find_top_student(self):
        """找出平均分最高的學生"""
        if not self.students:
            return None
        return max(self.students.values(), key=lambda student: student.average)
    
    def get_passing_students(self):
        """獲取所有通過考試的學生"""
        return [student for student in self.students.values() if student.is_passing()]


# 創建學生註冊表並添加學生
registry = StudentRegistry()

# 從原始數據創建學生對象
for data in student_data:
    student = Student(data["id"], data["name"], data["scores"])
    registry.add_student(student)

# 使用物件導向方法獲取信息
oop_top_student = registry.find_top_student()
oop_passing_students = registry.get_passing_students()

print("\n物件導向風格處理學生數據:")
print(f"學生列表:")
for student in registry.get_all_students():
    print(f"  {student}")
print(f"最佳學生: {oop_top_student}")
print(f"通過考試的學生數量: {len(oop_passing_students)}")

# 演示物件狀態變化
print("\n演示狀態變化:")
bob = registry.get_student("A002")
print(f"Bob 原始成績: {bob}")
bob.add_score(75)  # 添加一個新的分數
print(f"新增分數後: {bob}")

# %% [markdown]
# ## 4. 兩種範式的比較

# %%
import pandas as pd
from IPython.display import display

# 創建比較表格
comparison_data = {
    "特性": [
        "數據與行為的關係",
        "狀態管理",
        "代碼重用機制",
        "擴展性",
        "可測試性",
        "適用場景",
        "代碼結構",
        "學習曲線"
    ],
    "函數式編程": [
        "分離 (數據和函數獨立存在)",
        "避免狀態，偏好不可變數據",
        "高階函數、閉包、函數組合",
        "通過組合現有函數",
        "容易測試 (無副作用)",
        "數據轉換、並行計算、批處理",
        "扁平，基於函數調用",
        "需理解函數式概念 (如純函數、柯里化)"
    ],
    "物件導向編程": [
        "合併 (數據和方法封裝在對象中)",
        "管理對象內部狀態",
        "繼承、接口、組合",
        "通過添加新類或擴展現有類",
        "需要模擬對象狀態",
        "模擬現實世界、GUI、遊戲開發",
        "層次化，基於類的關係",
        "需理解物件概念 (類、繼承、多態)"
    ]
}

comparison_df = pd.DataFrame(comparison_data)
print("函數式編程 vs 物件導向編程 比較:")
display(comparison_df)

# %% [markdown]
# ## 5. 何時使用哪種範式？

# %%
scenarios = {
    "適合函數式風格的場景": [
        "數據轉換和處理管道 (ETL 流程)",
        "複雜的數學計算",
        "並行計算和大數據處理",
        "事件處理系統",
        "無狀態的 Web API"
    ],
    "適合物件導向風格的場景": [
        "需要建模現實世界實體的應用 (如銀行系統、遊戲)",
        "具有複雜狀態的應用",
        "圖形用戶界面 (GUI)",
        "需要繼承和多型的系統",
        "複雜業務邏輯的企業應用"
    ],
    "混合使用的場景": [
        "Web 框架 (如 Django: OOP 結構 + 函數式視圖)",
        "數據科學應用 (OOP 用於架構，函數式用於數據處理)",
        "圖形處理 (對象表示圖形元素，函數處理變換)",
        "遊戲引擎 (OOP 用於遊戲對象，函數式用於遊戲邏輯)",
        "現代前端框架 (如 React: 組件是對象，渲染邏輯是函數式)"
    ]
}

for scenario_type, examples in scenarios.items():
    print(f"{scenario_type}:")
    for example in examples:
        print(f"  - {example}")
    print()

# %% [markdown]
# ## 6. 從函數式到物件導向的轉變

# %%
# 展示同一個問題的思維轉變過程

# 步驟 1: 純函數式方法處理形狀
print("步驟 1: 純函數式方法 - 處理不同形狀的面積計算")

def square_area(side):
    return side ** 2

def rectangle_area(width, height):
    return width * height

def circle_area(radius):
    import math
    return math.pi * radius ** 2

def calculate_total_area(shapes):
    total = 0
    for shape in shapes:
        shape_type = shape["type"]
        if shape_type == "square":
            total += square_area(shape["side"])
        elif shape_type == "rectangle":
            total += rectangle_area(shape["width"], shape["height"])
        elif shape_type == "circle":
            total += circle_area(shape["radius"])
    return total

# 使用函數式方法
shapes_data = [
    {"type": "square", "side": 4},
    {"type": "rectangle", "width": 3, "height": 5},
    {"type": "circle", "radius": 2}
]

total_area = calculate_total_area(shapes_data)
print(f"計算面積 (函數式): {total_area:.2f}")

# %%
# 步驟 2: 過渡階段 - 使用類作為組織工具
print("\n步驟 2: 過渡階段 - 使用類作為組織工具")

class ShapeCalculator:
    @staticmethod
    def square_area(side):
        return side ** 2
    
    @staticmethod
    def rectangle_area(width, height):
        return width * height
    
    @staticmethod
    def circle_area(radius):
        import math
        return math.pi * radius ** 2
    
    @classmethod
    def calculate_total_area(cls, shapes):
        total = 0
        for shape in shapes:
            shape_type = shape["type"]
            if shape_type == "square":
                total += cls.square_area(shape["side"])
            elif shape_type == "rectangle":
                total += cls.rectangle_area(shape["width"], shape["height"])
            elif shape_type == "circle":
                total += cls.circle_area(shape["radius"])
        return total

# 使用組織成類的靜態方法
total_area = ShapeCalculator.calculate_total_area(shapes_data)
print(f"計算面積 (靜態方法): {total_area:.2f}")

# %%
# 步驟 3: 完整的物件導向設計
print("\n步驟 3: 完整的物件導向設計")

import math

class Shape:
    """形狀基類"""
    def area(self):
        """計算面積的抽象方法"""
        raise NotImplementedError("子類必須實現此方法")
    
    def __str__(self):
        return f"{self.__class__.__name__} (面積: {self.area():.2f})"


class Square(Shape):
    """正方形類"""
    def __init__(self, side):
        self.side = side
        
    def area(self):
        return self.side ** 2


class Rectangle(Shape):
    """矩形類"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def area(self):
        return self.width * self.height


class Circle(Shape):
    """圓形類"""
    def __init__(self, radius):
        self.radius = radius
        
    def area(self):
        return math.pi * self.radius ** 2


class ShapeFactory:
    """形狀工廠 - 創建形狀物件"""
    @staticmethod
    def create_shape(shape_data):
        shape_type = shape_data["type"]
        if shape_type == "square":
            return Square(shape_data["side"])
        elif shape_type == "rectangle":
            return Rectangle(shape_data["width"], shape_data["height"])
        elif shape_type == "circle":
            return Circle(shape_data["radius"])
        else:
            raise ValueError(f"未知的形狀類型: {shape_type}")


# 使用完整的物件導向設計
shapes = [ShapeFactory.create_shape(data) for data in shapes_data]

# 顯示每個形狀
for shape in shapes:
    print(f"  {shape}")

# 計算總面積
total_area = sum(shape.area() for shape in shapes)
print(f"計算總面積 (OOP): {total_area:.2f}")

# 展示添加新形狀的擴展性
class Triangle(Shape):
    """三角形類 - 展示擴展性"""
    def __init__(self, base, height):
        self.base = base
        self.height = height
        
    def area(self):
        return 0.5 * self.base * self.height

# 添加新形狀並重新計算
shapes.append(Triangle(4, 3))
print(f"\n添加三角形後:")
for shape in shapes:
    print(f"  {shape}")

total_area = sum(shape.area() for shape in shapes)
print(f"新的總面積: {total_area:.2f}")

# %% [markdown]
# ## 7. 實際開發中的混合使用

# %%
# 展示在實際開發中如何混合使用兩種範式
hybrid_code = """
# 數據處理系統中的混合使用示例

# 1. 使用類來建模系統元件和狀態管理
class DataProcessor:
    def __init__(self, data_source):
        self.data_source = data_source
        self.processed_data = None
        self.processing_steps = []
        
    def add_processing_step(self, step_function):
        # 函數式: 使用高階函數作為處理步驟
        self.processing_steps.append(step_function)
        
    def process(self):
        # 獲取原始數據
        data = self.data_source.get_data()
        
        # 函數式: 使用函數管道處理數據
        for step in self.processing_steps:
            data = step(data)
            
        self.processed_data = data
        return data
        
    def save(self, destination):
        # OOP: 通過方法和狀態管理保存結果
        if self.processed_data is None:
            raise ValueError("必須先處理數據")
        destination.save(self.processed_data)


# 2. 使用函數式方法進行數據轉換
def filter_invalid_records(data):
    # 函數式: 純函數轉換數據
    return [record for record in data if is_valid(record)]

def normalize_values(data):
    # 函數式: 映射轉換
    min_val = min(record["value"] for record in data)
    max_val = max(record["value"] for record in data)
    range_val = max_val - min_val
    
    return [
        {**record, "normalized": (record["value"] - min_val) / range_val}
        for record in data
    ]

def calculate_statistics(data):
    # 函數式: 使用歸納計算統計信息
    total = sum(record["value"] for record in data)
    count = len(data)
    return {
        "data": data,
        "stats": {
            "count": count,
            "average": total / count if count else 0,
            "total": total
        }
    }


# 3. 使用示例
class DatabaseSource:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        
    def get_data(self):
        # 實際中這裡會查詢數據庫
        print(f"從 {self.connection_string} 獲取數據")
        return sample_data  # 示例數據


class FileDestination:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def save(self, data):
        # 實際中這裡會保存到文件
        print(f"保存 {len(data['data'])} 條記錄到 {self.file_path}")
        print(f"統計信息: {data['stats']}")


# 使用這個混合設計的系統
sample_data = [
    {"id": 1, "value": 10, "valid": True},
    {"id": 2, "value": 15, "valid": True},
    {"id": 3, "value": 0, "valid": False},
    {"id": 4, "value": 20, "valid": True}
]

def is_valid(record):
    return record.get("valid", False)

# 創建處理器並配置管道
processor = DataProcessor(DatabaseSource("mysql://example"))
processor.add_processing_step(filter_invalid_records)
processor.add_processing_step(normalize_values)
processor.add_processing_step(calculate_statistics)

# 執行處理並保存結果
result = processor.process()
processor.save(FileDestination("output.json"))
"""

print("混合使用函數式和物件導向範式的範例:")
print(hybrid_code)

# %% [markdown]
# ## 8. Python 中的函數式編程特性

# %%
functional_features = [
    "Lambda 表達式 - 創建匿名函數",
    "map(), filter(), reduce() - 高階函數",
    "列表/字典/集合推導式 - 簡潔的函數式數據轉換",
    "生成器表達式和生成器函數 - 惰性求值",
    "函數作為一等公民 - 可作為參數傳遞",
    "裝飾器 - 函數變換",
    "partial() - 函數部分應用"
]

print("Python 中的函數式編程特性:")
for i, feature in enumerate(functional_features, 1):
    print(f"{i}. {feature}")

# 展示一些函數式編程示例
examples = {
    "Lambda 表達式": "sorted(names, key=lambda x: len(x))  # 按名稱長度排序",
    
    "map/filter": """
    # map 示例
    numbers = [1, 2, 3, 4, 5]
    squares = list(map(lambda x: x**2, numbers))  # [1, 4, 9, 16, 25]
    
    # filter 示例
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))  # [2, 4]
    """,
    
    "推導式": """
    # 列表推導式
    squares = [x**2 for x in range(10)]
    
    # 字典推導式
    name_to_age = {name: age for name, age in [("Alice", 25), ("Bob", 30)]}
    
    # 集合推導式
    unique_letters = {char.lower() for char in "Hello World"}
    """,
    
    "生成器": """
    # 生成器函數
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    # 生成器表達式
    sum_of_squares = sum(x**2 for x in range(10))
    """,
    
    "裝飾器": """
    # 簡單裝飾器
    def log_function(func):
        def wrapper(*args, **kwargs):
            print(f"調用函數: {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    
    @log_function
    def add(a, b):
        return a + b
    """
}

for name, example in examples.items():
    print(f"\n{name} 示例:")
    print(example)

# %% [markdown]
# ## 9. 實作練習
# 
# 1. 重構練習：將以下函數式代碼重構為物件導向設計：
#    ```python
#    # 處理商品訂單的函數
#    def calculate_price(item, quantity):
#        return item["price"] * quantity
#    
#    def apply_discount(total, discount_percent):
#        return total * (1 - discount_percent / 100)
#    
#    def calculate_tax(amount, tax_rate):
#        return amount * tax_rate / 100
#    
#    def process_order(items, quantities, discount=0, tax_rate=5):
#        total = sum(calculate_price(item, qty) for item, qty in zip(items, quantities))
#        after_discount = apply_discount(total, discount)
#        final_price = after_discount + calculate_tax(after_discount, tax_rate)
#        return {
#            "subtotal": total,
#            "discount": total - after_discount,
#            "tax": calculate_tax(after_discount, tax_rate),
#            "total": final_price
#        }
#    ```
# 
# 2. 混合設計練習：設計一個簡單的數據分析系統，結合物件導向設計 (用於系統組件) 和函數式方法 (用於數據轉換)。 