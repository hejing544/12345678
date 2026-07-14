# -*- coding: utf-8 -*-
"""全局配置常量 — 颜色、字体、尺寸、文件路径、默认用户"""
from theme import get_theme, set_theme, toggle_theme, get_theme_mode

# ====================== 颜色常量（动态从 theme 读取） ======================
def HEADER_COLOR():
    return get_theme()["HEADER_COLOR"]

def BG_COLOR():
    return get_theme()["BG_COLOR"]

def BTN_COLOR():
    return get_theme()["BTN_COLOR"]

def BTN_ACTIVE():
    return get_theme()["BTN_ACTIVE"]

def CARD_BG():
    return get_theme()["CARD_BG"]

def LOGOUT_BG():
    return get_theme()["LOGOUT_BG"]

def LOGOUT_ACTIVE():
    return get_theme()["LOGOUT_ACTIVE"]

def INPUT_HIGHLIGHT():
    return get_theme()["INPUT_HIGHLIGHT"]

def INPUT_BORDER():
    return get_theme()["INPUT_BORDER"]

def TEXT_GRAY():
    return get_theme()["TEXT_GRAY"]

def TEXT_LIGHT_GRAY():
    return get_theme()["TEXT_LIGHT_GRAY"]

def TEXT_BLACK():
    return get_theme()["TEXT_BLACK"]

def ONLINE_GREEN():
    return get_theme()["ONLINE_GREEN"]

def DIVIDER_GRAY():
    return get_theme()["DIVIDER_GRAY"]

# 新增主题相关的颜色
def SIDEBAR_BG():
    return get_theme()["SIDEBAR_BG"]

def SIDEBAR_BTN_BG():
    return get_theme()["SIDEBAR_BTN_BG"]

def SIDEBAR_TEXT():
    return get_theme()["SIDEBAR_TEXT"]

def CHAT_TITLE_BG():
    return get_theme()["CHAT_TITLE_BG"]

def CHAT_AREA_BG():
    return get_theme()["CHAT_AREA_BG"]

def MSG_DISPLAY_BG():
    return get_theme()["MSG_DISPLAY_BG"]

def LEFT_BOX_BG():
    return get_theme()["LEFT_BOX_BG"]

def LEFT_BOX_TEXT():
    return get_theme()["LEFT_BOX_TEXT"]

def POPUP_HEADER_BG():
    return get_theme()["POPUP_HEADER_BG"]

def FRAME_BORDER():
    return get_theme()["FRAME_BORDER"]

def INPUT_BG():
    return get_theme()["INPUT_BG"]

def BTN_GREEN():
    return get_theme()["BTN_GREEN"]

def BTN_RED():
    return get_theme()["BTN_RED"]

def CAL_CHECKED_BG():
    return get_theme()["CAL_CHECKED_BG"]

def CAL_CHECKED_FG():
    return get_theme()["CAL_CHECKED_FG"]

def CAL_TODAY_BG():
    return get_theme()["CAL_TODAY_BG"]

def CAL_TODAY_FG():
    return get_theme()["CAL_TODAY_FG"]

def BINDING_LABEL_FG():
    return get_theme()["BINDING_LABEL_FG"]

def TEXT_WHITE():
    return get_theme()["TEXT_WHITE"]

def TEXT_PRIMARY():
    return get_theme()["TEXT_PRIMARY"]

# ====================== 窗口尺寸 ======================
LOGIN_W = 380
LOGIN_H = 540
REGISTER_W = 360
REGISTER_H = 480
MAIN_W = 600
MAIN_H = 900

# ====================== 字体 ======================
FONT_TITLE = ("Microsoft YaHei", 18, "bold")
FONT_SUBTITLE = ("Microsoft YaHei", 10)
FONT_NORMAL = ("Microsoft YaHei", 11)
FONT_SMALL = ("Microsoft YaHei", 9)
FONT_BTN = ("Microsoft YaHei", 12, "bold")
FONT_LOGOUT = ("Microsoft YaHei", 11, "bold")
FONT_EMOJI = ("Segoe UI Emoji", 40)

# ====================== 文件路径 ======================
USER_DB_FILE = "user_db.json"
CHAT_FILE = "chat_record.json"
MOMENTS_FILE = "moments.json"
CHECKIN_FILE = "checkin_data.json"
MOMENTS_VIDEOS_DIR = "moments_videos"
MOMENTS_PHOTOS_DIR = "moments_photos"
GROUP_FILE = "groups_data.json"
GROUP_CHAT_FILE = "group_chat.json"

# ====================== 默认用户（bcrypt 哈希，仅供首次运行） ======================
DEFAULT_USERS = {
    "123456": {
        "hash_pwd": b'$2b$12$cV8xR9w0F1N8aG7tXyKzOuJdZ7bQ5sL9mN0pR6dT',
        "nickname": "小明",
        "signature": "每一天，乐在沟通",
        "gender": "男",
        "age": "22",
        "city": "深圳",
    },
    "admin": {
        "hash_pwd": b'$2b$12$dE9sK2pQ7zR5aT8xYbN0cJdF3gH6lM4vW1eS9',
        "nickname": "管理员",
        "signature": "好好学习，天天向上",
        "gender": "男",
        "age": "25",
        "city": "北京",
    },
    "qquser": {
        "hash_pwd": b'$2b$12$fR3gT7vB9nD2zP5sC8kX0jL6hM1wQ4aE7dS2',
        "nickname": "QQ用户",
        "signature": "这个人很懒，什么都没留下",
        "gender": "女",
        "age": "20",
        "city": "上海",
    },
}