# 版本控制基礎 - Git 入門

本節介紹版本控制系統 Git 的基本概念和使用方法，這對於任何軟體開發項目都至關重要。

---

**本節目標：**
- 了解什麼是版本控制
- 學會 Git 的基本操作（init、add、commit、branch、merge）
- 學會與遠程倉庫互動（push、pull、clone）
- 認識 .gitignore 的用途

## 1. 什麼是版本控制？

版本控制是一種跟蹤文件或代碼更改的系統，它允許多人協作並保存更改的歷史記錄。

## 2. Git 基本概念

| 概念 | 說明 |
|:---|:---|
| 倉庫 (Repository) | 包含所有項目文件和歷史記錄的容器 |
| 提交 (Commit) | 代碼更改的快照 |
| 分支 (Branch) | 開發線的獨立版本 |
| 合併 (Merge) | 將一個分支的更改整合到另一個分支 |
| 遠程 (Remote) | 託管在網絡上的倉庫副本 |

## 3. 安裝與配置 Git

### 安裝

#### Windows
到 [git-scm.com](https://git-scm.com/) 下載安裝程式。

#### macOS
```bash
# 方法一：使用 Xcode Command Line Tools
xcode-select --install

# 方法二：使用 Homebrew
brew install git
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install git
```

### 配置

```bash
# 檢查 Git 是否已安裝
git --version

# 配置用戶信息（首次使用必做）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 檢查當前配置
git config --list
```

## 4. 創建和管理 Git 倉庫

```bash
# 初始化新的 Git 倉庫
git init

# 查看倉庫狀態
git status

# 添加文件到暫存區
git add filename.py
git add .              # 添加所有文件

# 提交更改
git commit -m "描述性的提交信息"

# 查看提交歷史
git log
git log --oneline      # 簡潔格式
```

## 5. 分支操作

```bash
# 查看所有分支
git branch

# 創建新分支
git branch feature-x

# 切換到某個分支
git checkout feature-x

# 創建並切換到新分支（簡便方法）
git checkout -b feature-y

# 合併分支
git checkout main          # 先切換到目標分支
git merge feature-x        # 將 feature-x 合併到當前分支

# 刪除已合併的分支
git branch -d feature-x
```

## 6. 遠程倉庫操作

```bash
# 添加遠程倉庫
git remote add origin https://github.com/username/repository.git

# 查看遠程倉庫
git remote -v

# 從遠程倉庫獲取更新
git fetch origin

# 推送到遠程倉庫
git push -u origin main    # 第一次推送設置上游分支
git push                   # 後續推送可簡化

# 從遠程倉庫克隆
git clone https://github.com/username/repository.git

# 拉取遠程更新並合併
git pull origin main
```

## 7. Git 工作流程

```
LOCAL                                      REMOTE
----------------                           ----------------
Working Directory                          GitHub/GitLab/Bitbucket
    |                                          |
    v                                          |
Staging Area                                   |
    |                                          |
    v                                          |
Local Repository ----(git push)-----------> Remote Repository
    ^                                          |
    |                                          |
    <-----------(git pull)--------------------|
```

## 8. 使用 .gitignore 文件

`.gitignore` 文件用於指定 Git 應該忽略的文件或目錄。

典型的 Python 項目 `.gitignore`：

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# 虛擬環境
.venv/
venv/
ENV/

# Jupyter Notebook
.ipynb_checkpoints/

# IDE
.idea/
.vscode/
*.swp

# 作業系統
.DS_Store
Thumbs.db

# 環境變數
.env
```

## 9. 實作練習

1. 為本 OOP 課程項目初始化一個 Git 倉庫
2. 創建並配置適當的 `.gitignore` 文件
3. 提交初始代碼
4. 創建一個新的開發分支並在分支上添加新功能
5. 將更改合併回主分支
