import os
import tkinter as tk
from tkinter import ttk, filedialog

from config.config import ConfigManager


class SettingsPage(tk.Frame):
    def __init__(self, parent, config: ConfigManager):
        super().__init__(parent)
        self.config = config

        # 从配置读取路径并转换为反斜杠格式
        root_path = self.config.get_tarkov_root().replace("/", "\\")
        self.root_path_var = tk.StringVar(value=root_path)

        # 根目录选择按钮
        browse_button = ttk.Button(self, text="选择文件夹", command=self.select_folder)
        browse_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # 路径输入框
        self.root_entry = ttk.Entry(self, textvariable=self.root_path_var, width=50)
        self.root_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # 有效性提示标签（与按钮同一行）
        self.validation_label = ttk.Label(self, text="", foreground="red")
        self.validation_label.grid(row=0, column=2, padx=10, sticky="w")

        self.root_path_var.trace_add("write", self._on_path_change)
        self.grid_columnconfigure(1, weight=1)

        # 初始化时检查路径
        self._check_valid_root_path(root_path)

    def select_folder(self):
        folder = filedialog.askdirectory(title="选择塔科夫根目录")
        if folder:
            self.root_path_var.set(folder.replace("/", "\\"))

    def _on_path_change(self, *args):
        path = self.root_path_var.get().replace("/", "\\")
        self._check_valid_root_path(path)

    def _check_valid_root_path(self, path):
        if os.path.isdir(path):
            self.validation_label.config(text="路径有效", foreground="green")
            self.config.update_tarkov_root(path)
        else:
            self.validation_label.config(text="路径无效", foreground="red")
