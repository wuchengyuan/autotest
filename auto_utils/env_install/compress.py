#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
压缩包处理模块
1、去掉压缩包中的Web.config文件
2、去掉压缩包中的多级文件夹
"""


import shutil
from auto_utils.common import *


class Compress:
    def __init__(self):
        self.cfg = get_config()
        self.l_path = get_project_path() + 'auto_utils/env_install/software/'
        self.filename = self.cfg['svn']['filename'].decode('utf-8')
        self.l_file = self.l_path + self.filename

    @staticmethod
    def os_command(command):
        """
        执行dos命令
        :param command: dos命令
        :return:获取系统返回的信息
        """
        info = os.popen(command)
        # print command.decode('gbk')
        return info.read().decode('gbk')

    def zip_path(self):
        """
        查看压缩包内是否存在多级文件夹
        :return:返回最终的需要压缩文件的路径
        """
        l_file = self.l_file.encode('gbk')
        regex = re.compile(r':\d{2}\s{2}(.+)?\\bin\\')
        if re.match('(.+)\.rar$', l_file):
            info = self.os_command('UnRAR l %s' % l_file)
            folder = regex.search(info)
        else:
            info = self.os_command('UnZIP -l %s' % l_file)
            folder = regex.search(info)
        if folder:
            return self.l_path + 'zip/' + folder.group(1)
        else:
            return self.l_path + 'zip/'

    def unzip(self):
        """
        解压缩包中文件，调用dos的unrar和unzip命令
        要求c://windows目录下存在unrar.exe和unzip.exe文件
        :return:None
        """
        l_file = self.l_file.encode('gbk')
        z_path = (self.l_path + 'zip/').encode('gbk')
        if os.path.isdir(z_path):
            shutil.rmtree(z_path)
        os.mkdir(z_path)
        if re.match('(.+)\.rar$', l_file):
            self.os_command('UnRAR x %s %s' % (l_file, z_path))
        else:
            # print 'UnZIP -o %s %s' % (l_file, z_path)
            self.os_command('UnZIP -x %s -d %s' % (l_file, z_path))

    def del_file(self, name):
        """
        删除文件方法，调用dos中的del命令，只删除软件根目录下的Web.config
        不删除Views目录下的web.config文件
        :param name: 文件名
        :return:None，用于跳出多级循环
        """
        for info in os.walk(self.l_path + 'zip'):
            for filename in info[2]:
                if name == filename:
                    if info[0].find('Views') == -1:
                        os.remove(info[0] + '/' + filename)
                        return

    def update_zip(self):
        """
        创建新的zip文件，供外部模块调用
        1、删除Web.config文件
        2、压缩成一份新的不包含多级目录的.zip文件
        :return:
        """
        print('开始更新压缩文件!')
        self.unzip()
        self.del_file('Web.config')
        folder = self.zip_path().encode('gbk')
        file_name = os.path.splitext(self.filename)[0]
        zip_file_path = self.l_path + file_name + '.zip'
        if os.path.isfile(zip_file_path):
            os.remove(zip_file_path)
        self.os_command(r'cd /d %s && zip -r9 %s ./' % (folder, zip_file_path.encode('gbk')))
        print('压缩文件更新完成!')


if __name__ == '__main__':
    c = Compress()
    c.update_zip()
