#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from auto_utils.common import *


class Browser(object):
    def __init__(self):
        self.driver = None
        self.wait_time = int(get_config().get('project_config').get('page_load'))
        self._driver_path = os.path.dirname(__file__) + '/chromedriver.exe'

    def open_browser(self, browser):
        """
        打开浏览器
        :param browser: 浏览器类型(ie,firefox,chrome)
        """
        download_path = get_project_path() + 'download'
        if browser == "firefox":
            fp = webdriver.FirefoxProfile()            
            fp.set_preference("browser.download.folderList", 2)
            fp.set_preference("browser.download.manager.showWhenStarting", False)
            fp.set_preference("browser.download.dir", download_path)
            fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
            self.driver = webdriver.Firefox(firefox_profile=fp)            
        elif browser == "chrome":
            options = webdriver.ChromeOptions()
            pref = {"download.default_directory": download_path}
            options.add_experimental_option("prefs", pref)
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
            self.driver = webdriver.Chrome(executable_path=self._driver_path, chrome_options=options)
        elif browser == "ie":
            self.driver = webdriver.Ie()
        else:
            raise Exception(u'浏览器类型错误：%s' % browser)
        return self.driver

    def open(self, url, redirect_title=None):
        """
        #如果open之前的操作会导致页面重定向时，有可能会出现页面实际跳转的为重定向页面
        打开网址
        :param url: 网址
        """
        if redirect_title:
            end_time = time.time() + self.wait_time
            while True:
                title = self.get_title()
                if title == redirect_title:
                    logging.info(u'页面已完成重定向，重定向title：%s' % title)
                    self.driver.get(url)
                    return
                else:
                    logging.warning(u'页面未完成重定向！')
                    time.sleep(3)
                if time.time() > end_time:
                    self.driver.get(url)
                    break
        else:
            self.driver.get(url)

    def window_maximize(self):
        """
        浏览器最大化
        """
        self.driver.maximize_window()

    def set_window(self, width, height):
        """
        设定浏览器宽高
        :param width: 宽度
        :param height: 高度
        """
        self.driver.set_window_size(width, height)

    def close(self):
        """
        关闭当前页面
        """
        self.driver.close()

    def quit(self):
        """
        退出浏览器
        """
        self.driver.quit()
        os.system(r'taskkill /f /im chromedriver.exe >nul 2>nul')  # 处理chrome退出后进程不能结束的问题

    def refresh(self):
        """
        刷新当前页面
        """
        self.driver.refresh()

    def forward(self):
        """
        前进
        """
        self.driver.forward()

    def back(self):
        """
        后退
        """
        self.driver.back()

    def get_url(self, key=None):
        """
        获取当前页面的url
        :return: url
        """
        url = self.driver.current_url
        if key:
            global_var[key] = url
        return url

    def get_title(self, key=None):
        """
        获取当前页面的title
        :return: title
        """
        title = self.driver.title.strip()
        if key:
            global_var[key] = title
        return title

    def screen_shot(self, case_id):
        """
        截图
        :return: 截图文件名
        """
        file_name = case_id + '__' + time.strftime("%Y-%m-%d") + '.png'
        image_path = get_project_path() + 'result/web_log/image/'
        if not os.path.isdir(image_path):
            os.mkdir(image_path)
        image_file = '%s%s' % (image_path, file_name)
        self.driver.save_screenshot(image_file)

    def web_esc(self):
        """
        对浏览器发送ESC键
        """
        ActionChains(self.driver).send_keys(Keys.ESCAPE)

    def alert_accept(self):
        """
        浏览器警告信息确定
        :return:
        """
        alert = self.driver.switch_to_alert()
        alert.accept()

    def alert_dismiss(self):
        """
        浏览器警告信息取消
        :return:
        """
        alert = self.driver.switch_to_alert()
        alert.dismiss()
if __name__ == '__main__':
    bro = Browser()
    bro.open_browser('chrome')
