#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
文件下载模块
1、读取配置文件获取Svn服务器、软件基础信息
2、根据基础信息递归查找文件全路径
3、根据全路径从SVN下载软件
"""


import sys
import urllib.request
import re
import ssl
import os
from auto_utils import common


class Download:
    def __init__(self):
        self.cfg = common.get_config()
        self.path = common.get_project_path()
        self.username = self.cfg['svn']['user']
        self.password = self.cfg['svn']['password']
        self.realm = 'VisualSVN Server'
        self.file_url = None

    def url_read(self, url):
        """
        http页面读取方法
        :param url:
        :return:str
        """
        # 关闭ssl验证
        ssl._create_default_https_context = ssl._create_unverified_context
        auth = urllib.request.HTTPBasicAuthHandler()
        auth.add_password(self.realm, url, self.username, self.password)
        opener = urllib.request.build_opener(auth, urllib.request.CacheFTPHandler)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(url)
        return urllib.request.urlopen(req).read()

    def find_path(self, url, name):
        """
        根据基础路径和文件名查找文件路径
        :param url:
        :param name:
        :return:
        """
        url = url.rstrip("/")
        url = "%s/" % url
        html = self.url_read(url)
        flag = self.find_zip(html, name)
        if flag:
            self.file_url = url + name
        else:
            folders = self.find_folder(html)
            if len(folders) > 0:
                for folder in folders:
                    new_url = url + folder
                    self.find_path(new_url, name)
                    if self.file_url:
                        break

    @staticmethod
    def find_folder(html):
        """
        查找html页面中所有文件夹
        :param html: html页面
        :return:文件夹名称列表
        """
        folders = re.findall('<dir name="(.+)?" href', html)
        return folders

    @staticmethod
    def find_zip(html, name):
        """
        查找html页面中是否存在name
        :param html: html页面
        :param name: 文件名
        :return:bool
        """
        flag = html.find(name)
        if flag == -1:
            return False
        else:
            return True

    @staticmethod
    def view_bar(num=1, total=100):
        """
        进度条
        :param num:
        :param total:
        :return:None
        """
        rate = float(num) / float(total)
        rate_num = int(rate * 100)
        bar_num = int(rate * 50)
        bar_word = "#" * bar_num
        sys.stdout.write('\r' + '%d' % rate_num + "%" + "%s" % bar_word)
        sys.stdout.flush()

    def download_file(self):
        """
        根据配置文件下载文件
        :return:
        """

        base_url = self.cfg['svn']['base_url']
        file_name = self.cfg['svn']['filename']
        self.find_path(base_url, file_name)
        folder_name = self.path + 'auto_utils/env_install/software/'
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        local_path = folder_name + file_name.decode('utf-8')
        if os.path.isfile(local_path):
            os.remove(local_path)
        data = urllib2.urlopen(self.file_url)
        print('文件开始下载!')
        file_size = data.headers['content-length']
        rec_data = 0
        while True:
            buf = data.read(32768)
            rec_data += len(buf)
            self.view_bar(rec_data, file_size)
            if buf:
                with open(local_path, 'ab') as f:
                    f.write(buf)
            else:
                break
        print("\n文件下载完成!")

if __name__ == '__main__':
    d = Download()
    d.download_file()
