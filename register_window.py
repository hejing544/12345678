# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from user_db import user_exists, add_user

class RegisterWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title('QQ注册')
        self.width = 400
        self.height = 500
        self._center_window(self.width, self.height)
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.bg_color = '#F5F6FA'
        self.header_color = '#12B7F5'
        self.btn_color = '#12B7F5'
        self.btn_active = '#0E9BD6'
        
        self._build_ui()
    
    def _center_window(self, w, h):
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2
        self.window.geometry(f'{w}x{h}+{x}+{y}')
    
    def _build_ui(self):
        # 头部
        header = tk.Frame(self.window, bg=self.header_color, height=120)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        close_btn = tk.Label(header, text='X', fg='white', bg=self.header_color, 
                           font=('Microsoft YaHei', 12, 'bold'), cursor='hand2')
        close_btn.place(x=370, y=8)
        close_btn.bind('<Button-1>', lambda e: self.window.destroy())
        
        title = tk.Label(header, text='QQ注册', fg='white', bg=self.header_color,
                        font=('Microsoft YaHei', 20, 'bold'))
        title.place(x=20, y=20)
        
        subtitle = tk.Label(header, text='创建您的QQ账号', fg='#E8F7FF', bg=self.header_color,
                           font=('Microsoft YaHei', 10))
        subtitle.place(x=22, y=60)
        
        # 输入区域
        input_frame = tk.Frame(self.window, bg=self.bg_color)
        input_frame.pack(fill='x', padx=40, pady=20)
        
        # 账号
        tk.Label(input_frame, text='账号', bg=self.bg_color, fg='#666666',
                font=('Microsoft YaHei', 9)).pack(anchor='w')
        self.account_var = tk.StringVar()
        account_entry = tk.Entry(input_frame, textvariable=self.account_var,
                               font=('Microsoft YaHei', 11), relief='flat', bd=0,
                               highlightthickness=1, highlightcolor=self.header_color,
                               highlightbackground='#DDDDDD')
        account_entry.pack(fill='x', ipady=6, pady=(2, 12))
        
        # 昵称
        tk.Label(input_frame, text='昵称', bg=self.bg_color, fg='#666666',
                font=('Microsoft YaHei', 9)).pack(anchor='w')
        self.nickname_var = tk.StringVar()
        nickname_entry = tk.Entry(input_frame, textvariable=self.nickname_var,
                                font=('Microsoft YaHei', 11), relief='flat', bd=0,
                                highlightthickness=1, highlightcolor=self.header_color,
                                highlightbackground='#DDDDDD')
        nickname_entry.pack(fill='x', ipady=6, pady=(2, 12))
        
        # 密码
        tk.Label(input_frame, text='密码', bg=self.bg_color, fg='#666666',
                font=('Microsoft YaHei', 9)).pack(anchor='w')
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(input_frame, textvariable=self.password_var, show='*',
                                font=('Microsoft YaHei', 11), relief='flat', bd=0,
                                highlightthickness=1, highlightcolor=self.header_color,
                                highlightbackground='#DDDDDD')
        password_entry.pack(fill='x', ipady=6, pady=(2, 12))
        
        # 确认密码
        tk.Label(input_frame, text='确认密码', bg=self.bg_color, fg='#666666',
                font=('Microsoft YaHei', 9)).pack(anchor='w')
        self.confirm_var = tk.StringVar()
        confirm_entry = tk.Entry(input_frame, textvariable=self.confirm_var, show='*',
                               font=('Microsoft YaHei', 11), relief='flat', bd=0,
                               highlightthickness=1, highlightcolor=self.header_color,
                               highlightbackground='#DDDDDD')
        confirm_entry.pack(fill='x', ipady=6, pady=(2, 0))
        confirm_entry.bind('<Return>', lambda e: self._on_register())
        
        # 注册按钮
        register_btn = tk.Button(self.window, text='注 册', command=self._on_register,
                               bg=self.btn_color, fg='white',
                               activebackground=self.btn_active, activeforeground='white',
                               font=('Microsoft YaHei', 12, 'bold'), relief='flat',
                               cursor='hand2', bd=0)
        register_btn.pack(fill='x', padx=40, ipady=8, pady=10)
        
        # 返回登录
        back_label = tk.Label(self.window, text='返回登录', fg=self.header_color,
                            bg=self.bg_color, font=('Microsoft YaHei', 9),
                            cursor='hand2')
        back_label.pack(pady=10)
        back_label.bind('<Button-1>', lambda e: self.window.destroy())
    
    def _on_register(self):
        account = self.account_var.get().strip()
        nickname = self.nickname_var.get().strip()
        password = self.password_var.get().strip()
        confirm = self.confirm_var.get().strip()
        
        if not account:
            messagebox.showwarning('提示', '请输入账号！')
            return
        if not nickname:
            messagebox.showwarning('提示', '请输入昵称！')
            return
        if not password:
            messagebox.showwarning('提示', '请输入密码！')
            return
        if not confirm:
            messagebox.showwarning('提示', '请确认密码！')
            return
        if password != confirm:
            messagebox.showwarning('提示', '两次密码输入不一致！')
            return
        if user_exists(account):
            messagebox.showwarning('提示', '该账号已存在！')
            return
        
        add_user(account, password, nickname)
        messagebox.showinfo('注册成功', f'注册成功！\n账号：{account}\n昵称：{nickname}')
        self.window.destroy()