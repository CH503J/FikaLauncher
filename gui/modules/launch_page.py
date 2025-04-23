import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import os
import psutil

from config.config import ConfigManager


class LaunchPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.config = ConfigManager()

        # 启动服务端按钮
        self.start_button = ttk.Button(self, text="启动服务端", command=self.start_server)
        self.start_button.pack(padx=10, pady=10)

        # 日志显示区域
        self.log_text = tk.Text(self, height=15, width=80, wrap=tk.WORD)
        self.log_text.pack(padx=10, pady=10)
        self.log_text.insert(tk.END, "服务端日志将显示在这里...\n")
        self.log_text.config(state=tk.DISABLED)

    def start_server(self):
        """启动服务端并在Text区域显示日志"""
        # 获取服务端.exe文件所在的目录路径
        server_exe_path = self.config.get_server_path()
        server_dir = os.path.dirname(server_exe_path)

        # 检查端口6969是否被占用，若占用则杀死进程
        if self.is_port_in_use(6969):
            self.kill_process_using_port(6969)

        # 使用线程启动服务端，避免阻塞主界面
        threading.Thread(target=self.run_server, args=(server_dir, server_exe_path), daemon=True).start()

    def run_server(self, server_dir, exe_path):
        """运行exe文件并捕获日志输出"""
        # 切换当前工作目录到服务端目录
        os.chdir(server_dir)

        # 使用subprocess启动服务端.exe
        process = subprocess.Popen(exe_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors="replace")

        # 实时读取并显示日志
        for line in process.stdout:
            self.insert_log(line)

        # 读取错误输出（如果有）
        for line in process.stderr:
            self.insert_log(line)

    def insert_log(self, text):
        """将日志插入到Text组件中"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text)
        self.log_text.yview(tk.END)  # 滚动到底部
        self.log_text.config(state=tk.DISABLED)

    def is_port_in_use(self, port):
        """检查指定端口是否被占用"""
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port:
                return True
        return False

    def kill_process_using_port(self, port):
        """杀死占用指定端口的进程"""
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == port:
                # 获取占用该端口的进程PID
                pid = conn.pid
                if pid:
                    try:
                        process = psutil.Process(pid)
                        process.terminate()  # 杀死进程
                        self.insert_log(f"已终止占用端口 {port} 的进程（PID：{pid}）。\n")
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        self.insert_log(f"无法终止占用端口 {port} 的进程（PID：{pid}）。\n")
                break
