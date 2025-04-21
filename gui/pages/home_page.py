# home_page.py

import tkinter as tk
from tkinter import ttk


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="首页内容").pack(padx=10, pady=10)
