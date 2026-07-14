# -*- coding: utf-8 -*-
"""主题系统 — 日间/夜间模式配色管理"""

# ==================== 日间主题 ====================
DAY_THEME = {
    "HEADER_COLOR": "#12B7F5",
    "BG_COLOR": "#F5F6FA",
    "BTN_COLOR": "#12B7F5",
    "BTN_ACTIVE": "#0E9BD6",
    "CARD_BG": "#FFFFFF",
    "LOGOUT_BG": "#FF4D4F",
    "LOGOUT_ACTIVE": "#D9363E",
    "INPUT_HIGHLIGHT": "#12B7F5",
    "INPUT_BORDER": "#DDDDDD",
    "INPUT_BG": "#FFFFFF",
    "TEXT_PRIMARY": "#333333",
    "TEXT_GRAY": "#666666",
    "TEXT_LIGHT_GRAY": "#999999",
    "TEXT_BLACK": "#333333",
    "TEXT_WHITE": "#FFFFFF",
    "ONLINE_GREEN": "#52C41A",
    "DIVIDER_GRAY": "#EEEEEE",
    "SIDEBAR_BG": "#2C3E50",
    "SIDEBAR_BTN_BG": "#34495E",
    "SIDEBAR_BTN_ACTIVE": "#1A252F",
    "SIDEBAR_TEXT": "#FFFFFF",
    "CHAT_TITLE_BG": "#FFFFFF",
    "CHAT_AREA_BG": "#FFFFFF",
    "MSG_DISPLAY_BG": "#F5F6FA",
    "LEFT_BOX_BG": "#EEEEEE",
    "LEFT_BOX_TEXT": "#333333",
    "POPUP_HEADER_BG": "#12B7F5",
    "BTN_GREEN": "#52C41A",
    "BTN_RED": "#FF4D4F",
    # 打卡页
    "CAL_CHECKED_BG": "#E8F5E9",
    "CAL_CHECKED_FG": "#2E7D32",
    "CAL_TODAY_BG": "#E3F2FD",
    "CAL_TODAY_FG": "#12B7F5",
    "BINDING_LABEL_FG": "#E8F7FF",
    "FRAME_BORDER": "#DDDDDD",
}

# ==================== 夜间主题 ====================
NIGHT_THEME = {
    "HEADER_COLOR": "#1a1a2e",
    "BG_COLOR": "#16213e",
    "BTN_COLOR": "#0f3460",
    "BTN_ACTIVE": "#1a4a8a",
    "CARD_BG": "#1a1a2e",
    "LOGOUT_BG": "#c0392b",
    "LOGOUT_ACTIVE": "#e74c3c",
    "INPUT_HIGHLIGHT": "#0f3460",
    "INPUT_BORDER": "#34495e",
    "INPUT_BG": "#16213e",
    "TEXT_PRIMARY": "#ecf0f1",
    "TEXT_GRAY": "#bdc3c7",
    "TEXT_LIGHT_GRAY": "#7f8c8d",
    "TEXT_BLACK": "#ecf0f1",
    "TEXT_WHITE": "#FFFFFF",
    "ONLINE_GREEN": "#2ecc71",
    "DIVIDER_GRAY": "#2c3e50",
    "SIDEBAR_BG": "#0f0f23",
    "SIDEBAR_BTN_BG": "#1a1a2e",
    "SIDEBAR_BTN_ACTIVE": "#16213e",
    "SIDEBAR_TEXT": "#ecf0f1",
    "CHAT_TITLE_BG": "#1a1a2e",
    "CHAT_AREA_BG": "#1a1a2e",
    "MSG_DISPLAY_BG": "#16213e",
    "LEFT_BOX_BG": "#0f0f23",
    "LEFT_BOX_TEXT": "#ecf0f1",
    "POPUP_HEADER_BG": "#1a1a2e",
    "BTN_GREEN": "#2ecc71",
    "BTN_RED": "#e74c3c",
    # 打卡页
    "CAL_CHECKED_BG": "#1a3a1a",
    "CAL_CHECKED_FG": "#2ecc71",
    "CAL_TODAY_BG": "#0f3460",
    "CAL_TODAY_FG": "#3498db",
    "BINDING_LABEL_FG": "#bdc3c7",
    "FRAME_BORDER": "#34495e",
}

# ==================== 当前主题状态 ====================
_current_theme = "day"  # "day" 或 "night"


def get_theme():
    """获取当前主题配色字典"""
    if _current_theme == "day":
        return DAY_THEME
    return NIGHT_THEME


def get_theme_mode() -> str:
    """获取当前主题模式名"""
    return _current_theme


def set_theme(mode: str):
    """设置主题模式 'day' 或 'night'"""
    global _current_theme
    if mode in ("day", "night"):
        _current_theme = mode


def toggle_theme() -> str:
    """切换主题，返回新的模式名 'day'/'night'"""
    global _current_theme
    _current_theme = "night" if _current_theme == "day" else "day"
    return _current_theme