import os
import tkinter as tk
from tkinter import ttk, filedialog

from config.config import ConfigManager


class SettingsPage(tk.Frame):
    def __init__(self, parent, config: ConfigManager):
        super().__init__(parent)
        self.config = config

        # 从配置读取路径并转换为反斜杠格式（确保正确显示）
        root_path = self.config.get_tarkov_root().replace("/", "\\")  # 确保从配置中读取的是反斜杠路径
        self.root_path_var = tk.StringVar(value=root_path)

        self.server_path_var = tk.StringVar()
        self.headless_path_var = tk.StringVar()

        # 根目录输入部分
        browse_button = ttk.Button(self, text="选择文件夹", command=self.select_folder)
        browse_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.root_entry = ttk.Entry(self, textvariable=self.root_path_var, width=50)
        self.root_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.validation_label = ttk.Label(self, text="", foreground="red")
        self.validation_label.grid(row=1, column=1, padx=10, sticky="w")

        # 服务端路径显示（只读）
        ttk.Label(self, text="服务端路径:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.server_entry = ttk.Entry(self, textvariable=self.server_path_var, state="readonly", width=50)
        self.server_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.server_status = ttk.Label(self, text="", foreground="green")
        self.server_status.grid(row=2, column=2, padx=10, sticky="w")

        # Headless路径显示（只读）
        ttk.Label(self, text="Headless路径:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.headless_entry = ttk.Entry(self, textvariable=self.headless_path_var, state="readonly", width=50)
        self.headless_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.headless_status = ttk.Label(self, text="", foreground="green")
        self.headless_status.grid(row=3, column=2, padx=10, sticky="w")

        self.root_path_var.trace_add("write", self._on_path_change)
        self.grid_columnconfigure(1, weight=1)

        # 初始化时查找并显示服务端和 Headless 文件路径
        self._initialize_paths()

    def select_folder(self):
        folder = filedialog.askdirectory(title="选择塔科夫根目录")
        if folder:
            # 转换为反斜杠格式后设置路径
            self.root_path_var.set(folder.replace("/", "\\"))
            self._check_valid_root_path(folder)  # 检查根目录路径是否有效

    def _on_path_change(self, *args):
        # 获取路径并转化为反斜杠
        path = self.root_path_var.get().replace("/", "\\")
        self._check_valid_root_path(path)  # 检查路径是否有效

    def _check_valid_root_path(self, path):
        """检查路径下是否包含服务端和 Headless 文件"""
        if os.path.isdir(path):
            # 查找服务端文件
            server_path = os.path.normpath(os.path.join(path, "SPT.Server.exe"))
            if os.path.isfile(server_path):
                self.server_path_var.set(server_path)
                self.server_status.config(text="已找到服务端")
                self.config.update_config(server_path=server_path)
            else:
                self.server_path_var.set("")
                self.server_status.config(text="")

            # 查找 headless 文件
            headless_file = next(
                (f for f in os.listdir(path) if f.startswith("Start_headless_") and f.endswith(".ps1")), None)
            if headless_file:
                headless_path = os.path.normpath(os.path.join(path, headless_file))
                self.headless_path_var.set(headless_path)
                self.headless_status.config(text="已找到 Headless")
                self.config.update_config(headless_path=headless_path)
            else:
                self.headless_path_var.set("")
                self.headless_status.config(text="")

            # 如果根目录包含两个文件则显示有效提示
            if os.path.isfile(server_path) and headless_file:
                self.validation_label.config(text="路径有效", foreground="green")
                self.config.update_tarkov_root(path)
            else:
                self.validation_label.config(text="路径无效，请检查", foreground="red")
        else:
            self.validation_label.config(text="路径无效，请检查", foreground="red")
            self.server_path_var.set("")
            self.server_status.config(text="")
            self.headless_path_var.set("")
            self.headless_status.config(text="")

    def _initialize_paths(self):
        # 从配置中读取服务端和 Headless 路径
        server_path = self.config.get_server_path()
        headless_path = self.config.get_headless_path()

        if server_path and os.path.isfile(server_path):
            self.server_path_var.set(server_path)
            self.server_status.config(text="已找到服务端")
        else:
            self.server_path_var.set("")
            self.server_status.config(text="")

        if headless_path and os.path.isfile(headless_path):
            self.headless_path_var.set(headless_path)
            self.headless_status.config(text="已找到 Headless")
        else:
            self.headless_path_var.set("")
            self.headless_status.config(text="")
