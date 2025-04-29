# 主題：腳本執行位置與工作目錄可能不同

import os
from pathlib import Path

def get_script_dir():
    if '__file__' in globals():
        return os.path.dirname(os.path.abspath(__file__))
    else:
        return os.getcwd()

print("腳本目錄:", get_script_dir())


print(globals())

