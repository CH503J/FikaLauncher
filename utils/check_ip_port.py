import socket

from config.config import ConfigManager


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
