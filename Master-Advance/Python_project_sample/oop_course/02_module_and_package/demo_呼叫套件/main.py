from my_package import func_a, func_b, sub_func
import my_package

def main():
    print(f"使用 my_package 版本: {my_package.__version__}")
    print("\n直接從套件匯入的函式:")
    print(f"func_a() -> {func_a()}")
    print(f"func_b() -> {func_b()}")
    print(f"sub_func() -> {sub_func()}")
    
    print("\n透過完整路徑匯入:")
    # 即使沒有在 __all__ 中列出，我們仍然可以透過完整路徑匯入
    from my_package.module_a import another_func_a
    from my_package.module_b import internal_func_b
    from my_package.subpackage.sub_module import helper_func
    
    print(f"another_func_a() -> {another_func_a()}")
    print(f"internal_func_b() -> {internal_func_b()}")
    print(f"helper_func() -> {helper_func()}")

if __name__ == "__main__":
    main() 