#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
软件安装模块，
1、本地执行下载、压缩文件处理、软件上传服务器
2、远程服务器备份已安装的软件、替换新的安装软件、删除上传文件、重启IIS服务
3、数据库脚本执行在通过统一调度时执行，本模块不再开发数据库方法
"""


from auto_utils.env_install.compress import Compress
from auto_utils.env_install.download import Download
from auto_utils.env_install.os_connect import OsConnect
from auto_utils.common import *


class Install:
    def __init__(self):
        self.cfg = None

    def install(self):
        """
        外部调用该方法即可完成软件安装
        :return:None
        """
        self.cfg = get_config()
        filename = os.path.splitext(self.cfg['svn']['filename'])[0] + '.zip'
        Download().download_file()
        Compress().update_zip()
        o = OsConnect()
        o.upload(filename)
        filename_gbk = filename.decode('utf-8').encode('gbk')
        path_gbk = self.cfg['install_path'][self.cfg['svn']['moudle']].decode('utf-8').encode('gbk')
        o.exec_command(r'cmd.exe /c "zip -r C:\Users\wuchengyuan\backup\%s %s"' % (filename_gbk, path_gbk))
        print u'软件备份完毕！'
        o.exec_command(r'cmd.exe /c "cd ..&&unzip -o C:\Users\wuchengyuan\%s -d %s"' % (filename_gbk, path_gbk))
        print u'完成软件更新！'
        o.exec_command('cmd.exe /c "iisreset"')
        print u'重启iis服务！'
        o.exec_command(r'cmd.exe /c "cd ..&&del C:\Users\wuchengyuan\%s"' % filename_gbk)
        print u'删除上传文件！'

if __name__ == '__main__':
    i = Install()
    i.install()
