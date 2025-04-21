import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

from config.config import ConfigManager


# 只显示路径末尾部分，例如 .../文件夹/文件名
def shorten_path(full_path, keep=2):
    parts = full_path.replace("\\", "/").split("/")
    if len(parts) <= keep:
        return full_path
    return f".../{'/'.join(parts[-keep:])}"


class TarkovLauncherGUI:
    def __init__(self, root):
        self.headless_path_full = None
        self.server_path_full = None
        self.port_var = None
        self.ip_var = None
        self.headless_path_var = None
        self.server_path_var = None
        self.log_text = None
        self.root = root
        self.root.title("逃离塔科夫 Headless 一键启动器")

        # 创建config实例
        self.config = ConfigManager()

        # 设置窗口大小
        self.root.geometry(self.config.get_window_size())
        # 居中窗口显示
        self.root.update_idletasks()  # 确保 winfo_width 获取准确
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.create_widgets()

        # 加载config
        self.load_config()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # ========== 文件路径设置 ==========
        path_frame = ttk.LabelFrame(self.root, text="服务路径设置")
        path_frame.pack(fill="x", padx=10, pady=10)

        # 服务端路径
        ttk.Label(path_frame, text="服务端路径 (.exe):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.server_path_var = tk.StringVar()
        server_entry = ttk.Entry(path_frame, textvariable=self.server_path_var, width=60)
        server_entry.grid(row=0, column=1, padx=5)
        ttk.Button(path_frame, text="浏览", command=self.browse_server_path).grid(row=0, column=2, padx=5)

        # Headless路径
        ttk.Label(path_frame, text="Headless路径 (.ps1):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.headless_path_var = tk.StringVar()
        headless_entry = ttk.Entry(path_frame, textvariable=self.headless_path_var, width=60)
        headless_entry.grid(row=1, column=1, padx=5)
        ttk.Button(path_frame, text="浏览", command=self.browse_headless_path).grid(row=1, column=2, padx=5)

        # ========== IP 和 端口 ==========
        network_frame = ttk.LabelFrame(self.root, text="网络设置")
        network_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(network_frame, text="IP地址:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_var = tk.StringVar(value="127.0.0.1")
        ttk.Entry(network_frame, textvariable=self.ip_var, width=20).grid(row=0, column=1, padx=5)

        ttk.Label(network_frame, text="端口:").grid(row=0, column=2, padx=5)
        self.port_var = tk.StringVar(value="6969")
        ttk.Entry(network_frame, textvariable=self.port_var, width=10).grid(row=0, column=3, padx=5)

        # 恢复ip和端口为默认值
        ttk.Button(
            network_frame,
            text="恢复默认",
            command=self.reset_network_to_default
        ).grid(row=0, column=4, rowspan=2, padx=5)

        # ========== 控制按钮 ==========
        control_frame = ttk.LabelFrame(self.root, text="控制面板")
        control_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(control_frame, text="一键启动", command=self.start_all).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(control_frame, text="一键关闭", command=self.stop_all).grid(row=0, column=1, padx=10)
        ttk.Button(control_frame, text="一键重启", command=self.restart_all).grid(row=0, column=2, padx=10)

        # ========== 日志输出 ==========
        log_frame = ttk.LabelFrame(self.root, text="日志输出")
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15)
        self.log_text.pack(fill="both", expand=True)

    # ========== 控制按钮回调 ==========
    def start_all(self):
        self.append_log("🟢 正在启动所有服务...")
        self.save_config()

    def stop_all(self):
        self.append_log("🔴 正在关闭所有服务...")
        self.save_config()

    def restart_all(self):
        self.append_log("🟡 正在重启所有服务...")
        self.save_config()

    # ========== 浏览路径 ==========
    def browse_server_path(self):
        path = filedialog.askopenfilename(filetypes=[("可执行文件", "*.exe")])
        if path:
            self.server_path_full = path
            self.server_path_var.set(shorten_path(path))
            self.append_log(f"已选择服务端路径: {path}")

    def browse_headless_path(self):
        path = filedialog.askopenfilename(filetypes=[("PowerShell 脚本", "*.ps1")])
        if path:
            self.headless_path_var.set(path)
            self.headless_path_full = path
            self.headless_path_var.set(shorten_path(path))
            self.append_log(f"已选择Headless路径: {path}")

    # ========== 日志追加 ==========
    def append_log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def load_config(self):
        self.server_path_full = self.config.get_server_path()
        self.server_path_var.set(shorten_path(self.server_path_full))
        self.headless_path_full = self.config.get_headless_path()
        self.headless_path_var.set(shorten_path(self.headless_path_full))
        self.ip_var.set(self.config.get_ip())
        self.port_var.set(self.config.get_port())

    def save_config(self):
        current_geometry = self.root.winfo_geometry().split("+")[0]  # 例如 "700x600"
        self.config.update_config(
            server_path=self.server_path_full,
            headless_path=self.headless_path_full,
            ip=self.ip_var.get(),
            port=self.port_var.get(),
            window_size=current_geometry
        )

    # 重置 IP 和端口为默认值
    def reset_network_to_default(self):
        self.ip_var.set("127.0.0.1")
        self.port_var.set("6969")
        self.append_log("🌐 已重置 IP 和端口为默认值：127.0.0.1:6969")

    def on_close(self):
        self.save_config()
        self.root.destroy()
