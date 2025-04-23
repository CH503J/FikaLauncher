import os
import shutil
import time
import tarfile


def backup_files(file_path, backup_path, max_backups=10, backup_threshold=10):
    """
    备份指定文件到目标备份目录，并在超过备份次数时压缩备份文件
    :param file_path: 需要备份的文件路径
    :param backup_path: 备份目标文件夹
    :param max_backups: 最多保留的备份数量，超出时删除最早的备份
    :param backup_threshold: 触发压缩的备份数量（默认10）
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

    # 获取备份目录中的所有备份文件
    existing_backup_files = os.listdir(backup_path)

    # 判断是否是首次备份，首次备份时使用 .bak 后缀
    backup_file_name = f"{file_name_without_extension}.bak" if not any(file_name_without_extension in f for f in existing_backup_files) else f"{file_name_without_extension}_{time.strftime('%Y%m%d_%H%M%S', time.localtime())}{extension}"

    # 拼接出完整的备份文件路径
    backup_file_path = os.path.join(backup_path, backup_file_name)

    # 复制文件到备份目录
    shutil.copy(file_path, backup_file_path)
    print(f"文件 {file_path} 已备份到 {backup_file_path}")

    # 获取备份文件的创建时间并排序
    existing_backup_files = sorted(
        [(f, os.path.getctime(os.path.join(backup_path, f))) for f in os.listdir(backup_path)],
        key=lambda x: x[1]
    )

    # 管理备份次数：如果备份文件超过最大备份数，删除最早的一个
    if len(existing_backup_files) >= max_backups:
        # 如果备份次数达到 threshold，进行压缩
        if len(existing_backup_files) >= backup_threshold:
            # 仅选择包含时间戳的备份文件进行打包
            backup_files_to_compress = [
                f for f, _ in existing_backup_files if time.strftime("%Y%m%d_%H%M%S", time.localtime(_)) in f
            ]

            # 如果有足够的文件进行压缩
            if len(backup_files_to_compress) >= backup_threshold:
                earliest_timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime(os.path.getctime(os.path.join(backup_path, backup_files_to_compress[0]))))
                latest_timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime(os.path.getctime(os.path.join(backup_path, backup_files_to_compress[-1]))))

                # 压缩包命名
                compressed_backup_name = f"{file_name_without_extension}_{earliest_timestamp}_{latest_timestamp}.tar.gz"
                compressed_backup_path = os.path.join(backup_path, compressed_backup_name)

                # 创建 tar.gz 压缩包
                with tarfile.open(compressed_backup_path, "w:gz") as tar:
                    for file in backup_files_to_compress:
                        file_to_add = os.path.join(backup_path, file)
                        tar.add(file_to_add, arcname=file)
                        os.remove(file_to_add)  # 压缩后删除这些文件

                print(f"备份文件已经打包成压缩包：{compressed_backup_path}")

        # 删除超出最大备份数的最早备份文件（如果未被打包的文件）
        for file, _ in existing_backup_files[:len(existing_backup_files) - max_backups]:
            backup_file_path_to_delete = os.path.join(backup_path, file)
            if not file.endswith(".bak"):
                os.remove(backup_file_path_to_delete)
                print(f"删除最早的备份文件: {backup_file_path_to_delete}")

    return backup_file_path
