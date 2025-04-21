# gui/pages/settings_page.py

import tkinter as tk
from tkinter import ttk, filedialog


class SettingsPage(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.config = config

        self.root_path_var = tk.StringVar(value=self.config.get_tarkov_root())

        # 根目录区域框架
        path_frame = ttk.Frame(self)
        path_frame.pack(padx=20, pady=20, fill="x")

        # 根目录说明文字
        ttk.Label(path_frame, text="根目录:").pack(side="left", padx=(0, 10))

        # 路径输入框（可手动编辑）
        self.path_entry = ttk.Entry(path_frame, textvariable=self.root_path_var, width=50)
        self.path_entry.pack(side="left", fill="x", expand=True)

        # 输入框内容变动监听，实时保存配置
        self.root_path_var.trace_add("write", self._on_path_change)

        # 独立按钮：弹出文件夹选择对话框
        select_button = ttk.Button(path_frame, text="浏览", command=self.select_folder)
        select_button.pack(side="right")

    def select_folder(self):
        folder = filedialog.askdirectory(title="塔科夫根目录")
        if folder:
            self.root_path_var.set(folder)  # 触发 trace 保存配置

    def _on_path_change(self, *args):
        self.config.update_tarkov_root(self.root_path_var.get())
