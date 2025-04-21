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
        ttk.Label(path_frame, text="塔科夫根目录:").pack(side="left", padx=(0, 10))

        # 显示路径的标签
        self.path_label = ttk.Label(path_frame, textvariable=self.root_path_var, width=50)
        self.path_label.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # 选择文件夹按钮
        select_button = ttk.Button(path_frame, text="选择文件夹", command=self.select_folder)
        select_button.pack(side="right")

    def select_folder(self):
        folder = filedialog.askdirectory(title="选择塔科夫根目录")
        if folder:
            self.root_path_var.set(folder)
            self.config.update_tarkov_root(folder)
