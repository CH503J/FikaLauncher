import os
import tkinter as tk
from tkinter import ttk, filedialog

from config.config import ConfigManager


class SettingsPage(tk.Frame):
    def __init__(self, parent, config: ConfigManager):
        super().__init__(parent)
        self.config = config

        root_path = self.config.get_tarkov_root().replace("/", "\\")
        self.root_path_var = tk.StringVar(value=root_path)

        # 根目录选择部分
        browse_button = ttk.Button(self, text="选择文件夹", command=self.select_folder)
        browse_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.root_entry = ttk.Entry(self, textvariable=self.root_path_var, width=50)
        self.root_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.validation_label = ttk.Label(self, text="", foreground="red")
        self.validation_label.grid(row=0, column=2, padx=10, sticky="w")

        # 添加标题 SPT
        # title_label = ttk.Label(self, text="AKI-SPT", font=("Segoe UI", 12, "bold"))
        # title_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(5, 15), sticky="w")

        # 创建LabelFrame容器
        spt_frame = ttk.LabelFrame(self, text="AKI-SPT")
        spt_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(5, 15), sticky="w")
        spt_frame.grid_columnconfigure(1, weight=1)

        # EscapeFromTarkov.exe路径
        ttk.Label(spt_frame, text="主程序(EscapeFromTarkov)").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.client_path_var = tk.StringVar()
        self.client_entry = ttk.Entry(spt_frame, textvariable=self.client_path_var, state="readonly", width=50)
        self.client_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.client_status = ttk.Label(spt_frame, text="", foreground="green")
        self.client_status.grid(row=2, column=2, padx=10, sticky="w")

        # SPT.Server.exe路径
        ttk.Label(spt_frame, text="服务端(SPT.Server)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.server_path_var = tk.StringVar()
        self.server_path_var = ttk.Entry(spt_frame, textvariable=self.client_path_var, state="readonly", width=50)
        self.server_path_var.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.server_path_var = ttk.Label(spt_frame, text="", foreground="green")
        self.server_path_var.grid(row=3, column=2, padx=10, sticky="w")

        # SPT.Launcher.exe路径
        ttk.Label(spt_frame, text="启动器(SPT.Launcher)").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.launcher_path_var = tk.StringVar()
        self.launcher_path_var = ttk.Entry(spt_frame, textvariable=self.client_path_var, state="readonly", width=50)
        self.launcher_path_var.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.launcher_path_var = ttk.Label(spt_frame, text="", foreground="green")
        self.launcher_path_var.grid(row=4, column=2, padx=10, sticky="w")

        # 添加标题 Fika
        # title_label = ttk.Label(self, text="Fika", font=("Segoe UI", 12, "bold"))
        # title_label.grid(row=5, column=0, columnspan=3, padx=10, pady=(5, 15), sticky="w")
        fika_frame = ttk.LabelFrame(self, text="Fika")
        fika_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=(5, 15), sticky="w")
        fika_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(fika_frame, text="FikaCore").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.fika_core_path_var = tk.StringVar()
        self.fika_core_path_var = ttk.Entry(fika_frame, textvariable=self.client_path_var, state="readonly", width=50)
        self.fika_core_path_var.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.fika_core_path_var = ttk.Label(fika_frame, text="", foreground="green")
        self.fika_core_path_var.grid(row=1, column=2, padx=10, sticky="w")

        ttk.Label(fika_frame, text="FikaHeadless").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.fika_headless_path_var = tk.StringVar()
        self.fika_headless_path_var = ttk.Entry(fika_frame, textvariable=self.client_path_var, state="readonly", width=50)
        self.fika_headless_path_var.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.fika_headless_path_var = ttk.Label(fika_frame, text="", foreground="green")
        self.fika_headless_path_var.grid(row=2, column=2, padx=10, sticky="w")

        ttk.Label(fika_frame, text="FikaServer").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.fika_server_path_var = tk.StringVar()
        self.fika_server_path_var = ttk.Entry(fika_frame, textvariable=self.client_path_var, state="readonly", width=50)
        self.fika_server_path_var.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.fika_server_path_var = ttk.Label(fika_frame, text="", foreground="green")
        self.fika_server_path_var.grid(row=3, column=2, padx=10, sticky="w")

        self.root_path_var.trace_add("write", self._on_path_change)
        self.grid_columnconfigure(1, weight=1)

        self._check_valid_root_path(root_path)

    def select_folder(self):
        folder = filedialog.askdirectory(title="选择塔科夫根目录")
        if folder:
            self.root_path_var.set(folder.replace("/", "\\"))

    def _on_path_change(self, *args):
        path = self.root_path_var.get().replace("/", "\\")
        self._check_valid_root_path(path)

    def _check_valid_root_path(self, path):
        if os.path.isdir(path):
            self.validation_label.config(text="路径有效", foreground="green")
            self.config.update_tarkov_root(path)
        else:
            self.validation_label.config(text="路径无效", foreground="red")
