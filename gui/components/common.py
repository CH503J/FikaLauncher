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
    """
        创建一个带有标题的LabelFrame，并将其放置在指定的父容器中。

        参数:
        parent (tk.Widget): 父容器，LabelFrame将被放置在其中。
        title (str): LabelFrame的标题文本。
        row (int): LabelFrame在父容器中的行位置。

        返回值:
        ttk.LabelFrame: 创建并配置好的LabelFrame实例。
        """
    frame = ttk.LabelFrame(parent, text=title)
    frame.grid(row=row, column=0, columnspan=3, padx=10, pady=(5, 15), sticky="w")
    frame.grid_columnconfigure(1, weight=1)
    return frame
