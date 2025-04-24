import os.path
import socket
import subprocess
import time
import tkinter as tk
from tkinter import ttk

import commentjson
import psutil

from config.config import ConfigManager
from gui.components.common import create_label_frame


def create_log_tabs(parent_frame):
    # 创建标签页容器
    notebook = ttk.Notebook(parent_frame)
    notebook.grid(row=0, column=0, sticky="nsew")

    # 创建四个标签页
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)
    tab4 = ttk.Frame(notebook)

    notebook.add(tab1, text="GUI")
    notebook.add(tab2, text="Server")
    notebook.add(tab3, text="Headless")
    notebook.add(tab4, text="专用主机")

    # 在每个标签页中添加内容，示例为文本框
    log_text1 = tk.Text(tab1, height=10, width=75)
    log_text1.pack(padx=20, pady=10)
    log_text2 = tk.Text(tab2, height=10, width=75)
    log_text2.pack(padx=20, pady=10)
    log_text3 = tk.Text(tab3, height=10, width=75)
    log_text3.pack(padx=20, pady=10)
    log_text4 = tk.Text(tab4, height=10, width=75)
    log_text4.pack(padx=20, pady=10)


def create_buttons(parent_frame):
    launcher = LauncherServer()
    launcher_button = ttk.Button(parent_frame, text="一键启动", command=launcher.start)
    launcher_button.grid(row=0, column=0, padx=50, pady=5)

    terminated_button = TerminatedServer()
    terminated_button = ttk.Button(parent_frame, text="一键关闭", command=terminated_button.stop)
    terminated_button.grid(row=0, column=1, padx=50, pady=5)

    relaunched_button = RelaunchedServer()
    relaunched_button = ttk.Button(parent_frame, text="一键重启", command=relaunched_button.restart)
    relaunched_button.grid(row=0, column=2, padx=50, pady=5)


class LaunchPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # 创建一个标题框，包含三个按钮，并将标题框铺满整个GUI宽度
        button_frame = create_label_frame(self, "服务", row=0)

        # 在标题框中添加按钮
        create_buttons(button_frame)

        # 创建日志框标题框
        log_frame = create_label_frame(self, "日志", row=1)

        # 在日志框内添加标签页
        create_log_tabs(log_frame)


class LauncherServer:
    def __init__(self):
        self.ip = None
        self.port = None
        self.backup_ip = None
        self.backup_port = None
        self.ps1_pid = None
        self.ps1_process = None
        self.server_pid = None
        self.server_process = None
        self.config = None

    def start(self):
        print("启动操作")
        self.config = ConfigManager()
        server_path = self.config.get_server_path()
        fika_path = self.config.get_fika_server_path()

        print(server_path)
        print(fika_path)
        if not server_path or not fika_path:
            print("配置文件中缺少路径信息！")
            return

        # 获取服务端ip端口信息
        config = ConfigManager()
        root_path = config.get_tarkov_root()
        ip_port_path = os.path.join(root_path, "SPT_Data", "Server", "configs", "http.json")
        if os.path.exists(ip_port_path):
            try:
                with open(ip_port_path, 'r', encoding='utf-8') as file:
                    ip_port_data = commentjson.load(file)
                    self.ip = ip_port_data.get("ip", "")
                    self.port = ip_port_data.get("port", "")
                    self.backup_ip = ip_port_data.get("backendIp", "")
                    self.backup_port = ip_port_data.get("backendPort", "")
            except commentjson.JSONLibraryException as e:
                print(f"JSON解析错误: {e}")
        else:
            print("HTTP配置文件不存在！")
        print(f"服务端IP: {self.ip}, 服务端端口: {self.port}, 备份IP: {self.backup_ip}, 备份端口: {self.backup_port}")

        # 检测指定端口是否被占用
        try:
            # 创建socket对象
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # 设置连接超时
                s.settimeout(1)
                # 尝试连接指定ip端口
                result = s.connect_ex((self.ip, int(self.port)))

            if result == 0:
                print(f"端口 {self.port} 被占用，尝试杀死占用该端口的进程...")

                # 查找并终止占用该端口的进程
                found_process = False
                for process in psutil.process_iter():
                    try:
                        # 获取进程的所有网络连接
                        for conn in process.connections(kind='inet'):
                            if conn.laddr.port == int(self.port):  # 端口占用
                                print(f"进程 {process.name()} (PID: {process.pid}) 正在占用端口 {self.port}")
                                try:
                                    process.terminate()  # 尝试杀死进程
                                    process.wait()  # 等待进程结束
                                    print(f"进程 {process.pid} 已被终止")
                                    found_process = True
                                    break  # 找到并终止进程后跳出循环
                                except psutil.NoSuchProcess:
                                    print(f"进程 {process.pid} 不存在")
                                except psutil.AccessDenied:
                                    print(f"没有权限终止进程 {process.pid}")
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                    if found_process:
                        break
                else:
                    print(f"无法找到占用端口 {self.port} 的进程")
                    return  # 如果没有找到占用进程，直接退出

                # 等待短暂的时间确保端口完全释放
                time.sleep(1)

            else:
                print(f"端口 {self.port} 可用，继续启动服务端！")

            # 启动服务端
            if os.path.exists(server_path):
                # 启动服务端，保证启动脚本与服务端在同一个目录下
                server_dir = os.path.dirname(server_path)
                log_file_path = os.path.join(server_dir, "server_log.log")  # 改为 .log 文件扩展名

                with open(log_file_path, "w") as log_file:
                    # cwd后加入stdout=log_file, stderr=log_file即可将服务端日志写入log文件
                    process = subprocess.Popen([server_path], cwd=server_dir)
                    self.server_pid = process.pid
                    self.server_process = process
                    time.sleep(1)  # 给服务端一些时间启动
                    # print("服务端已启动，日志记录在 server_log.log 中")
            else:
                print("服务端路径不存在！")

            # 启动 PS1 脚本
            scripts_path = os.path.join(fika_path, "assets", "scripts")
            if os.path.exists(scripts_path):
                ps1_file = None
                for file in os.listdir(scripts_path):
                    if file.lower().startswith("start_headless_") and file.lower().endswith(".ps1"):
                        ps1_file = os.path.join(scripts_path, file)
                        break

                if ps1_file and os.path.exists(ps1_file):
                    self.ps1_process = subprocess.Popen(
                        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps1_file],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
                    time.sleep(1)
                    self.ps1_pid = self.ps1_process.pid
                    print("PS1脚本已启动")
                else:
                    print("未找到符合条件的PS1脚本！")
            else:
                print(f"PS1 脚本路径 {scripts_path} 不存在！")
        except Exception as e:
            print(f"连接错误: {e}")


class TerminatedServer:
    def stop(self):
        pass


class RelaunchedServer:
    def restart(self):
        pass
