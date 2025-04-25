# gui/components/common.py
import os
from tkinter import ttk

import commentjson


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
    frame.grid_columnconfigure(0, weight=1)  # 使列能够扩展
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    return frame


def get_ip_port(server_conf_path, fika_server_conf_path):
    """
    传入服务端http.json和服务端fika模组config.jsonc文件路径
    :param server_conf_path: 服务端ip端口配置文件路径
    :param fika_server_conf_path: Fika服务端ip端口配置文件路径
    :return: 服务端和fika字典
    """
    if os.path.exists(server_conf_path):
        try:
            with open(server_conf_path, "r", encoding="utf-8") as file:
                ip_port_data = commentjson.load(file)
                ip = ip_port_data.get("ip", "")
                port = ip_port_data.get("port", "")
                backend_ip = ip_port_data.get("backendIp", "")
                backend_port = ip_port_data.get("backendPort", "")
        except commentjson.JSONLibraryException as e:
            print(f"未获取到服务端ip端口信息！错误信息：{e}")

    if os.path.exists(fika_server_conf_path):
        try:
            with open(fika_server_conf_path, "r", encoding="utf-8") as file:
                fika_ip_port_data = commentjson.load(file)
                label1 = fika_ip_port_data.get("server", "")
                label2 = label1.get("SPT", "")
                label3 = label2.get("http", "")

                fika_ip = label3.get("ip", "")
                fika_port = label3.get("port", "")
                fika_backend_ip = label3.get("backendIp", "")
                fika_backend_port = label3.get("backendPort", "")
        except commentjson.JSONLibraryException as e:
            print(f"未获取到fika服务端ip端口信息！错误信息：{e}")

    return dict(
        ip=ip,
        port=port,
        backend_ip=backend_ip,
        backend_port=backend_port,
        fika_ip=fika_ip,
        fika_port=fika_port,
        fika_backend_ip=fika_backend_ip,
        fika_backend_port=fika_backend_port
    )


def kill_process_in_use(ip, port):
    """
    根据ip端口杀死进程
    :param port:
    :param ip:
    :return:布尔
    """
    import psutil
    for conn in psutil.net_connections(kind="inet"):
        laddr = conn.laddr
        if conn.status == psutil.CONN_LISTEN and laddr.port == port:
            # 如果指定了 IP，则判断 IP 和 port 都匹配
            if ip in ip or laddr.ip == ip:
                pid = conn.pid
                if pid:
                    try:
                        p = psutil.Process(pid)
                        print(f"正在终止占用端口 {port} 的进程: PID={pid}, 名称={p.name()}")
                        p.terminate()
                        p.wait(timeout=3)
                        print("进程已成功终止")
                        return True
                    except Exception as e:
                        print(f"终止进程失败: {e}")
                        return False
    print(f"没有找到占用端口 {port} 的进程")
    return False
