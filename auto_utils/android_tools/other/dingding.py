# coding:utf-8
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from android_driver import *
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
desired_caps['deviceName'] = 'ec3097c9'
desired_caps['appPackage'] = 'com.alibaba.android.rimet'
desired_caps['appActivity'] = '.biz.SplashActivity'
# desired_caps['newCommandTimeout'] = '15'
desired_caps['unicodeKeyboard'] = True
desired_caps['resetKeyboard'] = True
# desired_caps["chromeOptions"] = {'androidProcess': 'com.tencent.mm:tools'}
desired_caps['noReset'] = True
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# driver.find_element_by_id('com.alibaba.android.rimet:id/et_pwd_login').send_keys('wucy123456')
# driver.find_element_by_id('com.alibaba.android.rimet:id/btn_next').click()
driver.find_element_by_xpath('//android.widget.TextView[@text=\"工作\"]').click()
driver.find_element_by_xpath('//android.widget.TextView[@resource-id=\"com.alibaba.android.rimet:id/oa_entry_title\" and @text=\"考勤打卡\"]').click()
driver.find_element_by_xpath('//android.view.View[@content-desc=\"下班打卡\"]').click()