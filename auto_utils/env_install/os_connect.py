#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Window操作模块
1、通过SSH协议实现对dos进行操作
2、可执行单条dos命令
3、可执行多条dos命令
4、可上传文件到服务器
"""


import paramiko
from auto_utils import common
import os


class OsConnect:
    def __init__(self):
        self.cfg = common.get_config()
        self.ip = self.cfg['windows']['ip']
        self.username = self.cfg['windows']['user']
        self.password = self.cfg['windows']['password']
        self.port = int(self.cfg['windows']['port'])

    def exec_command(self, command):
        """
        连接远程服务器，发送dos命令操作服务器
        :param command: dos命令：'cmd.exe /c "unzip -o E:\wcy\config1.zip -d E:\wcy"'
        :return:None
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, self.port, self.username, self.password, timeout=5)
        std_in, std_out, std_err = ssh.exec_command(command)
        out_info = std_out.read()
        # print out_info
        ssh.close()
        # print out_info.decode('gbk')

    def upload(self, file_name):
        """
        上传文件到远程服务器
        :param file_name: 文件名称，上传文件路径在software目录
        :return:None
        """
        print u'开始上传文件！'
        file_name = file_name.decode('utf-8')
        l_path = common.get_project_path() + 'auto_utils/env_install/software/' + file_name
        r_path = '/' + file_name
        t = paramiko.Transport((self.ip, self.port))
        t.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(l_path, r_path)
        t.close()
        print u'文件上传完毕！'

    def download(self, remote_dir, local_dir, f=None):
        """
        从服务器下载文件
        :param moudle:
        :return:
        """
        try:
            t = paramiko.Transport((self.ip, self.port))
            t.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            if not os.path.exists(local_dir):
                os.mkdir(local_dir)
            if f is not None:
                files = [].append(f)
            else:
                files = sftp.listdir(remote_dir)
            for f in files:
                print 'Downloading file:', os.path.join(remote_dir, f)
                sftp.get(os.path.join(remote_dir, f), os.path.join(local_dir, f))
            t.close()
        except Exception, e:
               print "download error,%s!" % e

    def exec_commands(self, commands, sec=3):
        """
        执行多条命令，commands=[]
        :param commands: []
        :param sec: 超时时间
        :return:None
        """
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(self.ip, self.port, self.username, self.password, timeout=5)
        ssh = s.invoke_shell()
        ssh.settimeout(sec)
        for command in commands:
            print u'执行%s命令。' % command
            ssh.send(command)
            out = ssh.recv(1024)
            print out


if __name__ == '__main__':
    o = OsConnect()
    print o.exec_command(r'cmd.exe /c dir')
    # o.download('/backup', '/')
