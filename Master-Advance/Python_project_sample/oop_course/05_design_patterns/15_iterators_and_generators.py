# 15_iterators_and_generators.py
# This file is part of the OOP course

"""
迭代器與生成器 (Iterators and Generators)
===================================
本模組介紹Python中的迭代器與生成器概念及其應用。

主題:
1. 迭代器協議 (__iter__ 和 __next__)
2. 迭代器和可迭代對象
3. 生成器函數
4. 生成器表達式
5. yield from 表達式
6. 生成器的高級應用
"""

import itertools
import sys
import time


# 1. 迭代器協議
print("="*50)
print("迭代器協議")
print("="*50)

# 自定義迭代器
class CountDown:
    """倒數計數迭代器"""
    
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        """返回迭代器對象"""
        # 在這裡，迭代器就是self本身
        return self
    
    def __next__(self):
        """返回下一個值或引發 StopIteration"""
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1


# 使用自定義迭代器
print("使用CountDown迭代器:")
for num in CountDown(5):
    print(num, end=" ")
print()

# 手動使用迭代器
print("\n手動使用迭代器:")
counter = CountDown(3)
iterator = iter(counter)  # 調用__iter__()
print(next(iterator))  # 調用__next__()
print(next(iterator))
print(next(iterator))
try:
    print(next(iterator))
except StopIteration:
    print("迭代結束")


# 2. 可迭代但非迭代器的對象
print("\n"+"="*50)
print("可迭代但非迭代器的對象")
print("="*50)

class NumberSequence:
    """生成一個數字序列的可迭代對象"""
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __iter__(self):
        """返回一個新的迭代器"""
        # 這裡返回的是一個獨立的迭代器對象，不是self
        return NumberIterator(self.start, self.end)


class NumberIterator:
    """NumberSequence的迭代器"""
    
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        """迭代器的__iter__方法返回自身"""
        return self
    
    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        self.current += 1
        return self.current - 1


# 使用 NumberSequence
print("NumberSequence迭代:")
numbers = NumberSequence(1, 5)
for num in numbers:
    print(num, end=" ")
print()

# 多次迭代同一對象
print("\n多次迭代同一可迭代對象:")
numbers = NumberSequence(10, 15)
print("第一次迭代:", end=" ")
for num in numbers:
    print(num, end=" ")
print()

print("第二次迭代:", end=" ")
for num in numbers:
    print(num, end=" ")
print()


# 3. 生成器函數
print("\n"+"="*50)
print("生成器函數")
print("="*50)

def simple_generator():
    """一個簡單的生成器函數"""
    yield 1
    yield 2
    yield 3


# 使用簡單生成器
print("使用簡單生成器函數:")
gen = simple_generator()
print(f"生成器類型: {type(gen)}")
print(f"是迭代器? {hasattr(gen, '__next__')}")
print(f"是可迭代對象? {hasattr(gen, '__iter__')}")

for num in simple_generator():
    print(num, end=" ")
print()

# 帶參數的生成器函數
def count_up_to(max):
    """從0計數到max-1的生成器"""
    count = 0
    while count < max:
        yield count
        count += 1


print("\n帶參數的生成器函數:")
for num in count_up_to(5):
    print(num, end=" ")
print()

# 無限生成器
def infinite_sequence():
    """生成無限自然數序列的生成器"""
    num = 0
    while True:
        yield num
        num += 1


print("\n無限生成器 (只取前5個數):")
gen = infinite_sequence()
for _ in range(5):
    print(next(gen), end=" ")
print()


# 4. 生成器表達式
print("\n"+"="*50)
print("生成器表達式")
print("="*50)

# 列表推導式 vs 生成器表達式
print("列表推導式 vs 生成器表達式:")
# 列表推導式 - 立即計算所有值並存儲在列表中
list_comp = [x**2 for x in range(5)]
print(f"列表推導式 (立即計算): {list_comp}")

# 生成器表達式 - 惰性計算，按需生成值
gen_exp = (x**2 for x in range(5))
print(f"生成器表達式 (對象): {gen_exp}")
print("生成器表達式 (按需計算):", end=" ")
for num in gen_exp:
    print(num, end=" ")
