# gui/pages/settings_page.py

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config.config import ConfigManager


class SettingsPage(tk.Frame):
    def __init__(self, parent, config: ConfigManager):
        super().__init__(parent)
        self.config = config  # 存储 config 实例
        self.root_path_var = tk.StringVar(value=self.config.get_tarkov_root())

        # 设置布局：文字 + 输入框 + 按钮
        ttk.Label(self, text="塔科夫根目录:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # 可输入路径框
        self.root_entry = ttk.Entry(self, textvariable=self.root_path_var, width=50)
        self.root_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # 错误提示标签（默认隐藏）
        self.validation_label = ttk.Label(self, text="", foreground="red")
        self.validation_label.grid(row=1, column=1, padx=10, sticky="w")

        # 浏览按钮
        browse_button = ttk.Button(self, text="选择文件夹", command=self.select_folder)
        browse_button.grid(row=0, column=2, padx=10, pady=10)

        # 监听路径输入变更
        self.root_path_var.trace_add("write", self._on_path_change)

        # 让右边列自动扩展（Entry 跟着窗口缩放）
        self.grid_columnconfigure(1, weight=1)

    def select_folder(self):
        folder = filedialog.askdirectory(title="选择塔科夫根目录")
        if folder:
            self.root_path_var.set(folder)  # 会自动触发路径验证和保存

    def _on_path_change(self, *args):
        path = self.root_path_var.get()
        if os.path.isdir(path):
            self.validation_label.config(text="")  # 清除提示
            self.config.update_tarkov_root(path)
        else:
            self.validation_label.config(text="路径无效，请检查", foreground="red")
