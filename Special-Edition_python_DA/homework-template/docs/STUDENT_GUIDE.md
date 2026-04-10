# 🚀 Git、PR 與 CI/CD — 學生操作手冊

> 這份手冊會教你從零開始，學會用「工程師的方式」繳交作業。
> 這些技能在業界每天都在用，學會了你就贏在起跑點。

---

## 目錄

1. [為什麼要學這些？](#1-為什麼要學這些)
2. [事前準備](#2-事前準備)
3. [核心觀念速懂](#3-核心觀念速懂)
4. [Step by Step 操作](#4-step-by-step-操作)
5. [查看成績與解答](#5-查看成績與解答)
6. [修改重交（改完再 push）](#6-修改重交改完再-push)
7. [常見問題 FAQ](#7-常見問題-faq)

---

## 1. 為什麼要學這些？

| 你現在學的 | 業界怎麼用 |
|:-----------|:-----------|
| **Git** | 所有軟體公司的程式碼版本管理工具，沒有例外 |
| **Fork + PR** | 開源專案的協作方式（你用的 NumPy、Pandas 都是這樣開發的） |
| **CI/CD** | 程式碼一推上去就自動跑測試、自動部署，不用人工檢查 |

> 你繳交作業的過程，就是在模擬真實的軟體開發流程。

---

## 2. 事前準備

### 2.1 註冊 GitHub 帳號

1. 到 [github.com](https://github.com) 註冊
2. 建議用英文 username（之後到處都會顯示）
3. 記住你的 username 和密碼

### 2.2 安裝 Git

**Mac：**
```bash
# 打開 Terminal，輸入：
git --version
# 如果沒安裝會自動提示安裝 Xcode Command Line Tools，按確認即可
```

**Windows：**
1. 到 [git-scm.com](https://git-scm.com) 下載安裝
2. 安裝時全部選預設就好
3. 安裝完打開 **Git Bash**（不是 CMD）

### 2.3 設定 Git 身份

```bash
git config --global user.name "你的名字"
git config --global user.email "你的email@example.com"
```

> 這只需要設一次，之後所有 commit 都會用這個身份。

---

## 3. 核心觀念速懂

### Git 是什麼？

想像 Google Docs 的「版本紀錄」功能 — Git 做的事一模一樣，但更強大：

```
你的程式碼
    │
    ├── 版本 1：「完成送分題」
    ├── 版本 2：「完成核心題」
    ├── 版本 3：「修正 bug」
    └── 版本 4：「完成挑戰題」
```

每個版本叫做一個 **commit**，你可以隨時回到任何一個版本。

### Fork 是什麼？

```
老師的 Repo（原版）
    │
    └── Fork ──→ 你的 Repo（副本，完全屬於你）
                    │
                    └── 你在這裡寫作業
```

Fork = 把老師的作業模板**複製一份**到你的 GitHub 帳號下。
你怎麼改都不會影響老師的原版。

### PR（Pull Request）是什麼？

```
你的 Repo ──── PR ────→ 老師的 Repo
              │
              └── 「老師你好，這是我的作業，請批改」
```

PR = 你主動告訴老師：「我寫完了，請看一下」。
老師可以在 PR 上看到你改了什麼、自動批改的成績也會貼在這裡。

### CI/CD 是什麼？

```
你 push 程式碼
    │
    └── GitHub 偵測到 ──→ 自動啟動機器人
                              │
                              ├── 安裝 Python
                              ├── 安裝套件
                              ├── 跑測試
                              ├── 算分數
                              └── 把成績貼回來
```

CI (Continuous Integration) = 每次你推程式碼，機器人就自動幫你跑測試。
不用人工批改，不用等老師，24/7 全年無休。

---

## 4. Step by Step 操作

### Step 1：Fork 老師的 Repo

1. 老師會給你一個 GitHub 連結
2. 打開連結，點擊右上角的 **「Fork」** 按鈕

   ![Fork 按鈕位置在頁面右上角](https://docs.github.com/assets/cb-40742/mw-1440/images/help/repository/fork-button.webp)

3. 在 "Create a new fork" 頁面，直接點 **「Create fork」**
4. 等幾秒鐘，你的副本就建好了！

> 現在你的 GitHub 帳號下會多一個 repo，網址是：
> `https://github.com/你的帳號/repo名稱`

### Step 2：Clone 到你的電腦

```bash
# 把 "你的帳號" 換成你的 GitHub username
git clone https://github.com/你的帳號/repo名稱.git

# 進入資料夾
cd repo名稱
```

> 你的電腦現在有了這個專案的完整副本。

### Step 3：寫作業

用任何你喜歡的編輯器打開 `homework/` 資料夾裡的 `.py` 檔：

```bash
# 推薦用 VS Code 打開整個專案
code .
```

每個函式長這樣：

```python
def green_mean():
    """建立 [10, 20, 30, 40, 50]，回傳所有元素的平均值"""
    # TODO: 你的程式碼
    pass    # ← 把這行刪掉，換成你的程式碼
```

改成：

```python
def green_mean():
    """建立 [10, 20, 30, 40, 50]，回傳所有元素的平均值"""
    arr = np.array([10, 20, 30, 40, 50])
    return arr.mean()
```

### Step 4：本地測試（選做，但推薦）

```bash
# 先裝套件（第一次做就好）
pip install -r requirements.txt

# 跑測試看結果
python -m pytest tests/test_m1.py -v
```

你會看到類似這樣的輸出：

```
tests/test_m1.py::TestGreen::test_green_mean PASSED     ✅
tests/test_m1.py::TestGreen::test_green_double PASSED   ✅
tests/test_m1.py::TestGreen::test_green_filter FAILED   ❌
```

PASSED = 這題對了，FAILED = 還有問題，看錯誤訊息修正。

### Step 5：儲存 + 上傳（commit + push）

```bash
# 1. 查看你改了哪些檔案
git status

# 2. 把改過的檔案加入「準備提交」清單
git add homework/

# 3. 建立一個存檔點（commit），附上說明
git commit -m "完成 M1 作業"

# 4. 上傳到 GitHub
git push
```

> 每個步驟的類比：
> - `git add` = 把作業放進信封
> - `git commit` = 封口、寫上標題
> - `git push` = 寄出去

### Step 6：發 PR 繳交

1. 到你 fork 的 repo 頁面（`github.com/你的帳號/repo名稱`）
2. 你會看到一個橫幅寫 **「This branch is X commits ahead」**
3. 點 **「Contribute」** → **「Open pull request」**

   或者直接點 **「Compare & pull request」** 按鈕

4. 填寫 PR 資訊：
   - **Title**：`M1 作業 — 你的姓名`
   - **Description**：可以寫心得或留白
5. 點 **「Create pull request」**

> 繳交完成！接下來等 1~2 分鐘，機器人就會自動批改。

---

## 5. 查看成績與解答

### 成績（在老師的 repo）

回到你剛發的 PR 頁面，往下滑，會看到一則自動留言：

```
📊 作業批改結果
總分：75 / 100（75%）— 等級 C

| 題目              | 分數  | 狀態 |
| test_green_mean   | 10/10 | ✅   |
| test_green_double | 10/10 | ✅   |
| ...               | ...   | ...  |
```

### 解答（在你自己的 repo）

1. 到你自己 fork 的 repo 頁面
2. 點上方的 **「Actions」** 頁籤
3. 點最新一次的 **「🔑 我的成績與解答」**
4. 往下滑到 **Job Summary** 區塊

> 解答只會出現在你自己的 Actions 裡，其他同學看不到。

---

## 6. 修改重交（改完再 push）

作業可以無限次修改重交！

```bash
# 1. 修改程式碼
# 2. 重複 Step 5 的流程：
git add homework/
git commit -m "修正核心題 bug"
git push
```

新的 push 會自動觸發重新批改，PR 上的成績也會更新。

---

## 7. 常見問題 FAQ

### Q: `git push` 要求輸入帳號密碼？

GitHub 已經不支援密碼登入了，你需要設定 **Personal Access Token** 或 **SSH Key**：

**方法 A — Token（最簡單）：**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 點 **Generate new token**
3. 勾選 `repo` 權限
4. 產生的 token 當作密碼用

**方法 B — SSH Key（一勞永逸）：**
```bash
# 產生 SSH Key
ssh-keygen -t ed25519 -C "你的email"

# 複製公鑰
cat ~/.ssh/id_ed25519.pub
# 把印出來的內容貼到 GitHub → Settings → SSH keys → New SSH key

# 以後用 SSH 網址 clone
git clone git@github.com:你的帳號/repo名稱.git
```

### Q: `git push` 出現 rejected（被拒絕）？

```bash
# 先拉取最新版本
git pull --rebase
# 再推
git push
```

### Q: 我改錯了想恢復原版？

```bash
# 恢復單一檔案到最後一次 commit 的狀態
git checkout -- homework/m1_numpy.py
```

### Q: Actions 跑了很久沒結果？

- 通常 1~2 分鐘就會完成
- 如果超過 5 分鐘，到 Actions 頁籤看是否有錯誤
- 最常見原因：import 錯誤導致測試無法執行

### Q: 我的 PR 顯示 "merge conflict"？

不用管它！你的作業批改不受影響。Conflict 只是因為老師可能更新了 repo。

### Q: 可以用 GitHub 網頁直接編輯嗎？

可以！但不推薦，因為你無法在網頁上測試程式碼。

---

## 附錄：常用 Git 指令速查

| 指令 | 功能 | 使用時機 |
|:-----|:-----|:---------|
| `git clone <url>` | 下載 repo 到本機 | 第一次取得專案 |
| `git status` | 查看目前狀態 | 隨時都可以看 |
| `git add <file>` | 把檔案加入準備提交 | 改完程式碼後 |
| `git commit -m "訊息"` | 建立存檔點 | add 之後 |
| `git push` | 上傳到 GitHub | commit 之後 |
| `git pull` | 下載最新版本 | 在另一台電腦工作前 |
| `git log --oneline` | 查看提交歷史 | 想看自己做了什麼 |
| `git diff` | 查看尚未提交的修改 | 想確認改了什麼 |

---

## 附錄：這個系統的完整流程圖

```
┌─────────────────────────────────────────────────────────────┐
│                      老師的 Repo                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐   │
│  │ 作業模板  │  │ 測試程式  │  │ CI/CD (grade.yml)        │   │
│  │ homework/ │  │ tests/   │  │ PR 來了 → 跑測試 → 貼分數 │   │
│  └──────────┘  └──────────┘  └──────────────────────────┘   │
│        │                              ▲                      │
│        │ Fork                         │ PR                   │
│        ▼                              │                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              學生的 Fork                              │    │
│  │  1. 寫作業 (homework/)                               │    │
│  │  2. git add + commit + push                         │    │
│  │  3. 發 PR → 繳交                                    │    │
│  │                                                      │    │
│  │  CI/CD (student-grade.yml)                           │    │
│  │  push → 跑測試 → 成績+解答 寫到 Job Summary          │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```
