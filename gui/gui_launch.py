# gui/gui_launch.py

import tkinter as tk
from tkinter import ttk
from gui.modules.home_page import HomePage
from gui.modules.launch_page import LaunchPage
from gui.modules.modify_page import ModifyPage
from gui.modules.settings_page import SettingsPage
from config.config import ConfigManager
from gui.components.common import bind_resize_event


class TarkovLauncherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("逃离塔科夫 Headless 一键启动器")

        # 初始化配置
        self.config = ConfigManager()
        default_size = self.config.get_window_size()
        self.root.geometry(default_size)

        # 设置最小尺寸（硬编码）
        self.root.minsize(600, 400)

        # 居中窗口
        self._center_window(default_size)

        # 实时监听窗口尺寸变更事件
        bind_resize_event(self.root, self.config)

        # 创建 Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # 添加各个页面
        self.home_page = HomePage(self.notebook)
        self.launch_page = LaunchPage(self.notebook)
        self.modify_page = ModifyPage(self.notebook)
        self.settings_page = SettingsPage(self.notebook, config=self.config)

        self.notebook.add(self.home_page, text="首页")
        self.notebook.add(self.launch_page, text="启动")
        self.notebook.add(self.modify_page, text="修改")
        self.notebook.add(self.settings_page, text="设置")

    def _center_window(self, size_str):
        width, height = map(int, size_str.split("x"))
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
