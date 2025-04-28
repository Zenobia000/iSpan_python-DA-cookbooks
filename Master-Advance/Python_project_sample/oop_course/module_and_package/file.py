import os

# 根目錄
base_structure = {
    "my_package": {
        "__init__.py": """
# 頂層套件初始化
from .module_a import function_a
from .module_b import function_b
""",
        "module_a.py": """
def function_a():
    print("Function A from module_a")
""",
        "module_b.py": """
def function_b():
    print("Function B from module_b")
""",
        "subpackage_1": {
            "__init__.py": """
# 子套件 1 初始化
from .module_c import function_c
from .module_d import function_d
""",
            "module_c.py": """
from .module_d import function_d

def function_c():
    print("Function C from module_c")
    function_d()
""",
            "module_d.py": """
def function_d():
    print("Function D from module_d")
"""
        },
        "subpackage_2": {
            "__init__.py": """
# 子套件 2 初始化
from .module_e import function_e
from .module_f import function_f
""",
            "module_e.py": """
def function_e():
    print("Function E from module_e")
""",
            "module_f.py": """
def function_f():
    print("Function F from module_f")
"""
        }
    },
    "demo": {
        "example_absolute_import.py": """
# Demo: 使用絕對導入
from my_package import function_a, function_b
from my_package.subpackage_1 import function_c
from my_package.subpackage_2 import function_e

def main():
    function_a()
    function_b()
    function_c()
    function_e()

if __name__ == "__main__":
    main()
""",
        "example_relative_import.py": """
# Demo: 直接在 module_c.py 示範相對導入，不需要額外寫
# 這個檔只是說明，不直接運行

相對導入只適用在「套件內部模組彼此之間」
print("請執行: my_package/subpackage_1/module_c.py 作為模組，示範相對導入")
"""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.strip())

# 執行建立
create_structure(".", base_structure)

print("✅ 套件結構（含相對與絕對導入範例）已完成！")



# my_package/
#     __init__.py
#     module_a.py
#     module_b.py
#     subpackage_1/
#         __init__.py
#         module_c.py
#         module_d.py
#     subpackage_2/
#         __init__.py
#         module_e.py
#         module_f.py
# demo/
#     example_absolute_import.py
#     example_relative_import.py
