# -*-coding:utf-8 -*-
import os
import subprocess
# 获取所有连接的设备
from time import sleep

from MonkeyTest.Common import log


def exist_file(f_p):
    return os.path.exists(f_p)


# 返回当前所有的包
def get_all_packages():
    list_packs = []
    data = os.popen("adb shell pm list packages ").read()
    list_d = data.split("\n")
    for d in list_d:
        d_s = d.replace("package:", "")
        list_packs.append(d_s)
    return list_packs


# 获取手机系统时间
def get_phone_time(device):
    data = os.popen("adb -s {} shell date".format(device)).read()
    data = data.strip("\n")
    return data


# 获取所有连接的设备
def get_devices():
    ret = os.popen('adb devices').readlines()
    device_lists = []
    for item in ret:
        if '\tdevice\n' in item:
            device_lists.append(item[:item.index('\t')])
    return device_lists


# 获取当前运行apk的包名
def currentRunPackage(device):
    return os.popen("adb -s {} shell dumpsys window | findstr mCurrentFocus".format(device)).read()


# 启动app
def startApp(device, appPackageName, appPackageActive):
    os.popen("adb -s {} root".format(device))
    os.popen("adb -s {} shell am start -n {}/{}".format(device, appPackageName, appPackageActive))


# 滑动
def slipFun(device):
    os.popen("adb -s " + device + " shell input swipe 1500 960 1500  450")


# 判断屏幕亮灭状态
def is_screenState(device):
    try:
        cmd = 'adb -s ' + device + ' shell dumpsys power | findstr "Display Power: state="'
        res = os.popen(cmd).read()
        if "mHoldingDisplaySuspendBlocker=true" in res:
            return True
        else:
            return False
    except Exception as e:
        print('获取手机屏幕点亮状态异常', e)
        return False


# 亮屏进入主页面
def lightScreen(device):
    os.popen("adb -s " + device + " shell input keyevent 224")
    sleep(1)
    slipFun(device)


# 判断mcu个数
def mcu_count_fun():
    data = os.popen("adb shell getevent -i").readlines()
    times = 0
    for item in data:
        if "add device" in item:
            times = times + 1
    return times


# 截图
def screen_cut_fun(device, path):
    data = get_phone_time(device)
    data_list = data.split(" ")
    temp = data_list[3].replace(":", "-")
    data_list[3] = temp
    pic_name = data_list[3]
    print(pic_name)
    # 进行截图
    cut_cmd = "adb -s " + device + " shell screencap -p /sdcard/" + pic_name + ".png"
    os.system(cut_cmd)
    # 获取截图照片
    get_cmd = "adb -s " + device + " pull /sdcard/" + pic_name + ".png " + path
    res = os.popen(get_cmd).read()
    if "1 file pulled" in res:
        return True
    else:
        return False


def stop_monkey(device):
    cmd_v = os.popen('adb -s {} shell ps | findstr monkey'.format(device))
    data = cmd_v.readline()
    if not data:
        return False
    # 杀死monkey进程
    os.popen("adb -s {} kill {}".format(device, data[13:18]))
    return True


# 执行系统Monkey
def do_monkey(device_m, event_times, log_rank, delay_time, type_m, event_list, pack=None, logger=None):
    # adb -s HA1WQRBK shell monkey --pct-touch 10 --pct-motion 20 --throttle 100 -v-v-v 500

    if type_m == "系统测试":
        str_sys_adb = "adb -s " + device_m + " shell monkey " + " ".join(event_list) + " --throttle " + str(
            delay_time) + " " + log_rank + " " + str(event_times)
        cmd_p = subprocess.Popen(str_sys_adb, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        str_pack_adb = "adb -s " + device_m + " shell monkey " + "-p " + pack + " " + " ".join(
            event_list) + " --throttle " + str(delay_time) + " " + log_rank + " " + str(event_times)
        print(str_pack_adb)
        cmd_p = subprocess.Popen(str_pack_adb, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(cmd_p.stdout.readline, b''):
        line = line.strip().decode("GB2312")
        logger.info(line)
        print(line)
    return True


if __name__ == '__main__':
    # flag = screen_cut_fun(device="01234ABC", path=r"D:\result")
    # device = get_devices()[0]
    # print(device)
    file_path = "D:\\log\\"
    logger = log.Logger("monkeyTestLog", FilePath=file_path, device="HA1WQRBK", log_type="app")
    # is_exists = exist_file(file_path)
    # do_monkey("HA1WQRBK", 500, "-v-v-v", 200, "系统测试", ['--pct-touch 10', '--pct-motion 20'], logger=logger)
    stop_monkey(device='HA1WQRBK')