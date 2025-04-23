import os
import shutil
import time


def backup_files(file_path, backup_path):
    """
    备份指定文件到目标备份目录
    :param file_path: 需要备份的文件路径
    :param backup_path: 备份目标文件夹
    :return: 返回备份后的文件路径
    """
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，无法进行备份")
        return None

    # 确保备份目录存在
    os.makedirs(backup_path, exist_ok=True)

    # 获取文件名和扩展名
    file_name = os.path.basename(file_path)
    file_name_without_extension, extension = os.path.splitext(file_name)

    # 判断是否是首次备份
    existing_backup_files = os.listdir(backup_path)
    if not any(file_name_without_extension in f for f in existing_backup_files):
        # 首次备份，使用 .bak 后缀
        backup_file_name = f"{file_name_without_extension}.bak"
    else:
        # 后续备份，使用时间戳
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        backup_file_name = f"{file_name_without_extension}_{timestamp}{extension}"

    # 拼接出完整的备份文件路径
    backup_file_path = os.path.join(backup_path, backup_file_name)

    # 复制文件到备份目录
    shutil.copy(file_path, backup_file_path)
    print(f"文件 {file_path} 已备份到 {backup_file_path}")

    return backup_file_path


