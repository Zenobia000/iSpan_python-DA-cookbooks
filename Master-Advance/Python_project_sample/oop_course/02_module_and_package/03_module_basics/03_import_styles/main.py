# 導入整個模組
import my_math
result_add = my_math.add(5, 3)  # 使用模組名稱作為前綴
print("加法:", result_add)


# 導入特定函數或變數
from my_math import add, subtract, PI
result_add = add(5, 3)  # 直接使用函數名
result_subtract = subtract(5, 3)  # 直接使用函數名
print("PI:", PI)
print("加法:", result_add)
print("減法:", result_subtract)

# 導入所有內容（通常不推薦）
from my_math import *
result_multiply = multiply(5, 3)  # 直接使用，但可能導致命名衝突
print("乘法:", result_multiply)

# 使用別名
import my_math as mm
result_add_alias = mm.add(5, 3)  # 使用較短的別名
print("加法:", result_add_alias)

from my_math import Calculator as Calc

# 建立 my_calc 這個物件
my_calc = Calc(10)  # 使用類的別名
print("計算器初始值:", my_calc.value)

