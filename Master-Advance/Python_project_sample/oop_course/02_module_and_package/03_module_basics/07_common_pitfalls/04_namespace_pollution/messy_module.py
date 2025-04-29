# messy_module.py

def function1():
    return "function1 from messy_module"

def function2():
    return "function2 from messy_module"

def print_():
    return "👎 被覆蓋的內建 print"

def open_():
    return "👎 被覆蓋的內建 open"

def sum_(a, b):
    return f"👎 偽 sum: {str(a)} + {str(b)} = {str(a + b)}, 但你再也不能用內建 sum 了"

def secret_util():
    return "這應該是內部使用，不該被 export"

# 故意不寫 __all__，暴露所有函數與污染名稱
# __all__ = ["function1", "function2", "print", "open", "sum", "secret_util"]
