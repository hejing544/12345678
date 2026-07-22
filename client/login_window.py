# -*- coding: utf-8 -*-
"""登录窗口 UI 模块"""
import tkinter as tk
from tkinter import messagebox

from config import (
    LOGIN_W, LOGIN_H,
    HEADER_COLOR, BG_COLOR, BTN_COLOR, BTN_ACTIVE,
    INPUT_HIGHLIGHT, INPUT_BORDER, TEXT_GRAY, TEXT_BLACK,
    FONT_SMALL, FONT_SUBTITLE, FONT_NORMAL, FONT_BTN, FONT_EMOJI,
)
from theme import get_theme_mode, set_theme, toggle_theme
from user_db import get_user_info, verify_password, save_theme_preference, get_theme_preference
from register_window import RegisterWindow
from chat_window import MainWindow


class QQLoginWindow:
    def __init__(self, root):
        try:
            self.root = root
            self.root.title("QQ登录")
            self.root.resizable(False, False)
            self._center_window(LOGIN_W, LOGIN_H)
            self.account_var = tk.StringVar()
            self.password_var = tk.StringVar()
            self.remember_var = tk.IntVar(value=1)
            self.auto_login_var = tk.IntVar(value=0)

            # 恢复主题偏好
            saved_theme = get_theme_preference()
            set_theme(saved_theme)

            self._build_all()
        except Exception as e:
            messagebox.showerror("启动异常", f"登录窗口初始化失败：{str(e)}")

    def _build_all(self):
        """重建所有组件（主题切换时调用）"""
        for w in self.root.winfo_children():
            w.destroy()
        self._build_header()
        self._build_avatar()
        self._build_input_area()
        self._build_option_area()
        self._build_login_btn()
        self._build_footer()

    def _center_window(self, w, h):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_header(self):
        header = tk.Frame(self.root, bg=HEADER_COLOR(), height=140)
        header.pack(fill="x")
        header.pack_propagate(False)
        close_btn = tk.Label(header, text="✕", fg="white", bg=HEADER_COLOR(),
                             font=FONT_SMALL, cursor="hand2")
        close_btn.place(x=350, y=8)
        close_btn.bind("<Button-1>", lambda e: self.root.quit())
        tk.Label(header, text="QQ", fg="white", bg=HEADER_COLOR(),
                 font=("Microsoft YaHei", 22, "bold")).place(x=20, y=20)
        tk.Label(header, text="每一天，乐在沟通", fg="#E8F7FF", bg=HEADER_COLOR(),
                 font=FONT_SUBTITLE).place(x=22, y=60)

    def _build_avatar(self):
        avatar_frame = tk.Frame(self.root, bg=BG_COLOR(), height=90)
        avatar_frame.pack(fill="x")
        avatar_frame.pack_propagate(False)
        tk.Label(avatar_frame, text="🐧", bg=BG_COLOR(), font=FONT_EMOJI).pack(pady=15)

    def _build_input_area(self):
        input_frame = tk.Frame(self.root, bg=BG_COLOR())
        input_frame.pack(fill="x", padx=40, pady=(5, 10))
        tk.Label(input_frame, text="账号", bg=BG_COLOR(), fg=TEXT_GRAY(), font=FONT_SMALL).pack(anchor="w")
        acc_entry = tk.Entry(
            input_frame, textvariable=self.account_var, font=FONT_NORMAL,
            relief="flat", bd=0, highlightthickness=1,
            highlightcolor=INPUT_HIGHLIGHT(), highlightbackground=INPUT_BORDER()
        )
        acc_entry.pack(fill="x", ipady=6, pady=(2, 12))
        tk.Label(input_frame, text="密码", bg=BG_COLOR(), fg=TEXT_GRAY(), font=FONT_SMALL).pack(anchor="w")
        pwd_entry = tk.Entry(
            input_frame, textvariable=self.password_var, show="●", font=FONT_NORMAL,
            relief="flat", bd=0, highlightthickness=1,
            highlightcolor=INPUT_HIGHLIGHT(), highlightbackground=INPUT_BORDER()
        )
        pwd_entry.pack(fill="x", ipady=6, pady=(2, 0))
        pwd_entry.bind("<Return>", lambda e: self._login_action())

    def _build_option_area(self):
        opt_frame = tk.Frame(self.root, bg=BG_COLOR())
        opt_frame.pack(fill="x", padx=40, pady=(5, 15))
        tk.Checkbutton(
            opt_frame, text="记住密码", variable=self.remember_var, bg=BG_COLOR(),
            activebackground=BG_COLOR(), font=FONT_SMALL, fg=TEXT_GRAY(),
            selectcolor=BG_COLOR(), bd=0
        ).pack(side="left")
        tk.Checkbutton(
            opt_frame, text="自动登录", variable=self.auto_login_var, bg=BG_COLOR(),
            activebackground=BG_COLOR(), font=FONT_SMALL, fg=TEXT_GRAY(),
            selectcolor=BG_COLOR(), bd=0
        ).pack(side="right")

    def _build_login_btn(self):
        tk.Button(
            self.root, text="登 录", command=self._login_action,
            bg=BTN_COLOR(), fg="white", activebackground=BTN_ACTIVE(), activeforeground="white",
            font=FONT_BTN, relief="flat", cursor="hand2", bd=0
        ).pack(fill="x", padx=40, ipady=8)

    def _build_footer(self):
        footer = tk.Frame(self.root, bg=BG_COLOR())
        footer.pack(fill="x", padx=40, pady=15)
        reg_label = tk.Label(footer, text="注册账号", fg=HEADER_COLOR(), bg=BG_COLOR(),
                             font=FONT_SMALL, cursor="hand2")
        reg_label.pack(side="left")
        reg_label.bind("<Button-1>", lambda e: RegisterWindow(self.root))

        # 主题切换按钮
        mode = get_theme_mode()
        theme_text = "🌙 夜间" if mode == "day" else "☀️ 日间"
        self.theme_btn = tk.Label(footer, text=theme_text, fg=HEADER_COLOR(), bg=BG_COLOR(),
                                  font=FONT_SMALL, cursor="hand2")
        self.theme_btn.pack(side="right", padx=(0, 10))
        self.theme_btn.bind("<Button-1>", lambda e: self._toggle_theme())

        forget_label = tk.Label(footer, text="找回密码", fg=HEADER_COLOR(), bg=BG_COLOR(),
                                font=FONT_SMALL, cursor="hand2")
        forget_label.pack(side="right")
        forget_label.bind("<Button-1>", lambda e: messagebox.showinfo("提示", "找回密码功能待开发"))

    def _toggle_theme(self):
        new_mode = toggle_theme()
        self.theme_btn.config(text="🌙 夜间" if new_mode == "day" else "☀️ 日间")
        save_theme_preference(new_mode)
        self._build_all()

    def _login_action(self):
        try:
            account = self.account_var.get().strip()
            raw_pwd = self.password_var.get().strip()
            if not account:
                messagebox.showwarning("输入提示", "请填写账号！")
                return
            if not raw_pwd:
                messagebox.showwarning("输入提示", "请填写密码！")
                return
            user_data = get_user_info(account)
            if user_data is None:
                messagebox.showerror("登录失败", "该账号不存在，请先注册！")
                return
            if not verify_password(raw_pwd, user_data["hash_pwd"]):
                messagebox.showerror("登录失败", "账号或密码错误！")
                return
            messagebox.showinfo("登录成功", f"欢迎 {user_data['nickname']}！正在进入主页")
            self.root.destroy()
            main_root = tk.Tk()
            MainWindow(main_root, account, user_data)
            main_root.mainloop()
        except Exception as err:
            messagebox.showerror("登录异常", f"程序出错：{str(err)}")


def run_login_window():
    """启动登录窗口（供 chat_window 退出登录时调用）"""
    root = tk.Tk()
    QQLoginWindow(root)
    root.mainloop()