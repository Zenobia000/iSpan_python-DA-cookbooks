"""跨平台繁體中文字型設定輔助模組。

本模組提供統一介面，自動偵測作業系統並為 matplotlib 與 plotly 設定
可用的繁體中文字型，避免圖表出現「豆腐字」（□□□）。

使用方式：
    from common.font_setup import setup_chinese_font, set_plotly_chinese_font
    setup_chinese_font()          # matplotlib / seaborn
    set_plotly_chinese_font()     # plotly express / graph_objects
"""
from __future__ import annotations

import platform
from typing import Optional

_FONT_CANDIDATES = {
    "Darwin": ["PingFang TC", "Heiti TC", "Arial Unicode MS"],
    "Windows": ["Microsoft JhengHei", "Microsoft YaHei", "SimHei"],
    "Linux": ["Noto Sans CJK TC", "WenQuanYi Zen Hei", "Source Han Sans TC"],
}

_INSTALL_HINT = {
    "Darwin": "macOS 內建應已包含 PingFang TC，請確認系統字型未被移除。",
    "Windows": "Windows 內建應已包含 Microsoft JhengHei，請檢查控制台字型設定。",
    "Linux": "請執行：sudo apt install fonts-noto-cjk（Ubuntu/Debian）。",
}


def _available_cjk_fonts(candidates: list[str]) -> list[str]:
    """回傳 matplotlib fontManager 中實際存在的候選字型。"""
    from matplotlib import font_manager

    installed = {f.name for f in font_manager.fontManager.ttflist}
    return [name for name in candidates if name in installed]


def setup_chinese_font() -> Optional[str]:
    """偵測平台並設定 matplotlib 繁體中文字型。

    Returns:
        成功選用的字型名稱；若無任何候選字型可用則回傳 None 並印出安裝提示。
    """
    import matplotlib.pyplot as plt

    system = platform.system()
    candidates = _FONT_CANDIDATES.get(system, _FONT_CANDIDATES["Linux"])
    available = _available_cjk_fonts(candidates)

    if not available:
        print(f"[font_setup] 找不到可用的繁體中文字型（平台：{system}）。")
        print(f"[font_setup] 安裝建議：{_INSTALL_HINT.get(system, '請手動安裝 Noto Sans CJK TC。')}")
        return None

    chosen = available[0]
    plt.rcParams["font.sans-serif"] = [chosen] + plt.rcParams.get("font.sans-serif", [])
    plt.rcParams["axes.unicode_minus"] = False
    print(f"[font_setup] 已套用 matplotlib 中文字型：{chosen}")
    return chosen


def set_plotly_chinese_font(font_name: Optional[str] = None) -> Optional[str]:
    """設定 plotly 預設模板的中文字型。

    Args:
        font_name: 指定字型；若為 None 則依平台自動挑選。

    Returns:
        實際套用的字型名稱，或 None。
    """
    import plotly.io as pio

    if font_name is None:
        system = platform.system()
        candidates = _FONT_CANDIDATES.get(system, _FONT_CANDIDATES["Linux"])
        available = _available_cjk_fonts(candidates)
        font_name = available[0] if available else None

    if font_name is None:
        print("[font_setup] plotly 未設定中文字型：找不到可用字型。")
        return None

    template_name = pio.templates.default or "plotly"
    template = pio.templates[template_name]
    template.layout.font.family = font_name
    print(f"[font_setup] 已套用 plotly 中文字型：{font_name}（template={template_name}）")
    return font_name


if __name__ == "__main__":
    from matplotlib import font_manager

    print(f"偵測平台：{platform.system()}")
    candidates = _FONT_CANDIDATES.get(platform.system(), [])
    print(f"候選字型：{candidates}")
    installed = {f.name for f in font_manager.fontManager.ttflist}
    print(f"系統實際可用的候選字型：{[c for c in candidates if c in installed]}")
    chosen = setup_chinese_font()
    print(f"最終選用：{chosen}")