print()

# 記憶體使用比較
print("\n記憶體使用比較:")

def memory_usage(obj):
    """估計對象的內存使用量"""
    return sys.getsizeof(obj)

# 大量數據
n = 1000000

# 使用列表推導式
start_time = time.time()
list_comp = [x for x in range(n)]  # 立即生成所有值
list_time = time.time() - start_time
list_memory = memory_usage(list_comp)

# 使用生成器表達式
start_time = time.time()
gen_exp = (x for x in range(n))  # 只創建生成器對象，不計算值
gen_time = time.time() - start_time
gen_memory = memory_usage(gen_exp)

print(f"列表推導式 - 時間: {list_time:.6f}秒, 內存: {list_memory} 字節")
print(f"生成器表達式 - 時間: {gen_time:.6f}秒, 內存: {gen_memory} 字節")
print(f"內存使用比率 (列表:生成器): {list_memory / gen_memory:.1f}x")


# 5. yield from 表達式
print("\n"+"="*50)
print("yield from 表達式")
print("="*50)

def subgenerator(n):
    """子生成器"""
    for i in range(n):
        yield i

def delegating_generator(n):
    """使用yield from委託給子生成器"""
    yield from subgenerator(n)
    yield from subgenerator(n)  # 可以多次委託

print("使用yield from的委託生成器:")
for num in delegating_generator(3):
    print(num, end=" ")
print()

# 等價的舊式代碼
def old_style_delegating(n):
    """不使用yield from的委託"""
    for i in subgenerator(n):
        yield i
    for i in subgenerator(n):
        yield i

print("\n舊式委託生成器 (等價):")
for num in old_style_delegating(3):
    print(num, end=" ")
print()

# 多層嵌套生成器
def nested_generators():
    """多層嵌套生成器"""
    # 字符串也是可迭代的
    yield from "ABC"
    yield from [10, 20, 30]
    yield from (x**2 for x in range(3))

print("\n多層嵌套生成器:")
for item in nested_generators():
    print(item, end=" ")
print()


# 6. 生成器的高級應用
print("\n"+"="*50)
print("生成器的高級應用")
print("="*50)

# 管道處理
def generate_data():
    """生成測試數據"""
    for i in range(10):
        yield i

def filter_even(data):
    """過濾出偶數"""
    for item in data:
        if item % 2 == 0:
            yield item

def multiply_by_2(data):
    """將數據乘以2"""
    for item in data:
        yield item * 2

# 構建數據處理管道
print("數據處理管道示例:")
pipeline = multiply_by_2(filter_even(generate_data()))
for result in pipeline:
    print(result, end=" ")
print()

# 協程風格生成器 (yield表達式接收值)
def coroutine():
    """協程風格的生成器函數"""
    print("協程啟動")
    while True:
        # yield作為表達式，可以接收send()傳入的值
        value = yield
        print(f"接收到: {value}")

print("\n協程風格生成器:")
co = coroutine()
next(co)  # 必須先調用next()啟動協程，運行到第一個yield處
co.send("Hello")
co.send(42)
co.close()  # 關閉協程


# 7. itertools模塊
print("\n"+"="*50)
print("itertools模塊")
print("="*50)

# 無限迭代器
print("無限迭代器:")
# count - 從n開始計數
count = itertools.count(10, 2)  # 從10開始，步長2
print("itertools.count(10, 2):", end=" ")
for _ in range(5):
    print(next(count), end=" ")
print()

# cycle - 循環迭代元素
cycle = itertools.cycle("ABC")
print("itertools.cycle('ABC'):", end=" ")
for _ in range(7):
    print(next(cycle), end=" ")
print()

# repeat - 重複生成元素
repeat = itertools.repeat("X", 5)  # 重複5次
print("itertools.repeat('X', 5):", end=" ")
for item in repeat:
    print(item, end=" ")
print()

# 有限迭代器
print("\n有限迭代器:")
# chain - 連接多個迭代器
print("itertools.chain([1, 2], [3, 4], [5]):", end=" ")
for item in itertools.chain([1, 2], [3, 4], [5]):
    print(item, end=" ")
print()

