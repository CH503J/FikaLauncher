import os


def is_valid_tarkov_root(path: str) -> bool:
    """
    判断是否为有效的塔科夫根目录：
    1. 路径必须存在且是文件夹；
    2. 必须包含 SPT.Server.exe、SPT.Launcher.exe 和 EscapeFromTarkov.exe 三个文件。
    """
    if not os.path.isdir(path):
        return False

    required_files = [
        "SPT.Server.exe",
        "SPT.Launcher.exe",
        "EscapeFromTarkov.exe",
    ]

    for filename in required_files:
        full_path = os.path.join(path, filename)
        if not os.path.isfile(full_path):
            return False

    return True
