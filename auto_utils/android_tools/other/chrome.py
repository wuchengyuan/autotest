# coding:utf-8

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
desired_caps['deviceName'] = 'ec3097c9'
# desired_caps['appPackage'] = 'com.tencent.mm'
# desired_caps['appActivity'] = '.ui.LauncherUI'
# desired_caps['newCommandTimeout'] = '15'
desired_caps['unicodeKeyboard'] = 'True'
desired_caps['resetKeyboard'] = 'True'
# desired_caps["chromeOptions"] = {'androidProcess': 'com.tencent.mm:tools'}
desired_caps['noReset'] = 'True'
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.get('http://qlcqd.test.jkt.guahao-inc.com/Register/hosList')
time.sleep(5)


driver.find_element_by_css_selector('#area_hos_list > div:nth-child(3) > a').click()
# driver.find_element_by_id('search_val').send_keys('456')
# time.sleep(3)
# driver.execute_script("$('#search_val').val('134')")
# time.sleep(2)
# driver.find_element_by_id('search_val').send_keys('456')
# time.sleep(2)
# print driver.page_source
# driver.execute_script("$('#search_val').trigger('touchstart')")
# driver.find_element_by_id('search_val').send_keys('456')
# driver.execute_script("$('#search_val').trigger('touchstart')")

