#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import threading
from multiprocessing import Process
from auto_utils.android_tools.android_common import *


class AppiumServer(object):
    def __init__(self, configs):
        self.configs = configs

    def start_server(self):
        """
        appium服务启动
        :return:None
        """
        configs = self.configs
        for config in configs:
            cmd = "appium --session-override  -p %s -U %s" % (
                config.get("port"),  config.get("device"))
            device = config.get('device')
            t1 = RunServer(cmd, device)
            p = Process(target=t1.start())
            p.start()
            while True:
                url = "http://127.0.0.1:" + str(config.get("port")) + "/wd/hub/status"
                if self.server_is_running(url):
                    break

    @staticmethod
    def server_is_running(url):
        """
        根据url检测appium服务是否启动
        :param url: appium服务检查链接
        :return:bool
        """
        time.sleep(2)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logging.info('appium服务已启动：%s' % url)
                return True
            else:
                return False
        except requests.ConnectionError:
            logging.warning('appium服务未开启：%s' % url)
            return False

    @staticmethod
    def stop_server():
        """
        关闭appium服务
        :return:None
        """
        cmd = 'taskkill /f /im node.exe'
        call_cmd(cmd)


class RunServer(threading.Thread):
    def __init__(self, cmd, device, save_log=True):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.device = device
        self.save_log = save_log

    def run(self):
        if self.save_log:
            log_path = get_project_path() + 'result/appium_%s.log' % self.device
            cmd = self.cmd + '>%s' % log_path
        else:
            cmd = self.cmd
        logging.info('appium服务器开始启动：%s' % cmd)
        os.system(cmd)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    a = AppiumServer([{'port': 4732,  'device': 'ec3097c9'}])
    a.stop_server()
    a.start_server()
