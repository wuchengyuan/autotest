#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from auto_utils.common import *


def call_adb(cmd):
    """
    adb用命执行方法，返回命令执行返回结果信息
    :param cmd: adb命令
    :return:命令返回结果
    """
    info = subprocess.check_output(cmd)
    return info


def call_cmd(cmd):
    """
    cmd命令执行方法，根据返回结果记录日志
    :param cmd:cmd命令
    :return:None
    """
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        logging.info(result.stdout.decode('gbk').strip())
    else:
        logging.error(result.stderr.decode('gbk').strip())


def get_devices():
    """
    获取已连接到电脑的所有设备的device id，以列表形式返回
    :return:device id 列表
    """
    info_list = call_adb('adb devices').decode().split('\n')
    devices = [d.replace('\tdevice\r', '') for d in info_list if d.find('\tdevice') != -1]
    if devices:
        return devices


def reboot(device=None):
    """
    手机重启方法，参数device：
    1、如果为空,重启连接电脑的所有手机，
    2、如果为列表，则重启列表中所有手机，
    3、如果为单个id，则只重启该手机
    :param device: None,list,str
    :return:None
    """
    if not device:
        call_adb('adb reboot')
    elif isinstance(device, list):
        for device_id in device:
            call_adb('adb reboot %s' % device_id)
    else:
        call_adb('adb reboot %s' % device)


def screen_on():
    devices = get_devices()
    for device in devices:
        cmd = "adb -s " + device + " shell dumpsys power "
        info = call_adb(cmd).decode()
        result = re.search('mHoldingDisplaySuspendBlocker=(.+)', info).group(1).strip()
        if result == 'false':
            call_adb('adb shell input keyevent 26')


def push(local, remote):
    """
    将电脑文件拷贝到手机里面
    :param local:
    :param remote:
    :return:
    """
    info = call_adb("push %s %s" % (local, remote))
    return info


def pull(remote, local):
    """
    将手机数据拷贝到本地
    :param remote:
    :param local:
    :return:
    """
    result = call_adb("pull %s %s" % (remote, local))
    return result


def sync(directory, **kwargs):
    """
    同步更新 很少用此命名
    :param directory:
    :param kwargs:
    :return:
    """
    command = "sync %s" % directory
    if 'list' in kwargs:
        command += " -l"
        result = call_adb(command)
        return result


def get_app_pid(pkg_name):
    """
    根据包名得到进程id
    :param pkg_name:
    :return:
    """
    string = call_adb("shell ps | grep "+pkg_name)
    if string == '':
        return "the process doesn't exist."
    result = string.split(" ")
    return result[4]


def get_phone_info(device):
    """
    获取手机的版本、型号、品牌、设备信息
    :param device: 设备id
    :return:dict
    """
    cmd = "adb -s " + device + " shell cat /system/build.prop "
    info = call_adb(cmd).decode()
    release = re.search('ro.build.version.release=(.+)', info).group(1).strip()  # 版本
    model = re.search('ro.product.model=(.+)', info).group(1).strip()  # 型号
    brand = re.search('ro.product.brand=(.+)', info).group(1).strip()  # 品牌
    device = re.search('ro.product.device=(.+)', info).group(1).strip()  # 设备名
    return dict(release=release, model=model, brand=brand, device=device)


def get_platform_version(device):
    cmd = "adb -s %s shell getprop ro.build.version.release" % device
    version = call_adb(cmd).decode().strip()
    return version


def get_phone_mem(device):
    """
    获取手机最大运行内存
    :param device: 设备id
    :return:int
    """
    cmd = "adb -s " + device + " shell cat /proc/meminfo"
    info = call_adb(cmd).decode()
    memory_total = re.search('MemTotal(.+)kB', info).group(1).strip()
    return int(memory_total)


def get_cpu_num(device):
    """
    获取手机的CPU核数
    :param device: 设备id
    :return:str
    """
    cmd = "adb -s " + device + " shell cat /proc/cpuinfo"
    info = call_adb(cmd).decode()
    cpu_num = re.findall('processor(.+)\r\r\n', info)
    return str(len(cpu_num)) + "核"


def get_phone_pix(device):
    """
    获取手机分辨率
    :param device: 设备id
    :return:str
    """
    cmd = "adb -s " + device + " shell wm size"
    info = call_adb(cmd).decode()
    pix = re.search('Physical size:(.+)', info).group(1).strip()
    width, height = pix.strip().split('x')
    return int(width), int(height)


def get_pkg_path(pkg_name):
    """
    获取测试app文件路径
    :param pkg_name: app名字
    :return:str
    """
    apk_path = get_project_path() + 'data\\' + pkg_name
    result = os.path.isfile(apk_path)
    if result:
        return apk_path
    else:
        raise FileNotFoundError('data目录下不存在%s文件' % pkg_name)


def get_apk_info(pkg_name):
    """
    获取apk包名、版本名、版本
    :param pkg_name:apk全名，包含后缀.apk
    :return:dict
    """
    apk_path = get_pkg_path(pkg_name)
    cmd = 'aapt dump badging %s' % apk_path
    info = call_adb(cmd).decode()
    match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)'").match(info)
    if not match:
        raise Exception("can't get package info")
    package_name = match.group(1)
    version_code = match.group(2)
    version_name = match.group(3)
    return dict(package_name=package_name, version_name=version_name, version_code=version_code)


def get_apk_name(pkg_name):
    """
    获取apk应用名称
    :param pkg_name: apk全名，包含后缀.apk
    :return:str
    """
    apk_path = get_pkg_path(pkg_name)
    cmd = 'aapt dump badging %s' % apk_path
    info = call_adb(cmd).decode()
    match = re.compile("application-label:(\S+)").search(info)
    if match is not None:
        return match.group(1)


def get_apk_activity(pkg_name):
    """
    获取apk启动类
    :param pkg_name: apk全名，包含后缀.apk
    :return:str
    """
    apk_path = get_pkg_path(pkg_name)
    cmd = 'aapt dump badging %s' % apk_path
    info = call_adb(cmd).decode()
    match = re.compile("launchable-activity: name='(\S+)'").search(info)
    if match is not None:
        return match.group(1)
    else:
        raise ModuleNotFoundError('apk activity not found')


if __name__ == '__main__':
    get_apk_activity('weixin_1320.apk')
