# 絕對導入 Absolute Import 定義：
# 從 sys.path[0]（工作目錄）或 sys.path 裡的路徑，依照完整的模組結構一路寫下去的導

import my_package.module_a as ma
import my_package.module_b as mb

print(ma.func_a())
print(mb.func_b())


# # --------------------------------------------

from my_package import module_a, module_b

print(module_a.func_a())
print(module_b.func_b())

# # --------------------------------------------

# 以下是錯誤示範
# 因為 package_basics 沒有 __init__.py	視為普通資料夾，不能 import，他不是一個 package 
# 需要先建立 __init__.py 才能 import

# IDE 導入的根目錄是以程式碼執行位置的當前目錄作為 sys.path[0] 往下找
# 所以 main.py 在 basic_package_structure 資料夾裡面，
# 所以 package_basics 是 sys.path[0] 的上一層，
# 🔵 所以從這個位置，你沒有辦法看到上層的 package_basics，
# 因為 import 查找是從 sys.path[0] 開始往下找的，不會自動往上找！

from package_basics.basic_package_structure.my_package import module_a, module_b

print(module_a.func_a())
print(module_b.func_b())






