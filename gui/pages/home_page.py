# home_page.py

import tkinter as tk
from tkinter import ttk
from gui.components import common
from config.config import ConfigManager


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config = ConfigManager()
        # SPT版本标题框
        spt_frame = common.create_label_frame(self, "SPT版本", row=0)

        # 服务端版本
        server_version = self.config.get_version()
        ttk.Label(spt_frame, text=f"服务端版本：{server_version}", font=("Verdana", 10)).pack(padx=10, pady=10)

        # Fika版本
        fika_version = self.config.get_fika_version()
        ttk.Label(spt_frame, text=f"Fika版本:{fika_version}", font=("Verdana", 10)).pack(padx=10, pady=10)
