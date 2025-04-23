import commentjson
import os
import tkinter as tk
from tkinter import ttk
from gui.components import common
from tkinter import Toplevel
from config.config import ConfigManager

"""
修改页
    现阶段只对
        服务器：ip、端口、备用ip、备用端口、最大延迟、日志请求
        fika服务器：ip、端口、备用ip、备用端口
    做修改
"""


class ModifyPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        modify_frame = common.create_label_frame(self, "IP端口", row=0)
        self._create_buttons(modify_frame)

    def _create_buttons(self, parent_frame):
        button_frame = ttk.Frame(parent_frame)
        button_frame.pack(padx=10, pady=10, fill="x")

        button1 = ttk.Button(button_frame, text="服务端", command=self.open_server_modify)
        button1.grid(row=0, column=0, padx=5, pady=5)

        button2 = ttk.Button(button_frame, text="Fika", command=self.open_fika_modify)
        button2.grid(row=0, column=1, padx=5, pady=5)

    def open_server_modify(self):
        """打开服务端IP端口设置页面"""
        new_window = Toplevel(self)
        new_window.title("服务端IP端口设置")
        new_window.geometry("500x300")
        page1 = ServerIpPort(new_window)
        page1.pack(fill="both", expand=True)

    def open_fika_modify(self):
        """打开FikaIP端口设置页面"""
        new_window = Toplevel(self)
        new_window.title("FikaIP端口设置")
        new_window.geometry("500x300")
        page2 = FikaIpPort(new_window)
        page2.pack(fill="both", expand=True)


# IP端口基类（修改页二级页面）
class IpPortBase(tk.Frame):
    def __init__(self, parent, title_prefix, config_file_path):
        super().__init__(parent)

        self.config_file_path = config_file_path

        ip_port_frame = ttk.Frame(self)
        ip_port_frame.pack(padx=10, pady=10, fill="x")

        label_width = 10

        self.server_ip_var = tk.StringVar()
        ttk.Label(ip_port_frame, text="IP:", width=label_width, anchor='w').grid(row=0, column=0, padx=10, sticky="w")
        self.server_ip_entry = ttk.Entry(ip_port_frame, textvariable=self.server_ip_var, width=15)
        self.server_ip_entry.grid(row=0, column=1, padx=10, sticky="ew")

        self.server_port_var = tk.StringVar()
        ttk.Label(ip_port_frame, text="端口:", width=label_width, anchor='w').grid(row=0, column=2, padx=10, sticky="w")
        self.server_port_entry = ttk.Entry(ip_port_frame, textvariable=self.server_port_var, width=5)
        self.server_port_entry.grid(row=0, column=3, padx=10, sticky="ew")

        backup_frame = ttk.Frame(self)
        backup_frame.pack(padx=10, pady=10, fill="x")

        self.backup_ip_var = tk.StringVar()
        ttk.Label(
            backup_frame,
            text=f"{title_prefix}备用IP:",
            width=label_width, anchor='w'
        ).grid(
            row=0,
            column=0,
            padx=10,
            sticky="w")
        self.backup_ip_entry = ttk.Entry(
            backup_frame,
            textvariable=self.backup_ip_var,
            width=15)
        self.backup_ip_entry.grid(
            row=0,
            column=1,
            padx=10,
            sticky="ew")

        self.backup_port_var = tk.StringVar()
        ttk.Label(
            backup_frame,
            text=f"{title_prefix}备用端口:",
            width=label_width,
            anchor='w').grid(
            row=0,
            column=2,
            padx=10,
            sticky="w")
        self.backup_port_entry = ttk.Entry(backup_frame, textvariable=self.backup_port_var, width=5)
        self.backup_port_entry.grid(
            row=0,
            column=3,
            padx=10,
            sticky="ew")

    def save_server_settings(self):
        """保存设置"""
        server_ip = self.server_ip_var.get()
        server_port = self.server_port_var.get()
        backup_ip = self.backup_ip_var.get()
        backup_port = self.backup_port_var.get()

        print(f"保存设置: IP = {server_ip}, 端口 = {server_port}")
        print(f"备用IP = {backup_ip}, 备用端口 = {backup_port}")


