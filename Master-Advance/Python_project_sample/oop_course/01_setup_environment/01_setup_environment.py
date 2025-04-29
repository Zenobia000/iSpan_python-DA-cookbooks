
# %% [markdown]
# # Python OOP 課程 - 環境設置
# 
# 本節將介紹如何使用 **Poetry** 來建立和管理 Python 開發環境，確保每個專案有獨立的依賴與配置。

# %% [markdown]
# ## 1. 虛擬環境與套件管理的重要性
# 
# 在現代Python開發中，良好的環境隔離與依賴管理至關重要。**Poetry** 是一個流行且現代化的工具，提供一站式的專案初始化、依賴管理與發佈流程。

# %% [markdown]
# ## 2. 安裝 Poetry
# 
# ### 官方推薦安裝指令
# 
# 請在終端機執行以下指令安裝 Poetry：

# %%
print("# 安裝 Poetry")
print("curl -sSL https://install.python-poetry.org | python3")

# %% [markdown]
# ### 驗證安裝

# %%
print("# 驗證 Poetry 是否安裝成功")
print("poetry --version")

# %% [markdown]
# ## 3. 使用 Poetry 初始化專案

# %%
print("# 建立新的專案資料夾")
print("mkdir python_oop_course")
print("cd python_oop_course")

print("\n# 使用 Poetry 初始化")
print("poetry init")
print("# 依指示回答問題，或直接 -n 快速初始化")
print("poetry init -n")

# %% [markdown]
# ## 4. 依賴套件管理
# 
# 使用 Poetry 管理套件相當直覺，下面是常見的操作方法：

# %% [markdown]
# ### 4.1 安裝套件

# %%
required_packages = [
    "jupyter",
    "matplotlib",
    "pandas",
    "pytest",
]

print("# 安裝本課程所需套件")
for pkg in required_packages:
    print(f"poetry add {pkg}")

# %% [markdown]
# ### 4.2 更新套件

# %%
print("# 更新單一套件")
print("poetry update 套件名稱")

print("\n# 更新所有套件")
print("poetry update")

# %% [markdown]
# ### 4.3 移除套件

# %%
print("# 移除單一套件")
print("poetry remove 套件名稱")

# %% [markdown]
# ## 5. 進入虛擬環境

# %%
print("# 啟動 Poetry 虛擬環境的 Shell")
print("poetry shell")

# %% [markdown]
# ## 6. 執行 Python 腳本或 Notebook

# %%
print("# 在 Poetry 環境中執行 Python")
print("poetry run python your_script.py")

print("\n# 或啟動 Jupyter Notebook")
print("poetry run jupyter notebook")

# %% [markdown]
# ## 7. Poetry常見檔案說明
# 
# - `pyproject.toml`：記錄專案名稱、描述、作者與套件依賴
# - `poetry.lock`：鎖定具體的套件版本，確保環境一致性
# - `.venv/`：(可選)儲存 Poetry 建立的虛擬環境，視設定而定

# %% [markdown]
# ## 8. 本課程需要的套件

# %%
print("課程推薦安裝以下套件：")
for pkg in required_packages:
    print(f"- {pkg}")
    
print("\n建議安裝指令:")
print(f"poetry add {' '.join(required_packages)}")

# %% [markdown]
# ## 9. 驗證套件安裝狀態

# %%
def check_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

for package in required_packages:
    status = "已安裝" if check_package_installed(package) else "未安裝"
    print(f"{package}: {status}")

# %% [markdown]
# ## 10. IDE 推薦
# 
# 以下是適合 Python 開發且支援 Poetry 的 IDE 和編輯器:
# 
# 1. **VS Code** + Python Extension (推薦！原生支援 Poetry)
# 2. **PyCharm Professional** (內建 Poetry 整合)
# 3. **Jupyter Lab** (資料分析友善，可搭配 `poetry run jupyter lab` 啟動)
# 4. **Vim + coc.nvim** (進階用戶適用)

# %% [markdown]
# ## 11. 實作練習
# 
# 1. 使用 Poetry 建立一個名為 `oop_course_env` 的專案
# 2. 安裝課程所需套件
# 3. 進入 Poetry 環境並驗證所有套件是否正確安裝

---

# ✅ 重點整理

| 項目                  | 指令範例                              |
|:-----------------------|:--------------------------------------|
| 安裝 Poetry            | `curl -sSL https://install.python-poetry.org | python3` |
| 初始化專案             | `poetry init`                         |
| 新增套件               | `poetry add pandas`                   |
| 移除套件               | `poetry remove pandas`                |
| 更新套件               | `poetry update`                       |
| 啟動虛擬環境           | `poetry shell`                        |
| 執行 Python 指令       | `poetry run python xxx.py`             |

---

要不要順便也一起規劃**pyproject.toml**的標準範本？  
（讓學生直接copy一份最快上手！）  
要的話我可以補一版！要繼續嗎？🚀  
要繼續的話也可以順便問你要不要預設 Python 版本（例如 3.11 or 3.12）？