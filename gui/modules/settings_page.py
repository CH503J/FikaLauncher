import tkinter as tk
from tkinter import ttk, filedialog
from config.config import ConfigManager
from utils.check_root_path_util import is_valid_tarkov_root


class SettingsPage(tk.Frame):
    def __init__(self, parent, config: ConfigManager):
        super().__init__(parent)
        self.fika_server_path_var = None
        self.fika_headless_path_var = None
        self.fika_core_path_var = None
        self.launcher_path_var = None
        self.server_path_var = None
        self.client_path_var = None
        self.config = config
        self.root_path_var = tk.StringVar(value=self.config.get_tarkov_root().replace("/", "\\"))

        # 根目录选择组件
        self._create_root_selector()

        # SPT 路径组
        spt_frame = self._create_label_frame("AKI-SPT", row=2)
        self._add_path_row(spt_frame, 2, "主程序(EscapeFromTarkov)", "client", self.config.get_client_path())
        self._add_path_row(spt_frame, 3, "服务端(SPT.Server)", "server", self.config.get_server_path())
        self._add_path_row(spt_frame, 4, "启动器(SPT.Launcher)", "launcher", self.config.get_launcher_path())

        # Fika 路径组
        fika_frame = self._create_label_frame("Fika", row=5)
        self._add_path_row(fika_frame, 1, "FikaCore", "fika_core")
        self._add_path_row(fika_frame, 2, "FikaHeadless", "fika_headless")
        self._add_path_row(fika_frame, 3, "FikaServer", "fika_server")

        # 根路径变更监听
        self.root_path_var.trace_add("write", self._on_path_change)
        self.grid_columnconfigure(1, weight=1)
        self._check_valid_root_path(self.root_path_var.get())

    def _create_root_selector(self):
        browse_button = ttk.Button(self, text="选择文件夹", command=self.select_folder)
        browse_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        root_entry = ttk.Entry(self, textvariable=self.root_path_var, width=50)
        root_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.validation_label = ttk.Label(self, text="", foreground="red")
        self.validation_label.grid(row=0, column=2, padx=10, sticky="w")

    def _create_label_frame(self, title: str, row: int) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(self, text=title)
        frame.grid(row=row, column=0, columnspan=3, padx=10, pady=(5, 15), sticky="w")
        frame.grid_columnconfigure(1, weight=1)
        return frame

    def _add_path_row(self, parent, row, label_text, key, initial_value=""):
        var = tk.StringVar(value=initial_value)
        setattr(self, f"{key}_path_var", var)

        ttk.Label(parent, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = ttk.Entry(parent, textvariable=var, state="readonly", width=50)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        status = ttk.Label(parent, text="", foreground="green")
        status.grid(row=row, column=2, padx=10, sticky="w")

        setattr(self, f"{key}_entry", entry)
        setattr(self, f"{key}_status", status)

    def select_folder(self):
        folder = filedialog.askdirectory(title="选择塔科夫根目录")
        if folder:
            self.root_path_var.set(folder.replace("/", "\\"))

    def _on_path_change(self, *args):
        path = self.root_path_var.get().replace("/", "\\")
        self._check_valid_root_path(path)

    def _check_valid_root_path(self, path):
        if is_valid_tarkov_root(path):
            self.validation_label.config(text="👍", foreground="green")
            self.config.update_tarkov_root(path)
            self.client_path_var.set(self.config.get_client_path())
            self.server_path_var.set(self.config.get_server_path())
            self.launcher_path_var.set(self.config.get_launcher_path())
            self.fika_core_path_var.set(self.config.get_fika_core_path())
            self.fika_headless_path_var.set(self.config.get_fika_headless_path())
            self.fika_server_path_var.set(self.config.get_fika_server_path())
        else:
            self.validation_label.config(text="👎", foreground="red")
