# 循環導入示例 A
print("正在導入 circular_a.py")
from circular_b import b_function

def a_function():
    print("這是 A 模組的函數")
