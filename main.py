"""
Fika Headless开服器
1. 一键启动、关闭、重启
2. 修改服务端数据

项目目标
1. 一键启动、关闭、重启
2. 修改服务端数据
3. 专属gui
4. 保存gui、用户配置记录（config）
5. 服务端日志记录（cache）
"""
# main.py
import tkinter as tk
from gui.gui_launch import TarkovLauncherGUI


def main():
    root = tk.Tk()
    # app = TarkovLauncherGUI(root)
    TarkovLauncherGUI(root)
    root.mainloop()
    print("Fika启动器")


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()
