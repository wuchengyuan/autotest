#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_utils.env_install.install import Install
from auto_utils.env_install.os_connect import OsConnect
from auto_utils.common import *

connect = OsConnect()
moudle_names = ['wap_front', 'wap_admin', 'batch_job', 'hos_serve', 'pay_manag', 'pay_admin']


def download_log(moudle):
    local_path = get_project_path() + 'auto_utils/env_install/software/' + moudle
    remote_path = get_config()['log_path'][moudle]
    connect.download(remote_path, local_path)


def auto_install():
    err = None
    try:
        connect.exec_command('cmd.exe /c "dir"')
    except Exception, e:
        err = e
        print u'请确认服务器是否开启SSH服务：%s' % err
    if not err:
        while True:
            command = raw_input(u'请选择要进行的操作：\n1、版本更新\n2、跑批重启\n3、日志读取\n4、退出操作\n'
                                .encode('gbk'))
            if command == '1':
                moudle = raw_input(u'选择需要安装的服务：\n1、WAP 前端\n2、WAP 后台\n3、跑批服务\n4、医院服务\n'
                                   u'5、支付后台\n6、支付平台\n'.encode('gbk'))
                set_config('svn', 'moudle', moudle_names[int(moudle)-1])
                zip_name = raw_input(u'输入需要更新的包名：\n'.encode('gbk'))
                set_config('svn', 'filename', zip_name.decode('gbk').encode('utf-8'))
                if moudle == '3':
                    connect.exec_command('cmd.exe /c "taskkill -f /im HWP.BusinessBatch.exe"')
                    time.sleep(3)
                    print u'跑批服务已停止！'
                i = Install()
                i.install()
            elif command == '2':
                connect.exec_command('cmd.exe /c "taskkill -f /im HWP.BusinessBatch.exe"')
                time.sleep(3)
                print u'跑批服务已停止！'
                connect.exec_command('cmd.exe /c "net start Hwp.Scheduler"')
                time.sleep(3)
                print u'跑批服务已启动！'
            elif command == '3':
                moudle = raw_input(u'选择需要读取日志的服务：\n1、WAP 前端\n2、WAP 后台\n3、跑批服务\n4、医院服'
                                   u'务\n5、支付后台\n6、支付平台\n7、删除日志\n'.encode('gbk'))
            elif command == '4':
                break
if __name__ == '__main__':
    try:
        auto_install()
    except Exception, e:
        print e
    raw_input(u'按回车键结束！'.encode('gbk'))
