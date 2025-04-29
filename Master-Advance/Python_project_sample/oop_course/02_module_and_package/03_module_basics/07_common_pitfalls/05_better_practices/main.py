print("=== 更好的實踐示範 ===")

# 1. 使用類來管理狀態
from counter import Counter
counter = Counter()
print("\n計數器示例:")
print("初始值:", counter.get_count())
print("增加後:", counter.increment())
print("再增加:", counter.increment())
print("重置後:", counter.reset())


# 2. 明確的模組接口
from clean_module import *

print(function1())  # OK
print(function2())  # OK
print(_internal_helper())  # ❌ NameError，因為沒被列入 __all__



# 2. 明確的模組接口
from clean_module import function1, function2
print("\n清晰的模組使用:")
print("公開函數:", function1())
print("公開函數:", function2())


print("\n最佳實踐總結:")
practices = [
    "使用類封裝相關的狀態和行為",
    "明確定義模組的公開接口",
    "使用 __all__ 控制可導出的名稱",
    "遵循命名規範（如使用下劃線前綴表示私有）",
    "保持模組功能單一且聚焦"
]
for i, practice in enumerate(practices, 1):
    print(f"{i}. {practice}")


