# -*- coding: utf-8 -*-
"""QQ 桌面版 — 程序入口"""
import tkinter as tk
from login_window import QQLoginWindow

root = tk.Tk()
QQLoginWindow(root)
root.mainloop()
