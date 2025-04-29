# 循環導入示例 B
print("正在導入 circular_b.py")
from circular_a import a_function

def b_function():
    print("這是 B 模組的函數")
