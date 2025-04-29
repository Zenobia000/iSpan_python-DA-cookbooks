# 好的實踐：明確指定要導出的函數
# 在 Python 模組（.py 檔案）中，__all__ 是一個列表（list），
# 用來明確指定當使用 from module import * 時，可以被導出的名稱。
# 簡單來說，就是一個導出白名單。

# 只導出公開函數
__all__ = ['function1', 'function2']

def function1():
    return "公開函數 1"

def function2():
    return "公開函數 2"

def _internal_helper():
    return "內部輔助函數"
