# coding:utf-8

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
desired_caps['deviceName'] = '25b389ad'
desired_caps['appPackage'] = 'com.eg.android.AlipayGphone'
desired_caps['appActivity'] = '.AlipayLogin'
desired_caps['newCommandTimeout'] = '15'
desired_caps['unicodeKeyboard'] = 'True'
desired_caps['resetKeyboard'] = 'True'
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(time_to_wait="15")
time.sleep(3)
cons = driver.contexts
print driver.current_context
time.sleep(3)
for con in cons:
    try:
        print driver.current_context
        driver.switch_to.context(con)
        driver.find_element_by_id('com.alipay.mobile.base.commonbiz:id/search_button').click()
    except Exception, e:
        print e
# driver.find_element_by_tag_name('全流程测试').click()

# new UiSelector().className(\"android.widget.Button\").textContains(\"蚂蚁森林\").resourceId(\"com.alipay.mobile.base.commonbiz:id/search_button\")