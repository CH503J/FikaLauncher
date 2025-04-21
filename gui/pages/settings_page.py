import os
import tkinter as tk
from tkinter import ttk, filedialog

from config.config import ConfigManager


class SettingsPage(tk.Frame):
    def __init__(self, parent, config: ConfigManager):
        super().__init__(parent)
        self.config = config  # 存储 config 实例
        self.root_path_var = tk.StringVar(value=self.config.get_tarkov_root())

        # 原"塔科夫根目录"改为选择按钮
        select_button = ttk.Button(self, text="游戏根目录", command=self.select_folder)
        select_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # 可输入路径框
        self.root_entry = ttk.Entry(self, textvariable=self.root_path_var, width=50)
        self.root_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # 路径无效提示（移至同一行原按钮位置）
        self.validation_label = ttk.Label(self, text="", foreground="red")
        self.validation_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # 监听路径输入变更
        self.root_path_var.trace_add("write", self._on_path_change)

        # Entry 可自适应拉伸
        self.grid_columnconfigure(1, weight=1)

    def select_folder(self):
        folder = filedialog.askdirectory(title="选择塔科夫根目录")
        if folder:
            self.root_path_var.set(folder)

    def _on_path_change(self, *args):
        path = self.root_path_var.get()
        if os.path.isdir(path):
            self.validation_label.config(text="路径有效", foreground="green")
            self.config.update_tarkov_root(path)
        else:
            self.validation_label.config(text="路径无效", foreground="red")
