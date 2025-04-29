print("=== 🧨 命名空間污染問題示範 ===")

print("方式 1: 使用 from messy_module import *")
try:
    from messy_module import *
    print("- 呼叫被覆蓋的 print:", print_())       # 💥 不是原生 print
    print("- 呼叫被覆蓋的 open:", open_())         # 💥 不是內建 open
    print("- 呼叫被覆蓋的 sum:", sum_(123, 3))   # 💥 爆錯，sum 被污染


except Exception as e:
    print("⚠️ 發生錯誤:", str(e))

print("\n方式 2: 使用明確導入（建議）")
import messy_module

print("- 使用 module prefix 呼叫:", messy_module.function1())
print("- 不會污染內建函數:", sum([1, 2, 3]))  # ✅ 照常使用內建 sum

print("\n📌 問題說明:")
print("1. 使用 * 導入會導入整包，包括破壞性名稱（如 print, open, sum）")
print("2. 原生內建函數被覆蓋，debug 超痛苦")
print("3. 無 __all__ 控制時，全模組暴露，毫無封裝性")

print("\n✅ 最佳實踐:")
print("1. 模組端定義 __all__ 控制暴露 API")
print("2. 使用 `from xxx import yyy` 精準導入")
print("3. 避免在模組中使用與 built-in 相同的名稱")
