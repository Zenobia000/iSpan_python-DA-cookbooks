print("=== 全局變數問題示範 ===")
from global_state import increment, get_counter, reset_counter

print("初始狀態:", get_counter())
print("增加一次:", increment())
print("再增加:", increment())
print("當前狀態:", get_counter())
print("重置:", reset_counter())
print("最終狀態:", get_counter())

print("\n問題說明:")
print("1. 全局變數使程式狀態難以追蹤")
print("2. 可能導致意外的副作用")
print("3. 使測試變得困難")

print("\n更好的方式:")
print("1. 使用類來封裝狀態")
print("2. 通過參數傳遞數據")
print("3. 使用不可變數據結構")
