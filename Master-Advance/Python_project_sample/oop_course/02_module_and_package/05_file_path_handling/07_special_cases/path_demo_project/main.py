# 主題：.py 套件導入路徑示範

from pathlib import Path
import sys

# 正確做法：加入專案根目錄到 sys.path
sys.path.append(str(Path(__file__).parent))

from mypackage import module_a

print(str(Path(__file__).parent))

print(module_a.greet("Python Script"))
