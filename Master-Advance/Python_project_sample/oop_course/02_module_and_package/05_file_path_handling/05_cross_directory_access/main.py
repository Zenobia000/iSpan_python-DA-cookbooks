# 主題：項目結構在開發環境與部署環境可能不同

from pathlib import Path

# 以下好處可以讓程式碼在不同環境下都能正常運行
base_dir = Path(__file__).parent
data_file = base_dir / "data" / "input.csv"

print("Data File Path:", data_file)

from utils import helpers
helpers.helper_function()

