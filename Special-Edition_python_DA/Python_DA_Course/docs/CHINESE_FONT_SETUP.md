# 繁體中文字型設定指引

> 適用於本課程 M4（matplotlib + seaborn）與 M6（plotly）所有筆記本。

## 為什麼會出現「豆腐字」？

matplotlib 與 plotly 預設使用的字型家族（DejaVu Sans、Open Sans 等）並未包含 CJK（中文、日文、韓文）字符，因此當圖表標題、軸標籤或圖例含有中文時，字形渲染器找不到對應的 glyph，就會以空心方塊 □□□（俗稱「豆腐字」）取代。解法是改用系統中已安裝、且包含 CJK 字符的字型。

## 快速使用

在任何筆記本或腳本最上方加入：

```python
from common.font_setup import setup_chinese_font, set_plotly_chinese_font

setup_chinese_font()          # 供 matplotlib / seaborn 使用
set_plotly_chinese_font()     # 供 plotly express / graph_objects 使用
```

輔助模組會自動依作業系統挑選下列順序的字型：

| 平台 | 優先順序 |
| :--- | :--- |
| macOS | PingFang TC → Heiti TC → Arial Unicode MS |
| Windows | Microsoft JhengHei → Microsoft YaHei → SimHei |
| Linux | Noto Sans CJK TC → WenQuanYi Zen Hei → Source Han Sans TC |

## 各平台手動安裝

### macOS
系統內建 **PingFang TC**，無需額外安裝。若遭移除，可從「字體册」重新啟用。

### Windows
系統內建 **微軟正黑體 (Microsoft JhengHei)**，無需額外安裝。

### Linux（Ubuntu / Debian）
```bash
sudo apt update
sudo apt install -y fonts-noto-cjk
```
安裝後請重新啟動 Python kernel，並清除 matplotlib 字型快取：
```bash
rm -rf ~/.cache/matplotlib
```

### Google Colab / 雲端環境
```python
!apt install -y fonts-noto-cjk
!rm -rf ~/.cache/matplotlib
```
接著從選單選擇「執行階段 → 重新啟動執行階段」後重新執行 `setup_chinese_font()`。

## 驗證片段

執行以下程式碼，若標題正確顯示繁體中文即代表設定成功：

```python
import matplotlib.pyplot as plt
from common.font_setup import setup_chinese_font

setup_chinese_font()

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title("中文字型測試：臺灣資料分析課程")
ax.set_xlabel("時間（月）")
ax.set_ylabel("數量")
plt.show()
```

Plotly 驗證：

```python
import plotly.express as px
from common.font_setup import set_plotly_chinese_font

set_plotly_chinese_font()
fig = px.bar(x=["一月", "二月", "三月"], y=[10, 20, 15], title="中文標題測試")
fig.show()
```

## 疑難排解

- 仍顯示豆腐字：刪除 `~/.cache/matplotlib` 後重啟 kernel。
- 執行 `python common/font_setup.py` 可列出目前系統偵測到的候選字型，便於除錯。
