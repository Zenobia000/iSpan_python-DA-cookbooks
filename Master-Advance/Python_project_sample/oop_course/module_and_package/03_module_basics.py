# %% [markdown]
# # 模組基礎
# 
# 本節將介紹Python模組的基本概念、使用方法以及常見陷阱。

# %% [markdown]
# ## 1. 什麼是模組？
# 
# 在Python中，模組是包含Python定義和語句的文件。模組名稱就是文件名（不含`.py`後綴）。

# %%
print("模組的主要優點:")
advantages = [
    "代碼重用 - 一次編寫，多處使用",
    "命名空間管理 - 避免命名衝突",
    "可維護性 - 將相關功能分組在一起",
    "邏輯分離 - 將代碼分散到多個文件中"
]

for i, adv in enumerate(advantages, 1):
    print(f"{i}. {adv}")

# %% [markdown]
# ## 2. 創建自己的模組
# 
# 任何Python文件都可以作為模組被導入。讓我們創建一個簡單的模組來說明。

# %%
# 這段代碼展示如何創建一個模組文件
module_code = """
# 文件: my_math.py

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
"""

print("自定義模組示例:")
print(module_code)

# %% [markdown]
# ## 3. 導入模組的方式

# %%
# 展示不同的導入方式
import_examples = [
    "# 導入整個模組",
    "import my_math",
    "result = my_math.add(5, 3)  # 使用模組名稱作為前綴",
    
    "\n# 導入特定函數或變數",
    "from my_math import add, subtract, PI",
    "result = add(5, 3)  # 直接使用函數名",
    
    "\n# 導入所有內容（通常不推薦）",
    "from my_math import *",
    "result = multiply(5, 3)  # 直接使用，但可能導致命名衝突",
    
    "\n# 使用別名",
    "import my_math as mm",
    "result = mm.add(5, 3)  # 使用較短的別名",
    
    "from my_math import Calculator as Calc",
    "my_calc = Calc(10)  # 使用類的別名"
]

print("模組導入方式:")
for example in import_examples:
    print(example)

# %% [markdown]
# ## 4. 模組搜索路徑
# 
# Python如何找到要導入的模組？

# %%
import sys

print("Python 搜索模組的路徑:")
for i, path in enumerate(sys.path, 1):
    print(f"{i}. {path}")

print("\n模組搜索順序:")
search_order = [
    "當前目錄",
    "PYTHONPATH 環境變數中的目錄",
    "標準庫目錄",
    "site-packages 目錄（第三方庫）"
]
for i, location in enumerate(search_order, 1):
    print(f"{i}. {location}")

# %% [markdown]
# ## 5. `if __name__ == "__main__"` 的用途

# %%
# 說明 __name__ 變數和它的用途
name_example = """
# 文件: example.py

def say_hello(name):
    return f"Hello, {name}!"

# 當作為主程序運行時執行的代碼
if __name__ == "__main__":
    print("這個模組正作為主程序運行")
    print(say_hello("Python"))
else:
    print("這個模組已被導入到另一個模組")
"""

print("__name__ 變數使用示例:")
print(name_example)

print("\n執行方式的區別:")
print("1. 作為主程序運行: python example.py")
print("   此時 __name__ 的值為 \"__main__\"")
print("2. 作為模組導入: import example")
print("   此時 __name__ 的值為 \"example\"")

# %% [markdown]
# ## 6. 模組的重載

# %%
import importlib

reload_example = """
# 已導入模組後，如果模組文件發生了變化：
import my_module

# ...模組文件被編輯...

# 重新載入更新後的模組
import importlib
importlib.reload(my_module)
"""

print("重載模組示例:")
print(reload_example)

# %% [markdown]
# ## 7. 常見陷阱和最佳實踐

# %%
pitfalls = [
    "循環導入 - 當兩個模組互相導入對方時",
    "遮蔽內置名稱 - 例如命名文件為 'sys.py' 或 'os.py'",
    "使用全局變數 - 可能導致難以跟踪的狀態問題",
    "過度使用 'from module import *' - 可能導致命名空間污染"
]

best_practices = [
    "使用有描述性的模組名稱",
    "保持模組功能聚焦且單一",
    "提供清晰的文檔字符串",
    "遵循 PEP 8 命名約定",
    "使用相對導入處理包內模組關係"
]

print("常見陷阱:")
for pitfall in pitfalls:
    print(f"- {pitfall}")

print("\n最佳實踐:")
for practice in best_practices:
    print(f"- {practice}")

# %% [markdown]
# ## 8. 實作練習
# 
# 1. 創建一個名為 `geometry.py` 的模組，包含計算各種形狀面積和體積的函數
# 2. 創建另一個名為 `use_geometry.py` 的文件，導入並使用 `geometry` 模組
# 3. 擴展 `geometry` 模組，添加新的形狀和計算，然後重載模組以獲取更新 