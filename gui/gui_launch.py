import sys
import os
import tkinter as tk
from tkinter import ttk
from gui.pages.home_page import HomePage
from gui.pages.launch_page import LaunchPage
from gui.pages.modify_page import ModifyPage
from gui.pages.settings_page import SettingsPage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'gui_launch.py')))


class TarkovLauncherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("逃离塔科夫 Headless 一键启动器")

        # 创建一个 Notebook（标签页）
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # 创建各个页面
        self.home_page = HomePage(self.notebook)
        self.launch_page = LaunchPage(self.notebook)
        self.modify_page = ModifyPage(self.notebook)
        self.settings_page = SettingsPage(self.notebook)

        # 将页面添加到 Notebook
        self.notebook.add(self.home_page, text="首页")
        self.notebook.add(self.launch_page, text="启动")
        self.notebook.add(self.modify_page, text="修改")
        self.notebook.add(self.settings_page, text="设置")
