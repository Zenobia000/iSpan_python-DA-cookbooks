# Python 進階教學：從基礎到物件導向

本教學專案旨在幫助 Python 基礎學生順利過渡到物件導向程式設計，同時解決常見的模組、套件和檔案處理問題。

## 學習目標

1. 掌握 Python 模組和套件概念
2. 理解 `__init__.py` 的作用和重要性
3. 學習正確處理檔案路徑（跨資料夾存取）
4. 認識 `.py` 和 `.ipynb` 環境下的差異
5. 實踐物件導向設計原則

## 課程章節

### 第一章：模組和套件基礎

1. [模組的概念與匯入方法](./tutorials/01_modules.md)
2. [建立自己的套件](./tutorials/02_packages.md)
3. [`__init__.py` 的功能與設計](./tutorials/03_init_files.md)

### 第二章：檔案路徑與讀取

1. [相對與絕對路徑](./tutorials/04_file_paths.md)
2. [跨資料夾存取檔案](./tutorials/05_cross_folder.md)
3. [`.py` 與 `.ipynb` 環境差異](./tutorials/06_py_vs_ipynb.md)

### 第三章：物件導向設計

1. [從函數到類別](./tutorials/07_functions_to_classes.md)
2. [繼承與多型](./tutorials/08_inheritance.md)
3. [封裝與私有屬性](./tutorials/09_encapsulation.md)
4. [設計模式入門](./tutorials/10_design_patterns.md)

## 專案結構說明

```
Python_project_sample/
│
├── main.py                 # 主程式進入點
├── my_package/             # 範例套件
│   ├── __init__.py         # 套件初始化檔案
│   ├── module_a.py         # 模組 A
│   ├── module_b.py         # 模組 B
│   └── subpackage/         # 子套件
│       ├── __init__.py     # 子套件初始化檔案
│       └── sub_module.py   # 子模組
│
├── tutorials/              # 教學文件
│   ├── 01_modules.md
│   ├── 02_packages.md
│   └── ...
│
├── examples/               # 完整範例
│   ├── file_handling/      # 檔案處理範例
│   └── oop_examples/       # 物件導向範例
│
└── tests/                  # 測試檔案
```

## 如何使用本教學

1. 按照章節順序學習，每個主題都建立在前一個主題的基礎上
2. 執行各章節中的範例代碼，理解其工作原理
3. 完成每章節後的練習題，鞏固所學知識
4. 參考 `examples` 目錄中的完整範例，了解實際應用

## 開始使用

```bash
# 克隆此倉庫
git clone <repository-url>

# 進入專案目錄
cd Python_project_sample

# 運行主程式查看套件範例
python main.py
``` 