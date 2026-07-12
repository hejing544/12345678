# -*- coding: utf-8 -*-
"""好友系统数据层 — 好友列表、好友请求存储"""
import json
import os
from datetime import datetime

FRIENDS_FILE = "friends_data.json"


def _load_friends_data() -> dict:
    """加载所有好友数据"""
    if os.path.exists(FRIENDS_FILE):
        with open(FRIENDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_friends_data(data: dict):
    """保存所有好友数据"""
    with open(FRIENDS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_friend_list(account: str) -> list:
    """获取用户的好友列表，返回 [{'account':..., 'nickname':...}, ...]"""
    data = _load_friends_data()
    return data.get(account, {}).get("friends", [])


def get_pending_requests(account: str) -> list:
    """获取待处理的好友请求，返回 [{'from_account':..., 'from_nickname':..., 'time':...}, ...]"""
    data = _load_friends_data()
    return data.get(account, {}).get("pending", [])


def send_friend_request(from_account: str, from_nickname: str, to_account: str) -> bool:
    """发送好友请求，如果已存在请求或已是好友返回 False"""
    if from_account == to_account:
        return False

    data = _load_friends_data()

    # 检查是否已是好友
    my_friends = data.get(from_account, {}).get("friends", [])
    for f in my_friends:
        if f["account"] == to_account:
            return False

    # 检查是否已经发过请求
    target_pending = data.get(to_account, {}).get("pending", [])
    for r in target_pending:
        if r["from_account"] == from_account:
            return False

    # 添加请求
    if to_account not in data:
        data[to_account] = {"friends": [], "pending": []}

    data[to_account]["pending"].append({
        "from_account": from_account,
        "from_nickname": from_nickname,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    _save_friends_data(data)
    return True


def accept_friend_request(account: str, from_account: str, from_nickname: str, my_nickname: str) -> bool:
    """接受好友请求"""
    data = _load_friends_data()

    # 从 pending 列表中移除
    if account not in data:
        return False
    new_pending = [r for r in data[account]["pending"] if r["from_account"] != from_account]
    data[account]["pending"] = new_pending

    # 双方添加好友
    if account not in data:
        data[account] = {"friends": [], "pending": []}
    if from_account not in data:
        data[from_account] = {"friends": [], "pending": []}

    # 避免重复添加
    if from_account not in [f["account"] for f in data[account]["friends"]]:
        data[account]["friends"].append({"account": from_account, "nickname": from_nickname})
    if account not in [f["account"] for f in data[from_account]["friends"]]:
        data[from_account]["friends"].append({"account": account, "nickname": my_nickname})

    _save_friends_data(data)
    return True


def reject_friend_request(account: str, from_account: str) -> bool:
    """拒绝好友请求"""
    data = _load_friends_data()
    if account not in data:
        return False
    old_count = len(data[account]["pending"])
    data[account]["pending"] = [r for r in data[account]["pending"] if r["from_account"] != from_account]
    if len(data[account]["pending"]) == old_count:
        return False
    _save_friends_data(data)
    return True


def remove_friend(account: str, friend_account: str) -> bool:
    """删除好友"""
    data = _load_friends_data()

    removed = False
    # 从自己的好友列表移除
    if account in data:
        new_friends = [f for f in data[account]["friends"] if f["account"] != friend_account]
        if len(new_friends) < len(data[account]["friends"]):
            removed = True
        data[account]["friends"] = new_friends

    # 从对方的好友列表移除
    if friend_account in data:
        new_friends = [f for f in data[friend_account]["friends"] if f["account"] != account]
        data[friend_account]["friends"] = new_friends

    if removed:
        _save_friends_data(data)
    return removed


def search_users(keyword: str) -> list:
    """搜索用户，返回匹配的 [{'account':..., 'nickname':...}, ...]"""
    from user_db import USER_DB
    results = []
    for acc, info in USER_DB.items():
        if keyword.lower() in acc.lower() or keyword.lower() in info.get("nickname", "").lower():
            results.append({"account": acc, "nickname": info.get("nickname", acc)})
    return results