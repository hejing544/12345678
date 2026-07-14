# -*- coding: utf-8 -*-
"""群系统数据层 — 群数据、群聊记录存储与管理"""
import json
import os
from datetime import datetime

from config import GROUP_FILE, GROUP_CHAT_FILE


def load_groups_data() -> dict:
    """加载所有群数据"""
    if os.path.exists(GROUP_FILE):
        with open(GROUP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_groups_data(data: dict):
    """保存所有群数据"""
    with open(GROUP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_group_chat_data() -> dict:
    """加载群聊天记录"""
    if os.path.exists(GROUP_CHAT_FILE):
        with open(GROUP_CHAT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_group_chat_data(data: dict):
    """保存群聊天记录"""
    with open(GROUP_CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _generate_group_id(data: dict) -> str:
    """生成下一个群号 G001、G002……"""
    existing = list(data.keys())
    if not existing:
        return "G001"
    nums = []
    for gid in existing:
        try:
            nums.append(int(gid[1:]))
        except (ValueError, IndexError):
            nums.append(0)
    return f"G{max(nums) + 1:03d}"


def create_group(creator_account: str, creator_nickname: str, group_name: str) -> dict:
    """创建群，返回群信息 dict，失败返回空 dict"""
    if not group_name.strip():
        return {}
    data = load_groups_data()
    gid = _generate_group_id(data)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    group_info = {
        "group_id": gid,
        "group_name": group_name.strip(),
        "creator": creator_account,
        "members": [
            {"account": creator_account, "nickname": creator_nickname, "role": "owner", "join_time": now}
        ],
        "pending_join": [],  # [{"from_account": ..., "from_nickname": ..., "time": ...}]
        "created_time": now,
    }
    data[gid] = group_info
    save_groups_data(data)
    return {"group_id": gid, "group_name": group_info["group_name"]}


def get_my_groups(account: str) -> list:
    """获取用户加入的所有群，返回 [{'group_id':..., 'group_name':..., 'member_count':..., 'owner':...}, ...]"""
    data = load_groups_data()
    result = []
    for gid, info in data.items():
        for m in info.get("members", []):
            if m["account"] == account:
                result.append({
                    "group_id": gid,
                    "group_name": info.get("group_name", "未命名群"),
                    "member_count": len(info.get("members", [])),
                    "owner": info.get("creator", ""),
                })
                break
    return result


def search_groups(keyword: str) -> list:
    """搜索群，按群号或群名匹配，返回 [{'group_id':..., 'group_name':..., 'member_count':...}, ...]"""
    data = load_groups_data()
    results = []
    kw = keyword.lower()
    for gid, info in data.items():
        if kw in gid.lower() or kw in info.get("group_name", "").lower():
            results.append({
                "group_id": gid,
                "group_name": info.get("group_name", "未命名群"),
                "member_count": len(info.get("members", [])),
                "owner": info.get("creator", ""),
            })
    return results


def get_group_info(group_id: str) -> dict:
    """获取单个群信息"""
    data = load_groups_data()
    return data.get(group_id, {})


def get_group_members(group_id: str) -> list:
    """获取群成员列表"""
    info = get_group_info(group_id)
    return info.get("members", [])


def is_group_member(account: str, group_id: str) -> bool:
    """检查用户是否在群中"""
    members = get_group_members(group_id)
    for m in members:
        if m["account"] == account:
            return True
    return False


def send_join_request(from_account: str, from_nickname: str, group_id: str) -> str:
    """申请加群，返回 'ok' / 'already_member' / 'already_requested' / 'not_found'"""
    data = load_groups_data()
    if group_id not in data:
        return "not_found"

    group = data[group_id]
    # 检查是否已是成员
    for m in group.get("members", []):
        if m["account"] == from_account:
            return "already_member"

    # 检查是否已申请过
    for r in group.get("pending_join", []):
        if r["from_account"] == from_account:
            return "already_requested"

    group["pending_join"].append({
        "from_account": from_account,
        "from_nickname": from_nickname,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    save_groups_data(data)
    return "ok"


def get_pending_join_requests(group_id: str) -> list:
    """获取群入群申请列表"""
    info = get_group_info(group_id)
    return info.get("pending_join", [])


def accept_join_request(group_id: str, from_account: str, from_nickname: str, admin_account: str) -> bool:
    """同意入群申请"""
    data = load_groups_data()
    if group_id not in data:
        return False
    group = data[group_id]

    # 验证操作者是群主或管理员
    admin_role = None
    for m in group.get("members", []):
        if m["account"] == admin_account:
            admin_role = m.get("role", "member")
            break
    if admin_role not in ("owner", "admin"):
        return False

    # 移除申请
    new_pending = [r for r in group.get("pending_join", []) if r["from_account"] != from_account]
    group["pending_join"] = new_pending

    # 添加成员
    members = group.get("members", [])
    if from_account not in [m["account"] for m in members]:
        members.append({
            "account": from_account,
            "nickname": from_nickname,
            "role": "member",
            "join_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    group["members"] = members
    save_groups_data(data)
    return True


def reject_join_request(group_id: str, from_account: str) -> bool:
    """拒绝入群申请"""
    data = load_groups_data()
    if group_id not in data:
        return False
    group = data[group_id]
    old_count = len(group.get("pending_join", []))
    group["pending_join"] = [r for r in group["pending_join"] if r["from_account"] != from_account]
    if len(group["pending_join"]) == old_count:
        return False
    save_groups_data(data)
    return True


def remove_group_member(group_id: str, target_account: str, admin_account: str) -> bool:
    """踢出群成员（群主/管理员操作），不能踢自己"""
    if target_account == admin_account:
        return False
    data = load_groups_data()
    if group_id not in data:
        return False
    group = data[group_id]

    # 验证操作者身份
    admin_role = None
    for m in group.get("members", []):
        if m["account"] == admin_account:
            admin_role = m.get("role", "member")
            break
    if admin_role not in ("owner", "admin"):
        return False

    # 不能踢群主
    target_role = None
    for m in group.get("members", []):
        if m["account"] == target_account:
            target_role = m.get("role", "")
            break
    if target_role == "owner":
        return False

    new_members = [m for m in group["members"] if m["account"] != target_account]
    if len(new_members) == len(group["members"]):
        return False
    group["members"] = new_members
    save_groups_data(data)
    return True


def assign_admin(group_id: str, target_account: str, admin_account: str) -> bool:
    """设置/取消管理员（仅群主可操作）"""
    data = load_groups_data()
    if group_id not in data:
        return False
    group = data[group_id]
    if group.get("creator") != admin_account:
        return False

    target_found = False
    owner_found = False
    for m in group["members"]:
        if m["account"] == target_account:
            # 如果当前是 admin 就降为 member，否则升为 admin
            m["role"] = "member" if m.get("role") == "admin" else "admin"
            target_found = True
        if m["account"] == admin_account and m.get("role") == "owner":
            owner_found = True

    if not (target_found and owner_found):
        return False
    save_groups_data(data)
    return True


def transfer_owner(group_id: str, new_owner_account: str, old_owner_account: str) -> bool:
    """转让群主（仅原群主可操作）"""
    data = load_groups_data()
    if group_id not in data:
        return False
    group = data[group_id]
    if group.get("creator") != old_owner_account:
        return False

    new_owner_found = False
    old_owner_found = False
    for m in group["members"]:
        if m["account"] == new_owner_account:
            m["role"] = "owner"
            new_owner_found = True
        if m["account"] == old_owner_account:
            m["role"] = "admin"
            old_owner_found = True

    if new_owner_found and old_owner_found:
        group["creator"] = new_owner_account
        save_groups_data(data)
        return True
    return False


def disband_group(group_id: str, account: str) -> bool:
    """解散群（仅群主可操作）"""
    data = load_groups_data()
    if group_id not in data:
        return False
    group = data[group_id]
    if group.get("creator") != account:
        return False
    del data[group_id]
    save_groups_data(data)

    # 同时删除群聊天记录
    chat_data = load_group_chat_data()
    if group_id in chat_data:
        del chat_data[group_id]
        save_group_chat_data(chat_data)
    return True


def send_group_message(sender_account: str, sender_nickname: str, group_id: str, content: str) -> dict:
    """发送群消息，返回消息 dict"""
    msg = {
        "sender_account": sender_account,
        "sender_nickname": sender_nickname,
        "content": content,
        "time": datetime.now().strftime("%H:%M"),
    }
    chat_data = load_group_chat_data()
    if group_id not in chat_data:
        chat_data[group_id] = []
    chat_data[group_id].append(msg)
    save_group_chat_data(chat_data)
    return msg


def load_group_conversation(group_id: str) -> list:
    """加载群聊天记录"""
    chat_data = load_group_chat_data()
    return chat_data.get(group_id, [])