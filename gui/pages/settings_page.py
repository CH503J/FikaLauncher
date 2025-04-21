import tkinter as tk
from tkinter import ttk


class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="设置页面内容").pack(padx=10, pady=10)
