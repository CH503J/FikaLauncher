import socket
from pathlib import Path

from config.config import ConfigManager


def get_fika_headless_path(tarkov_root_path, keyword):
    """
    获取Headless专用主机ps1启动脚本
    :param tarkov_root_path:
    :param keyword:
    :return:
    """
    base = Path(tarkov_root_path)
    return [str(p.resolve()) for p in base.rglob('*') if keyword in p.name]

def get_local_ip():
    try:
        # 获取主机名
        hostname = socket.gethostname()
        # 获取本机本地ip地址
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except socket.error as e:
        print("获取本地IP地址失败：", e)
        return None




if __name__ == '__main__':
    local_ip = get_local_ip()
    if local_ip:
        print("本地IP地址：", local_ip)
    else:
        print("无法获取本地IP地址")

    a = get_fika_headless_path(r"C:\Develop\Server", "Start_headless_")
    print(a)