# 服务端IP端口
class ServerIpPort(IpPortBase):
    def __init__(self, parent):
        self.config = ConfigManager()
        # 获取Tarkov根目录路径
        tarkov_root = self.config.get_tarkov_root()

        # 拼接出完整的http.json文件路径
        config_folder = os.path.join(tarkov_root, r"SPT_Data\Server\configs")
        self.config_file_path = os.path.join(config_folder, "http.json")

        self.max_delay_var = tk.StringVar()
        self.log_request_var = tk.BooleanVar()

        super().__init__(parent, "服务端", self.config_file_path)

        # 创建延迟和日志请求相关的控件
        delay_log_frame = ttk.Frame(self)
        delay_log_frame.pack(padx=10, pady=10, fill="x")

        label_width = 10

        # 初始化控件变量
        self.max_delay_var = tk.StringVar()
        ttk.Label(
            delay_log_frame,
            text="最大延迟:",
            width=label_width,
            anchor='w').grid(
            row=0,
            column=0,
            padx=10,
            sticky="w")
        self.max_delay_entry = ttk.Entry(
            delay_log_frame,
            textvariable=self.max_delay_var,
            width=6)
        self.max_delay_entry.grid(
            row=0,
            column=1,
            padx=10,
            sticky="ew")

        self.log_request_var = tk.BooleanVar()
        ttk.Label(
            delay_log_frame,
            text="日志请求:",
            width=label_width,
            anchor='w').grid(
            row=0,
            column=2,
            padx=10,
            sticky="w")
        self.log_request_check = ttk.Checkbutton(
            delay_log_frame,
            variable=self.log_request_var,
            onvalue=True,
            offvalue=False)
        self.log_request_check.grid(row=0, column=3, padx=10)

        # 保存按钮
        save_button = ttk.Button(self, text="保存设置", command=self.save_server_settings)
        save_button.pack(padx=10, pady=10)

        # 调用 load_settings 读取配置文件
        self.load_settings(self.config_file_path)

    def load_settings(self, config_file_path):
        """从配置文件读取设置并显示在文本框中"""
        if os.path.exists(config_file_path):
            try:
                with open(config_file_path, 'r', encoding='utf-8') as file:
                    config = commentjson.load(file)

                    # 更新控件显示的内容
                    self.server_ip_var.set(config.get("ip", ""))
                    self.server_port_var.set(config.get("port", ""))
                    self.backup_ip_var.set(config.get("backendIp", ""))
                    self.backup_port_var.set(config.get("backendPort", ""))

                    # 读取最大延迟和日志请求
                    self.max_delay_var.set(config.get("webSocketPingDelayMs", ""))
                    self.log_request_var.set(config.get("logRequests", True))

            except commentjson.JSONLibraryException:
                print(f"无法解析文件 {config_file_path}")
        else:
            print(f"配置文件 {config_file_path} 不存在")

    def save_server_settings(self):
        """保存服务端设置"""
        # 调用基类方法保存 IP 和端口设置
        super().save_server_settings()

        # 获取并保存最大延迟和日志请求设置
        max_delay = self.max_delay_var.get()
        log_request = self.log_request_var.get()

        print(f"保存服务端设置（最大延迟与日志请求）: 最大延迟 = {max_delay}, 启用日志请求 = {log_request}")


class FikaIpPort(IpPortBase):
    def __init__(self, parent):
        self.config = ConfigManager()
        # 假设Fika的配置文件路径为 SPT_Data/Fika/configs/http.json
        server_ip_port = self.config.get_fika_server_path() + r"\assets\configs\fika.jsonc"
        super().__init__(parent, "Fika", server_ip_port)

        self.load_settings(server_ip_port)

        save_button = ttk.Button(self, text="保存设置", command=self.save_server_settings)
        save_button.pack(padx=10, pady=10)

    def load_settings(self, config_file_path):
        """从配置文件读取设置并显示在文本框中"""
        if os.path.exists(config_file_path):
            try:
                with open(config_file_path, 'r', encoding='utf-8') as file:
                    config = commentjson.load(file)

                    fika_server = config.get("server", "")
                    fika_server_spt = fika_server.get("SPT", "")
                    fika_server_spt_http = fika_server_spt.get("http", "")

                    self.server_ip_var.set(fika_server_spt_http.get("ip", ""))
                    self.server_port_var.set(fika_server_spt_http.get("port", ""))
                    self.backup_ip_var.set(fika_server_spt_http.get("backendIp", ""))
                    self.backup_port_var.set(fika_server_spt_http.get("backendPort", ""))

            except commentjson.JSONLibraryException:
                print(f"无法解析文件 {config_file_path}")
        else:
            print(f"配置文件 {config_file_path} 不存在")
