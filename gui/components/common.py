# gui/components/common.py

from tkinter import ttk
import tkinter as tk


def bind_resize_event(widget, config_manager):
    """
    给指定 widget（如 root）绑定窗口大小改变事件，并将新尺寸写入 config.ini
    """

    def on_resize(event):
        width = widget.winfo_width()
        height = widget.winfo_height()
        size_str = f"{width}x{height}"
        config_manager.update_config(window_size=size_str)

    widget.bind("<Configure>", on_resize)


def create_label_frame(parent, title: str, row: int) -> ttk.LabelFrame:
    frame = ttk.LabelFrame(parent, text=title)
    frame.grid(row=row, column=0, columnspan=3, padx=10, pady=(5, 15), sticky="w")
    frame.grid_columnconfigure(1, weight=1)
    return frame


def add_path_row(parent, row, label_text, key, initial_value=""):
    var = tk.StringVar(value=initial_value)
    setattr(parent, f"{key}_path_var", var)

    ttk.Label(parent, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="w")
    entry = ttk.Entry(parent, textvariable=var, state="readonly", width=50)
    entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
    status = ttk.Label(parent, text="", foreground="green")
    status.grid(row=row, column=2, padx=10, sticky="w")

    setattr(parent, f"{key}_entry", entry)
    setattr(parent, f"{key}_status", status)

