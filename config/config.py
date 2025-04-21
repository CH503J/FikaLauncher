# config.py

import os
import configparser


class ConfigManager:
    def __init__(self, config_path="config/config.ini"):
        self.root = None
        self.port_var = None
        self.ip_var = None
        self.headless_path_var = None
        self.server_path_var = None
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
            "server_path": "",
            "headless_path": ""
        }
        self.config["NETWORK"] = {
            "ip": "127.0.0.1",
            "port": "6969"
        }
        self.config["GUI"] = {
            "window_size": "700x600"
        }
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def get_server_path(self):
        return self.config.get("PATHS", "server_path", fallback="")

    def get_headless_path(self):
        return self.config.get("PATHS", "headless_path", fallback="")

    def get_ip(self):
        return self.config.get("NETWORK", "ip", fallback="127.0.0.1")

    def get_port(self):
        return self.config.get("NETWORK", "port", fallback="6969")

    def get_window_size(self):
        return self.config.get("GUI", "window_size", fallback="700x600")

    def update_config(self, server_path=None, headless_path=None, ip=None, port=None, window_size=None):
        if server_path is not None:
            self.config["PATHS"]["server_path"] = server_path
        if headless_path is not None:
            self.config["PATHS"]["headless_path"] = headless_path
        if ip is not None:
            self.config["NETWORK"]["ip"] = ip
        if port is not None:
            self.config["NETWORK"]["port"] = port
        if window_size is not None:
            self.config["GUI"]["window_size"] = window_size

        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)
