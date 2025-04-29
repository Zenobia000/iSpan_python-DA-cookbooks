# Python 套件上傳到 PyPI 完整 SOP
PyPI = Python Package Index Python 的套件官方集中管理與發布平台
---

## 📚 教學目標

| 階段 | 內容 |
|:---|:---|
| 1 | 自動建立套件資料夾結構 |
| 2 | 撰寫 `setup.py`、`README.md`、`LICENSE` 等必要文件 |
| 3 | 本地打包 `.tar.gz`、`.whl` 檔案 |
| 4 | 上傳到 PyPI 測試站或正式站 |

---

## 🛠️ 1. 用 Python 自動建立套件結構

```python
import os

# 設定專案名稱
package_name = "my_package"

# 資料夾結構
folders = [
    f"{package_name}/{package_name}",
]

# 檔案與內容
files = {
    f"{package_name}/setup.py": """\
from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your package",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.0",
        "pandas>=1.0.0",
    ],
)
""",
    f"{package_name}/README.md": "# My Package\n\nThis is a sample Python package.",
    f"{package_name}/LICENSE": "MIT License",
    f"{package_name}/{package_name}/__init__.py": "# my_package __init__",
    f"{package_name}/{package_name}/module_a.py": """\
def hello_a():
    return "Hello from module_a!"
""",
    f"{package_name}/{package_name}/module_b.py": """\
def hello_b():
    return "Hello from module_b!"
""",
}

# 建立資料夾
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# 建立檔案
for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print(f"✅ {package_name} 結構建立完成！")
```

---

## 📦 2. 打包套件（本機端）

### 指令

```bash
cd my_package
python setup.py sdist bdist_wheel
```

---

### 補充說明

| 指令 | 解釋 |
|:---|:---|
| `cd my_package` | 進入有 `setup.py` 的目錄，準備打包 |
| `python setup.py sdist` | 生成 `.tar.gz` 的原始碼壓縮包（Source Distribution） |
| `python setup.py bdist_wheel` | 生成 `.whl` 的快速安裝檔（Wheel Distribution） |

---

#### ➡️ 什麼是 sdist？

```plaintext
1. sdist — Source Distribution
Source = 原始碼
Distribution = 分發套件

意思是：把原始碼打包成 .tar.gz 或 .zip，
讓其他人可以下載、解壓縮、自己 build 安裝。

✅ 特徵：
- 含原始 .py 檔案。
- 下載後通常需要執行 setup.py install 或其他流程。
- 可在任何平台自行編譯安裝。
```

---

#### ➡️ 什麼是 bdist？

```plaintext
2. bdist — Built Distribution
Built = 已經建構好的
Distribution = 分發套件

意思是：建立建構過的套件格式，
比如 wheel (.whl) 或某些平台的專用格式（如 .exe, .msi）。

✅ 特徵：
- 已整理成快速安裝的格式（例如 .whl）。
- 不需要解壓縮，pip install 直接安裝。
```

---

### 生成的檔案結構

```plaintext
my_package/
├── my_package/
│   ├── __init__.py
│   ├── module_a.py
│   └── module_b.py
├── README.md
├── LICENSE
├── setup.py
├── build/
│   └── my_package.egg-info/
│       ├── dependency_links.txt
│       ├── PKG-INFO
│       ├── requires.txt
│       ├── SOURCES.txt
│       └── top_level.txt
└── dist/
    ├── my_package-0.1.0.tar.gz
    └── my_package-0.1.0-py3-none-any.whl
```

---

### 📂 `my_package.egg-info` 說明

| 檔案 | 說明 |
|:---|:---|
| `PKG-INFO` | 套件的基本描述資訊（版本、作者、描述等） |
| `dependency_links.txt` | 額外依賴連結（通常是空的） |
| `requires.txt` | 安裝需要的套件清單（install_requires） |
| `SOURCES.txt` | 包含在分發包內的所有檔案清單 |
| `top_level.txt` | 套件最上層可以 import 的模組名稱 |

✅ `egg-info` 目錄是 pip、setuptools 需要的內部管理資訊。

---

### 產物說明

| 檔案 | 說明 |
|:---|:---|
| `my_package-0.1.0.tar.gz` | 原始碼壓縮包，需要解壓縮後安裝 |
| `my_package-0.1.0-py3-none-any.whl` | Wheel格式快速安裝檔，建議 pip 優先使用 |

- **`.tar.gz`** 適合需要自行編譯的人。
- **`.whl`** 安裝速度最快，符合現代 PyPI 標準。

---

## 🚀 3. 上傳到 PyPI

### 安裝 Twine（如果尚未安裝）

```bash
pip install twine
```

---

### 上傳到 Test PyPI（建議第一次先測試）

1. 註冊 [Test PyPI 帳號](https://test.pypi.org/account/register/)
2. 執行：

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

（輸入 Test PyPI 帳號密碼）

---

### 上傳到正式 PyPI

1. 註冊 [PyPI 帳號](https://pypi.org/account/register/)
2. 執行：

```bash
twine upload dist/*
```

（輸入正式 PyPI 帳號密碼）

---

## 📘 完整指令流程總表

| 步驟 | 指令 |
|:---|:---|
| 1. 生成資料夾結構 | （執行上方 Python 腳本） |
| 2. 進入套件目錄 | `cd my_package` |
| 3. 打包套件 | `python setup.py sdist bdist_wheel` |
| 4. 安裝 Twine | `pip install twine` |
| 5. 上傳到 Test PyPI | `twine upload --repository-url https://test.pypi.org/legacy/ dist/*` |
| 6. 上傳到正式 PyPI | `twine upload dist/*` |

---

## 🔥 小提醒

- 每次上傳的版本號必須不同（例：0.1.0 → 0.1.1）。
- `README.md` 和 `LICENSE` 是 PyPI 展示的核心文件。
- 上傳前可以用虛擬環境 (venv) 測試自己剛打包的 `.whl` 或 `.tar.gz` 檔案。

---

## 📎 補充：pip 安裝的優先順序

| 格式 | 安裝優先度 |
|:---|:---|
| `.whl` (wheel) | ✅ 最高，最快速安裝 |
| `.tar.gz` (source) | ⚠️ 退而求其次，需要編譯解壓 |

如果 wheel 檔案存在，`pip install` 會優先選擇 `.whl`，大幅提升安裝速度。

---