# islice - 切片迭代器
print("itertools.islice(range(10), 2, 8, 2):", end=" ")
for item in itertools.islice(range(10), 2, 8, 2):  # 從2開始，到8結束，步長2
    print(item, end=" ")
print()

# 組合生成器
print("\n組合生成器:")
# product - 笛卡爾積
print("itertools.product('AB', '12'):")
for item in itertools.product("AB", "12"):
    print(item, end=" ")
print()

# permutations - 排列
print("\nitertools.permutations('ABC', 2):")
for item in itertools.permutations("ABC", 2):
    print(item, end=" ")
print()

# combinations - 組合
print("\nitertools.combinations('ABCD', 2):")
for item in itertools.combinations("ABCD", 2):
    print(item, end=" ")
print()


# 8. 實際應用: 數據流處理
print("\n"+"="*50)
print("實際應用: 數據流處理")
print("="*50)

class DataProcessor:
    """數據處理器"""
    
    @staticmethod
    def read_data(filename):
        """從文件讀取數據 (模擬)"""
        # 模擬從文件讀取數據
        data = [
            {"id": 1, "name": "Alice", "score": 85},
            {"id": 2, "name": "Bob", "score": 92},
            {"id": 3, "name": "Charlie", "score": 78},
            {"id": 4, "name": "David", "score": 95},
            {"id": 5, "name": "Eve", "score": 88},
        ]
        for record in data:
            yield record
    
    @staticmethod
    def filter_by_score(data_stream, min_score):
        """過濾分數大於等於min_score的記錄"""
        for record in data_stream:
            if record["score"] >= min_score:
                yield record
    
    @staticmethod
    def transform_data(data_stream):
        """轉換數據格式"""
        for record in data_stream:
            # 轉換記錄格式
            yield {
                "student_id": record["id"],
                "full_name": record["name"],
                "grade": DataProcessor._score_to_grade(record["score"])
            }
    
    @staticmethod
    def _score_to_grade(score):
        """將分數轉換為等級"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        else:
            return "D"


# 使用數據處理器進行流處理
print("數據流處理示例:")
# 創建數據處理管道
data = DataProcessor.read_data("scores.txt")  # 模擬文件
filtered_data = DataProcessor.filter_by_score(data, 80)  # 過濾低分
transformed_data = DataProcessor.transform_data(filtered_data)  # 轉換格式

# 處理結果
for record in transformed_data:
    print(record)


# 9. 惰性評估與性能優化
print("\n"+"="*50)
print("惰性評估與性能優化")
print("="*50)

# 生成Fibonacci數列
def fibonacci():
    """生成無限Fibonacci數列的生成器"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print("Fibonacci數列 (前10個數):")
fib = fibonacci()
for _ in range(10):
    print(next(fib), end=" ")
print()

# 生成素數
def is_prime(n):
    """檢查n是否為素數"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def prime_generator():
    """生成無限素數序列的生成器"""
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1


print("\n素數序列 (前10個素數):")
primes = prime_generator()
for _ in range(10):
    print(next(primes), end=" ")
print()


# 使用生成器讀取大文件
def read_large_file(file_path, chunk_size=1024):
    """以塊為單位讀取大文件的生成器"""
    # 在這裡我們只模擬，實際應用中會讀取真實文件
    print(f"模擬打開文件: {file_path}")
    
    # 模擬的文件內容
    content = ["這是第一塊數據。", "這是第二塊數據。", "這是第三塊數據。"]
    
    for chunk in content:
        print(f"讀取塊: {len(chunk)} 字節")
        yield chunk


print("\n使用生成器讀取大文件:")
for chunk in read_large_file("大文件.txt"):
    print(f"處理塊: {chunk}")


# 正則表達式生成器
import re

def regex_search(pattern, text):
    """生成所有匹配模式的結果"""
    for match in re.finditer(pattern, text):
        yield match.group()


print("\n正則表達式匹配生成器:")
text = "Python是一種程式語言，python的優勢在於簡潔，Python也有許多庫。"
pattern = r"[Pp]ython"

print(f"文本: {text}")
print(f"模式: {pattern}")
for match in regex_search(pattern, text):
    print(f"匹配: {match}")

