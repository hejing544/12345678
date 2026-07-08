# -*- coding: utf-8 -*-
"""聊天记录持久化层 — JSON 文件读写"""
import json
import os

from config import CHAT_FILE


def load_chat_data():
    """从本地文件读取聊天记录，文件不存在返回空字典"""
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_chat_data(chat_dict):
    """将聊天记录保存到本地 JSON 文件"""
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(chat_dict, f, ensure_ascii=False, indent=2)
