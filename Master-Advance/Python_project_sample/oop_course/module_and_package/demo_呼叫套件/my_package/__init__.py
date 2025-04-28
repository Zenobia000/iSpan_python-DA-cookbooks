# 暴露模組 API，讓外部程式更容易引用
from .module_a import func_a
from .module_b import func_b
from .subpackage.sub_module import sub_func

__all__ = ["func_a", "func_b", "sub_func"]  # 限定外部 import 內容

# 版本資訊
__version__ = "0.1.0" 