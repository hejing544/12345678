# -*- coding: utf-8 -*-
"""注册窗口 UI 模块"""
import tkinter as tk
from tkinter import messagebox

from config import (
    REGISTER_W, REGISTER_H,
    HEADER_COLOR, BG_COLOR, BTN_COLOR, BTN_ACTIVE,
    INPUT_HIGHLIGHT, INPUT_BORDER, TEXT_GRAY,
    FONT_TITLE, FONT_SMALL, FONT_NORMAL, FONT_BTN,
)
from user_db import account_exists, create_user


class RegisterWindow:
    def __init__(self, parent_root):
        try:
            self.top = tk.Toplevel(parent_root)
            self.parent = parent_root
            self.top.title("注册QQ账号")
            self.top.resizable(False, False)
            self._center_window(REGISTER_W, REGISTER_H)
            self.top.transient(parent_root)
            self.top.grab_set()
            self.reg_account_var = tk.StringVar()
            self.reg_nickname_var = tk.StringVar()
            self.reg_password_var = tk.StringVar()
            self.reg_confirm_var = tk.StringVar()
            self._build_header()
            self._build_form()
            self._build_register_btn()
        except Exception as e:
            messagebox.showerror("窗口异常", f"注册窗口初始化失败：{str(e)}")

    def _center_window(self, w, h):
        screen_w = self.top.winfo_screenwidth()
        screen_h = self.top.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.top.geometry(f"{w}x{h}+{x}+{y}")

    def _build_header(self):
        header = tk.Frame(self.top, bg=HEADER_COLOR(), height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="注册QQ账号", fg="white", bg=HEADER_COLOR(), font=FONT_TITLE).pack(pady=30)

    def _create_input_row(self, parent_frame, label_text, var, show=""):
        row = tk.Frame(parent_frame, bg=BG_COLOR())
        row.pack(fill="x", pady=(0, 10))
        tk.Label(row, text=label_text, bg=BG_COLOR(), fg=TEXT_GRAY(), font=FONT_SMALL).pack(anchor="w")
        entry = tk.Entry(
            row, textvariable=var, show=show, font=FONT_NORMAL,
            relief="flat", bd=0, highlightthickness=1,
            highlightcolor=INPUT_HIGHLIGHT(), highlightbackground=INPUT_BORDER()
        )
        entry.pack(fill="x", ipady=6, pady=(2, 0))

    def _build_form(self):
        form = tk.Frame(self.top, bg=BG_COLOR())
        form.pack(fill="x", padx=40, pady=(15, 10))
        self._create_input_row(form, "账号", self.reg_account_var)
        self._create_input_row(form, "昵称", self.reg_nickname_var)
        self._create_input_row(form, "密码（6-16位）", self.reg_password_var, show="●")
        confirm_frame = tk.Frame(form, bg=BG_COLOR())
        confirm_frame.pack(fill="x")
        tk.Label(confirm_frame, text="确认密码", bg=BG_COLOR(), fg=TEXT_GRAY(), font=FONT_SMALL).pack(anchor="w")
        confirm_entry = tk.Entry(
            confirm_frame, textvariable=self.reg_confirm_var, show="●", font=FONT_NORMAL,
            relief="flat", bd=0, highlightthickness=1,
            highlightcolor=INPUT_HIGHLIGHT(), highlightbackground=INPUT_BORDER()
        )
        confirm_entry.pack(fill="x", ipady=6, pady=(2, 0))
        confirm_entry.bind("<Return>", lambda e: self._on_register())

    def _build_register_btn(self):
        tk.Button(
            self.top, text="立即注册", command=self._on_register,
            bg=BTN_COLOR(), fg="white", activebackground=BTN_ACTIVE(), activeforeground="white",
            font=FONT_BTN, relief="flat", cursor="hand2", bd=0
        ).pack(fill="x", padx=40, ipady=8, pady=(5, 0))

    def _on_register(self):
        try:
            account = self.reg_account_var.get().strip()
            nickname = self.reg_nickname_var.get().strip()
            pwd = self.reg_password_var.get().strip()
            confirm_pwd = self.reg_confirm_var.get().strip()
            if not account:
                messagebox.showwarning("提示", "请输入账号！", parent=self.top)
                return
            if not nickname:
                messagebox.showwarning("提示", "请输入昵称！", parent=self.top)
                return
            if not pwd:
                messagebox.showwarning("提示", "请输入密码！", parent=self.top)
                return
            if not confirm_pwd:
                messagebox.showwarning("提示", "请再次输入密码！", parent=self.top)
                return
            if not account.isalnum() or not (3 <= len(account) <= 16):
                messagebox.showwarning("格式错误", "账号仅支持字母/数字，长度3~16位", parent=self.top)
                return
            if not (6 <= len(pwd) <= 16):
                messagebox.showwarning("格式错误", "密码长度必须6~16位", parent=self.top)
                return
            if pwd != confirm_pwd:
                messagebox.showerror("错误", "两次输入密码不一致", parent=self.top)
                return
            if account_exists(account):
                messagebox.showerror("错误", f"账号 {account} 已被注册", parent=self.top)
                return
            create_user(account, nickname, pwd)
            messagebox.showinfo("注册成功", f"账号 {account} 注册完成，可返回登录！", parent=self.top)
            self.top.destroy()
        except Exception as err:
            messagebox.showerror("注册失败", f"程序异常：{str(err)}", parent=self.top)