# gui_launch.py

import sys
import os
import tkinter as tk
from tkinter import ttk
from gui.pages.home_page import HomePage
from gui.pages.launch_page import LaunchPage
from gui.pages.modify_page import ModifyPage
from gui.pages.settings_page import SettingsPage
from config.config import ConfigManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'gui_launch.py')))


class TarkovLauncherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("逃离塔科夫 Headless 一键启动器")

        # 初始化配置
        self.config = ConfigManager()
        self.root.geometry(self.config.get_window_size())

        self.root.minsize(600, 400)

        # 窗口关闭事件绑定（保存窗口大小）
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # 创建 Notebook（标签页）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # 各页面
        self.home_page = HomePage(self.notebook)
        self.launch_page = LaunchPage(self.notebook)
        self.modify_page = ModifyPage(self.notebook)
        self.settings_page = SettingsPage(self.notebook, config=self.config)

        self.notebook.add(self.home_page, text="首页")
        self.notebook.add(self.launch_page, text="启动")
        self.notebook.add(self.modify_page, text="修改")
        self.notebook.add(self.settings_page, text="设置")

        # 初始化配置
        self.config = ConfigManager()
        size = self.config.get_window_size()
        self.root.geometry(size)

        # 窗口居中显示
        self._center_window(size)

    def on_close(self):
        # 保存当前窗口大小
        geometry = self.root.winfo_geometry().split("+")[0]  # "700x600"
        self.config.update_config(window_size=geometry)
        self.root.destroy()

    def _center_window(self, size):
        width, height = map(int, size.split("x"))
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
