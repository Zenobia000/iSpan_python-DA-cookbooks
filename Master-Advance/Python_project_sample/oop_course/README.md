# Python 物件導向程式設計課程

此專案為 Python 物件導向程式設計系列課程的源碼庫，以 Jupyter Notebook 風格 `.py` 檔案的形式提供。

## 課程結構

課程內容分為以下幾個主要部分：

1. **環境設置與版本控制**
   - 虛擬環境的使用與套件管理
   - Git 版本控制入門

2. **模組與套件**
   - 模組基礎
   - 套件結構
   - 檔案路徑處理

3. **物件導向基礎**
   - 函數式 vs 物件導向
   - 類別與實例基礎
   - 方法與屬性
   - 封裝與資訊隱藏

4. **物件導向進階**
   - 繼承機制
   - 多重繼承與 MRO
   - 多型與抽象基類
   - 特殊方法與運算子重載

5. **設計模式**
   - 裝飾器模式
   - 迭代器與生成器
   - 描述器與元類別
   - 常見設計模式

6. **專案與測試**
   - 測試與文檔
   - 最終專案

## 檔案格式說明

本課程的所有範例代碼以 `.py` 格式提供，但採用 Jupyter Notebook 風格的分段格式，使您可以：

1. 在標準 Python 編輯器中查看和運行完整代碼
2. 使用支援 Python 檔案轉換為 Jupyter Notebook 的工具（如 Jupytext）將檔案轉換為 `.ipynb` 格式

每個 `.py` 檔案包含的特殊標記：

- `# %% [markdown]` - 標記 Markdown 文字區塊
- `# %%` - 標記程式碼區塊

## 使用方法

### 以 Python 腳本方式執行

```bash
python oop_basics/07_class_and_instance_basics.py
```

### 轉換為 Jupyter Notebook

使用 Jupytext 轉換：

```bash
pip install jupytext
jupytext --to notebook module_and_package/03_module_basics.py
```

## 環境要求

請參閱 `requirements.txt` 文件了解必要的套件。基本安裝：

```bash
pip install -r requirements.txt
```

## 學習建議

1. 按順序學習課程內容，每個主題都建立在前面的基礎上
2. 執行每個範例代碼並嘗試修改以加深理解
3. 完成每個檔案末尾的實作練習
4. 參考本專案的 [Wiki](https://github.com/username/python_oop_course/wiki) 獲取更多學習資源

## 授權

[MIT 授權](LICENSE) 