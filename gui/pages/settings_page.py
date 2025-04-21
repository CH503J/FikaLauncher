# settings_page.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from config.config import ConfigManager


class SettingsPage(tk.Frame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.config = config  # 存储 config 实例
        self.root_dir_var = tk.StringVar(value=self.config.get_tarkov_root())  # 加载配置中的塔科夫根目录

        # 塔科夫根目录选择部分
        ttk.Label(self, text="选择塔科夫根目录:").pack(padx=10, pady=10)

        # 显示当前选择的根目录
        self.root_dir_label = ttk.Label(self, text="未选择根目录")
        self.root_dir_label.pack(padx=10, pady=10)

        # 选择文件夹按钮
        self.select_folder_button = ttk.Button(self, text="选择文件夹", command=self.select_folder)
        self.select_folder_button.pack(padx=10, pady=10)

    def select_folder(self):
        # 弹出选择文件夹对话框
        folder_path = filedialog.askdirectory(title="选择塔科夫根目录")
        if folder_path:
            # 更新标签显示已选择的路径
            self.root_dir_var.set(folder_path)
            self.root_dir_label.config(text=f"已选择根目录: {folder_path}")

            # 保存根目录到配置文件
            self.config.update_tarkov_root(folder_path)