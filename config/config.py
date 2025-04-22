import json
import os
import configparser


class ConfigManager:
    def __init__(self, config_path="config/config.ini"):
        self.config_path = config_path
        self.config = configparser.ConfigParser()

        if not os.path.exists(os.path.dirname(config_path)):
            os.makedirs(os.path.dirname(config_path))

        if not os.path.isfile(self.config_path):
            self._create_default_config()
        else:
            self.config.read(self.config_path)

    def _create_default_config(self):
        self.config["PATHS"] = {
            "tarkov_root": "",
            "server_path": "",
            "launcher_path": "",
            "client_path": "",
            "headless_path": "",
            "fika_core_path": "",
            "fika_headless_path": "",
            "fika_server_path": ""
        }
        self.config["NETWORK"] = {
            "ip": "127.0.0.1",
            "port": "6969"
        }
        self.config["GUI"] = {
            "window_size": "800x600"
        }
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def get_tarkov_root(self):
        return self.config.get("PATHS", "tarkov_root", fallback="")

    def get_server_path(self):
        return self.config.get("PATHS", "server_path", fallback="")

    def get_launcher_path(self):
        return self.config.get("PATHS", "launcher_path", fallback="")

    def get_client_path(self):
        return self.config.get("PATHS", "client_path", fallback="")

    def get_headless_path(self):
        return self.config.get("PATHS", "headless_path", fallback="")

    def get_fika_core_path(self):
        return self.config.get("PATHS", "fika_core_path", fallback="")

    def get_fika_headless_path(self):
        return self.config.get("PATHS", "fika_headless_path", fallback="")

    def get_fika_server_path(self):
        return self.config.get("PATHS", "fika_server_path", fallback="")

    def get_ip(self):
        return self.config.get("NETWORK", "ip", fallback="127.0.0.1")

    def get_port(self):
        return self.config.get("NETWORK", "port", fallback="6969")

    def get_window_size(self):
        return self.config.get("GUI", "window_size", fallback="700x600")

    def update_config(self, server_path=None, launcher_path=None, client_path=None,
                      headless_path=None, fika_core_path=None, fika_headless_path=None,
                      fika_server_path=None, ip=None, port=None, window_size=None):
        if server_path is not None:
            self.config["PATHS"]["server_path"] = server_path
        if launcher_path is not None:
            self.config["PATHS"]["launcher_path"] = launcher_path
        if client_path is not None:
            self.config["PATHS"]["client_path"] = client_path
        if headless_path is not None:
            self.config["PATHS"]["headless_path"] = headless_path
        if fika_core_path is not None:
            self.config["PATHS"]["fika_core_path"] = fika_core_path
        if fika_headless_path is not None:
            self.config["PATHS"]["fika_headless_path"] = fika_headless_path
        if fika_server_path is not None:
            self.config["PATHS"]["fika_server_path"] = fika_server_path
        if ip is not None:
            self.config["NETWORK"]["ip"] = ip
        if port is not None:
            self.config["NETWORK"]["port"] = port
        if window_size is not None:
            self.config["GUI"]["window_size"] = window_size

        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def update_tarkov_root(self, root_path):
        self.config["PATHS"]["tarkov_root"] = root_path

        # 填充并保存主程序、服务端、启动器路径
        client = os.path.join(root_path, "EscapeFromTarkov.exe")
        server = os.path.join(root_path, "SPT.Server.exe")
        launcher = os.path.join(root_path, "SPT.Launcher.exe")

        self.config["PATHS"]["client_path"] = client if os.path.isfile(client) else ""
        self.config["PATHS"]["server_path"] = server if os.path.isfile(server) else ""
        self.config["PATHS"]["launcher_path"] = launcher if os.path.isfile(launcher) else ""

        # 填充并保存 Fika 路径
        fika_core = os.path.join(root_path, "BepInEx", "plugins", "Fika.Core.dll")
        fika_headless = os.path.join(root_path, "BepInEx", "plugins", "Fika.Headless.dll")
        fika_server = os.path.join(root_path, "user", "mods", "fika-server")

        self.config["PATHS"]["fika_core_path"] = fika_core if os.path.isfile(fika_core) else ""
        self.config["PATHS"]["fika_headless_path"] = fika_headless if os.path.isfile(fika_headless) else ""
        self.config["PATHS"]["fika_server_path"] = fika_server if os.path.isdir(fika_server) else ""

        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    # 获取版本号
    def get_version(self):
        tarkov_root = self.get_tarkov_root()  # 获取根路径
        version_file_path = os.path.join(tarkov_root, "SPT_Data", "Server", "configs", "core.json")

        # 检查文件是否存在
        if os.path.isfile(version_file_path):
            try:
                with open(version_file_path, "r") as file:
                    data = json.load(file)  # 解析 JSON 文件
                    return data.get("sptVersion", "未知版本")  # 返回 sptVersion，若找不到返回 "未知版本"
            except (json.JSONDecodeError, IOError) as e:
                print(f"读取或解析文件时出错: {e}")
                return "未知版本"
        else:
            print(f"文件不存在: {version_file_path}")
            return "未知版本"

    def get_fika_version(self):
        tarkov_root = self.get_tarkov_root()  # 获取根路径
        version_file_path = os.path.join(tarkov_root, "user", "mods", "fika-server", "package.json")

        if os.path.isfile(version_file_path):
            try:
                with open(version_file_path, "r") as file:
                    data = json.load(file)  # 解析 JSON 文件
                    return data.get("version", "未知版本")  # 返回 sptVersion，若找不到返回 "未知版本"
            except (json.JSONDecodeError, IOError) as e:
                print(f"读取或解析文件时出错: {e}")
                return "未知版本"
