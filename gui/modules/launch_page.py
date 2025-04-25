import os.path
import socket
import subprocess
import time
import tkinter as tk
from tkinter import ttk

import psutil

from config.config import ConfigManager
from gui.components import common
from utils.check_ip_port import get_fika_headless_path


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
        button_frame = common.create_label_frame(self, "服务", row=0)

        # 在标题框中添加按钮
        create_buttons(button_frame)

        # 创建日志框标题框
        log_frame = common.create_label_frame(self, "日志", row=1)

        # 在日志框内添加标签页
        create_log_tabs(log_frame)


class LauncherServer:
    def __init__(self):
        self.config = None
        self.config = ConfigManager()
        # 获取服务端路径
        self.server_path = self.config.get_server_path()
        # 获取根目录
        self.tarkov_root_path = self.config.get_tarkov_root()
        # 获取获取Headless专用主机ps1启动脚本
        self.fika_headless_path = get_fika_headless_path(self.tarkov_root_path, "Start_headless_")
        # 获取fika服务端mod路径
        self.fika_server_mod_path = self.config.get_fika_server_path()

        # 获取服务端ip端口信息http.json
        self.server_conf_path = os.path.join(self.tarkov_root_path, "SPT_Data", "Server", "configs", "http.json")
        # 获取fika服务端mod配置文件路径
        self.fika_server_conf_path = os.path.join(self.fika_server_mod_path, "assets", "configs", "fika.jsonc")
        self.ip_port_dict = common.get_ip_port(self.server_conf_path, self.fika_server_conf_path)

    def start(self):
        """
        一键启动服务端和fika专用主机
        """
        if not self.server_path or not self.fika_headless_path:
            print("❌ 根目录未找到服务端或Headless专用主机！")
            return

        try:
            # 创建socket对象
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0)
                result = s.connect_ex((self.ip_port_dict["ip"], int(self.ip_port_dict["port"])))
        except socket.timeout:
            print(
                f'❌ 连接指定IP端口超时，请检查网络连接或IP端口配置！IP{self.ip_port_dict["ip"]}；端口{self.ip_port_dict["port"]}')
            return

        if result == 0:
            print(f'⭕ 端口{self.ip_port_dict["port"]}被占用，正在结束占用端口的进程')
            common.kill_process_in_use(self.ip_port_dict["ip"], self.ip_port_dict["port"])
        else:
            print(f'✅ 端口{self.ip_port_dict["port"]}未被占用，服务端启动中...')

        # 启动服务端
        if not self.start_server():
            print("❌ 服务端启动失败。")
        else:
            print("✅ 服务端启动成功。")
            if not self.start_fika_headless_server():
                print("❌ fika专用主机启动失败。")
            else:
                print("✅ fika专用主机启动成功。")

    def start_server(self) -> bool:
        """
        启动服务端并确认端口是否被监听
        :return: True 表示成功，False 表示失败
        """
        if not os.path.exists(self.server_path):
            print("❌ 服务端路径不存在")
            return False

        server_dir = os.path.dirname(self.server_path)
        process = subprocess.Popen(
            [self.server_path],
            cwd=server_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        server_pid = process.pid

        ip = self.ip_port_dict["ip"]
        port = int(self.ip_port_dict["port"])
        target_process_name = "SPT.Server.exe"

        print("🚬 等待服务端监听端口中...")

        for _ in range(30):  # 最多等待30秒
            time.sleep(1)
            for conn in psutil.net_connections(kind="inet"):
                if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
                    pid = conn.pid
                    if pid:
                        try:
                            p = psutil.Process(pid)
                            if target_process_name.lower() in p.name().lower():
                                print(f'✅ 服务端已启动！PID：{server_pid}，进程：{target_process_name}')
                                return True
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass

        # 超时未监听成功
        print("⚠️ 服务端监听失败，正在终止进程...")
        try:
            process.terminate()
            process.wait(timeout=3)
            print("✅ 服务端已终止")
        except Exception as e:
            print(f"❌ 终止服务端失败：{e}")

        return False

    def start_fika_headless_server(self):
        """
            启动 Fika Headless Server（.ps1 脚本）
            :return: True 启动成功，False 启动失败
            """
        if not os.path.exists(self.fika_headless_path[0]):
            print("❌ Fika Headless 启动脚本路径不存在")
            return False

        try:
            # 使用 PowerShell 启动脚本，确保不阻塞主线程
            command = ["powershell", "-ExecutionPolicy", "Bypass", "-File", self.fika_headless_path[0]]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"🟡 已尝试启动 Fika Headless Server，PID: {process.pid}")

            # 可选：你可以加一段时间延迟，并检查是否运行中
            time.sleep(3)
            if process.poll() is None:
                print("\n✅ Fika Headless Server 启动中")
                return True
            else:
                stderr = process.stderr.read().decode("utf-8")
                print(f"❌ Fika Headless Server 启动失败：{stderr}")
                return False
        except Exception as e:
            print(f"❌ 启动 Fika Headless Server 出错：{e}")
            return False


class TerminatedServer:
    def stop(self):
        pass


class RelaunchedServer:
    def restart(self):
        pass
