# gui/components/common.py

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
