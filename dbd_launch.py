import os
import subprocess
import psutil
from time import sleep
import mouse
import time
import win32gui
import re
import pygetwindow as gw

WINDOW_NAME = "DeadByDaylight"
EAC_NAME="DeadByDaylight.exe"
EAC_WINDOW_NAME="Dead By Daylight"
PROCESS_NAME = "DeadByDaylight-Win64-Shipping.exe"
EXPIRE_TIME = 20


def is_process_responding(name=PROCESS_NAME):
    """Check if a program (based on its name) is responding"""
    cmd = 'tasklist /FI "IMAGENAME eq %s" /FI "STATUS eq running"' % name
    status = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read()
    return name[:-8] in str(status)


def kill_process(name=PROCESS_NAME):
    for proc in psutil.process_iter():
        # check whether the process to kill name matches
        if proc.name() == name:
            proc.kill()


def is_process_exist(name=PROCESS_NAME):
    for process in psutil.process_iter():
        if process.name() == name:
            return True
    return False


def is_eac_exit():
    return not is_process_exist(EAC_NAME)

def launch_dbd():
    retry_count = 0
    while True:
        kill_process()
        kill_process(EAC_NAME)
        sleep(5)
        os.startfile(r'steam://rungameid/381210')
        print("等待黎明杀鸡启动中")
        while not is_process_exist():
            sleep(2)
        # while len(gw.getWindowsWithTitle(WINDOW_NAME))==0:
        #     try:
        #         win = gw.getWindowsWithTitle(WINDOW_NAME)[0]
        #         win.activate()
        #         break
        #     except:
        #         continue
        while (not is_process_exist()):
            sleep(2)

        print("等待EAC退出")
        while (not is_eac_exit()) and is_process_exist():
            sleep(2)
        start_time = time.time()
        print("检测到黎明杀机，开始判断是否响应")
        while True:
            # win = gw.getWindowsWithTitle(WINDOW_NAME)[0]
            # win.activate()
            sleep(0.1)
            mouse.click()
            time_passed = time.time() - start_time
            if time_passed > EXPIRE_TIME and (not is_process_responding()):
                print("黎明杀机在20秒内无响应，关闭重新打开！")
                kill_process()
                break
            else:
                if is_process_responding() and is_process_exist():
                    sleep(5)
                    break
        # 检测黎明杀鸡是否打开并且正在运行
        # sleep(5)
        

        mouse.click()

        if is_process_responding() and is_process_exist():
            print(f"黎明杀鸡正在运行，启动程序退出，尝试了{retry_count}次")
            break
        retry_count += 1
        #     break
        # break


if __name__ == "__main__":
    launch_dbd()
