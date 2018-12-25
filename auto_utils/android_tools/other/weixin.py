# coding:utf-8

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.0'
desired_caps['deviceName'] = 'GSL7N16B09001809'
desired_caps['appPackage'] = 'com.tencent.mm'
desired_caps['appActivity'] = '.ui.LauncherUI'
# desired_caps['newCommandTimeout'] = '15'
desired_caps['unicodeKeyboard'] = True
desired_caps['resetKeyboard'] = True
desired_caps["chromeOptions"] = {'androidProcess': 'com.tencent.mm:tools'}
desired_caps['noReset'] = True
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
print driver.contexts
time.sleep(6)
driver.find_element_by_xpath('//android.widget.TextView[@text=\"通讯录\"]').click()
time.sleep(2)
driver.find_element_by_xpath('//android.widget.TextView[@text=\"公众号\"]').click()
time.sleep(2)
driver.find_element_by_xpath('//android.widget.TextView[@content-desc=\"搜索\"]').click()
# time.sleep(2)
driver.find_element_by_id('com.tencent.mm:id/h9').send_keys(u'微医')
driver.find_element_by_xpath('//android.widget.TextView[@text=\"微医集团全流程测试\"]').click()
time.sleep(2)
driver.find_element_by_xpath('//android.widget.TextView[@text=\"预约挂号\"]').click()
driver.find_element_by_xpath('//android.widget.TextView[@text=\"预约挂号\"]').click()
time.sleep(6)
print driver.contexts
driver.switch_to.context(u'WEBVIEW_com.tencent.mm:tools')
print driver.current_context


# driver.find_element_by_id('search_val').send_keys('456')
# driver.execute_script("$('#search_val').val('134')")
print driver.page_source
driver.execute_script("$('#search_val').trigger('touchstart')")
time.sleep(2)
driver.find_element_by_id('search_val').send_keys('456')

# time.sleep(3)
# print driver.current_context
# print driver.page_source
# driver.execute_script("$('#search_val').val('134')")
#
# driver.find_element_by_xpath('//*[@id="area_hos_list"]/div[2]/a').click()
# driver.find_element_by_css_selector('#area_hos_list > div:nth-child(2) > a').click()
# driver.find_element_by_css_selector('#hosModPanel > dl > a').click()