#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Android基本方法操作模块
"""
import random
from appium import webdriver
from auto_utils.android_tools.appium_server import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from selenium.common.exceptions import TimeoutException


class By(object):
    """
    Set of supported locator strategies
    """

    id = "id"
    xpath = "xpath"
    link = "link text"
    plink = "partial link text"
    name = "name"
    tag = "tag name"
    cls = "class name"
    css = "css selector"
    aid = 'accessibility id'
    ui = '-android uiautomator'


class AndroidDriver:
    def __init__(self):
        self.driver = None
        self.device = None
        self.wait_time = int(get_config().get('project_config').get('page_load'))

    def open_app(self, pkg_name):
        """
        app启动方法
        :param pkg_name: app名字
        :return:webdriver
        """
        screen_on()
        self.device = device = get_devices()[0]
        port = str(random.randint(4700, 4900))
        app_server = AppiumServer([dict(device=device, port=port)])
        app_server.stop_server()
        app_server.start_server()
        desired_caps = dict()
        desired_caps['appPackage'] = get_apk_info(pkg_name).get('package_name')
        desired_caps['appActivity'] = get_apk_activity(pkg_name)
        desired_caps['app'] = get_project_path() + '/data/' + pkg_name
        desired_caps['platformVersion'] = get_platform_version(device)
        desired_caps['platformName'] = 'Android'
        # desired_caps["automationName"] = 'selendroid'
        desired_caps['deviceName'] = device
        desired_caps["noReset"] = "True"
        desired_caps['noSign'] = "True"
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        desired_caps["systemPort"] = str(port)
        desired_caps["recreateChromeDriverSessions"] = "True"
        desired_caps['chromeOptions'] = {'androidProcess': 'com.tencent.mm:tools'}
        if desired_caps.get('appPackage') == 'com.android.chrome':
            desired_caps["browserName"] = 'Chrome'
            desired_caps["appActivity"] = '.BrowserActivity'
        remote = "http://127.0.0.1:" + str(port) + "/wd/hub"
        self.driver = webdriver.Remote(remote, desired_caps)

    @property
    def contexts(self):
        """
        返回当前会话中的上下文，使用后可以识别H5页面的控件
        :return:str
        """
        contexts = self.driver.contexts
        return contexts

    @property
    def context(self):
        """
        返回当前会话的当前上下文。
        :return:
        """
        context = self.driver.context
        return context

    @property
    def page_source(self):
        """
        获取当前页面的源
        :return:
        """
        return self.driver.page_source

    @staticmethod
    def get_type_value(str_type):
        """
        获取查找元素类型和值
        :param str_type: 如id=aa
        :return: {'type','value'}
        """
        new_str = str_type.replace('=', '$', 1)
        tmp = new_str.split('$')
        by_type = tmp[0].lower()
        by_value = tmp[1]
        if by_type not in By.__dict__:
            logging.error('不支持%s类型查询方式' % by_type)
            raise NameError('不支持%s类型查询方式' % by_type)
        return By.__dict__.get(by_type), by_value

    def find_type(self, str_type, elements=True):
        """
        查看元素方法，支持find_element和find_elements两种方法
        :param str_type: 元素类型和元素值
        :param elements: 使用find_element还是find_elements
        :return:元素对象
        """
        tmp = self.get_type_value(str_type)
        by_type = tmp[0]
        by_value = tmp[1]
        if elements:
            return self.driver.find_elements(by_type, by_value)
        else:
            element = WebDriverWait(self.driver, 3).\
                until(visibility_of_element_located(tmp), '页面元素不存在')
            return element

    def click(self, str_type):
        """
        元素点击方法，等待时间内如果点击失败则抛出异常
        :param str_type:元素类型和值
        :return:None
        """
        err = None
        end_time = time.time() + self.wait_time
        while True:
            try:
                element = self.find_type(str_type, False)
                logging.info('已查找到 %s 的元素.' % str_type)
                element.click()
                return
            except Exception as e:
                err = e
                msg = e.args[0].strip()
                logging.warning('click操作出错，错误原因：%s' % msg)
            time.sleep(1)
            if time.time() > end_time:
                break
        raise err

    def is_displayed(self, str_type, wait_time=30):
        try:
            element = WebDriverWait(self.driver, wait_time).\
                until(visibility_of_element_located(self.get_type_value(str_type)), '页面元素不存在')
        except TimeoutException:
            logging.warning('%s 的元素未出现' % str_type)
            return False
        if element:
            logging.info('已查找到 %s 的元素.' % str_type)
            return True

    def type(self, str_type, value, clear=True):
        """
        字符输入方法，输入之前先会清除输入框内容
        :param str_type:元素类型和值
        :param value:待输入字符
        :param clear:是否清除输入框内容，默认清除
        :return:None
        """
        err = None
        end_time = time.time() + self.wait_time
        while True:
            try:
                elements = self.find_type(str_type)
                logging.info('已查找到 %s 的元素 %s 个.' % (str_type, len(elements)))
                for element in elements:
                    try:
                        if clear:
                            element.clear()
                    except Exception as e:
                        logging.warning('清除输入框出现错误:%s' % e)
                    element.send_keys(value)
                    return
            except Exception as error:
                err = error
                msg = error.args[0].strip()
                logging.warning('type操作出错，错误原因：%s,稍后重试！' % msg)
            time.sleep(1)
            if time.time() > end_time:
                break
        raise err

    def scroll(self, origin_el, destination_el):
        """
        将元素origin_el拖动至元素destination_el
        :param origin_el:the element from which to being scrolling
        :param destination_el:the element to scroll to
        :return:None
        """
        origin_el = WebDriverWait(self.driver, self.wait_time).\
            until(visibility_of_element_located(self.get_type_value(origin_el)), u'页面元素不存在')
        destination_el = WebDriverWait(self.driver, self.wait_time).\
            until(visibility_of_element_located(self.get_type_value(destination_el)), u'页面元素不存在')
        self.driver.scroll(origin_el, destination_el)

    def drag_and_drop(self, origin_el, destination_el):
        """
        将元素origin_el拖到目标元素destination_el
        :param origin_el:需要拖动的元素
        :param destination_el:放置origin_el元素
        :return:None
        """
        origin_el = WebDriverWait(self.driver, self.wait_time).\
            until(visibility_of_element_located(self.get_type_value(origin_el)), u'页面元素不存在')
        destination_el = WebDriverWait(self.driver, self.wait_time).\
            until(visibility_of_element_located(self.get_type_value(destination_el)), u'页面元素不存在')
        self.driver.drag_and_drop(self, origin_el, destination_el)

    def tap(self, element, duration=None):
        """
        模拟手指点击，可设置按住时间长度（毫秒）
        :param positions:位置坐标，最多可支持五个手指,参数示例：[(100, 20), (100, 60), (100, 100)]
        :param duration:按住时间
        :return:None
        """
        elx=element.location.get('x') - 300
        ely=element.location.get('y')
        self.driver.tap([(elx, ely), ], duration)

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """
        从A点滑动至B点，滑动时间为毫秒
        :param start_x:滑动起点x轴坐标
        :param start_y:滑动起点y轴坐标
        :param end_x:滑动终点x轴坐标
        :param end_y:滑动终点y轴坐标
        :param duration:点击屏幕时间，单位为毫秒.
        :return:None
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def swipe2down(self):
        """
        向下滚动方法，每次向下滚动屏幕的1/2
        :return:None
        """
        width, height = get_phone_pix(self.device)
        try:
            self.swipe(width / 2, height * 3 / 4, width / 2, height / 4, 1000)
        except Exception as e:
            logging.error(e)

    def swipe2up(self):
        """
        向上滚动方法，每次向上滚动屏幕的1/2
        :return:None
        """
        width, height = get_phone_pix(self.device)
        self.swipe(width / 2, height / 4, width / 2, height * 3 / 4, 1000)


    def swipe2appear(self, str_type):
        err = None
        end_time = time.time() + self.wait_time
        while True:
            try:
                WebDriverWait(self.driver, 1).until(visibility_of_element_located(
                    self.get_type_value(str_type)), '页面元素不存在')
                logging.info('已查找到 %s 的元素.' % str_type)
                return
            except Exception as e:
                self.swipe2down()
                err = e
                msg = e.args[0].strip()
                logging.warning('swipe2appear没有找到元素，错误原因：%s,等待1S后重试！' % msg)
            if time.time() > end_time:
                break
        raise err

    def flick(self, start_x, start_y, end_x, end_y):
        """
        按住A点后快速滑动至B点
        :param start_x: 滑动起点x轴坐标
        :param start_y: 滑动起点y轴坐标
        :param end_x: 滑动终点x轴坐标
        :param end_y: 滑动终点y轴坐标
        :return:None
        """
        self.driver.flick(start_x, start_y, end_x, end_y)

    def pinch(self, element=None, percent=200, steps=50):
        """
        通过模拟双指执行缩小操作
        :param element:缩小操作指向的元素
        :param percent:（可选）缩小的百分比
        :param steps:（可选）缩小操作的步骤
        :return:None
        """
        self.driver.pinch(element, percent, steps)

    def zoom(self, element=None, percent=200, steps=50):
        """
        通过模拟双指执行放大操作
        :param element:放大操作指向的元素
        :param percent:（可选）缩小的百分比
        :param steps:（可选）缩小操作的步骤
        :return:None
        """
        self.driver.zoom(element, percent, steps)

    def reset(self):
        """
        重置应用(类似删除应用数据)
        :return:None
        """
        self.driver.reset()

    def press_keycode(self, keycode, metastate=None):
        """
        发送按键码
        :param keycode:按键码，详细按键码信息到网上查
        :param metastate:发送按键码的元信息
        :return:None
        """
        self.driver.keyevent(keycode, metastate)

    @property
    def current_activity(self):
        """
        获取应用当前activity
        :return:activity
        """
        activity = self.driver.current_activity
        return activity

    def wait_activity(self, activity, timeout, interval=1):
        """
        等待指定的activity出现直到超时
        :param activity:指定的activity
        :param timeout:超时时间
        :param interval:扫描间隔时间，单位为秒
        :return:bool
        """
        result = self.driver.wait_activity(activity, timeout, interval)
        return result

    def background_app(self, seconds):
        """
        后台运行app多少秒
        :param seconds:秒
        :return:None
        """
        self.driver.background_app(seconds)

    def launch_app(self):
        """
        启动app
        :return:None
        """
        self.driver.launch_app()

    def close_app(self):
        """
        关闭app
        :return:None
        """
        self.driver.close_app()

    def shake(self):
        """
        摇一摇手机
        :return:None
        """
        self.driver.shake()

    def open_notifications(self):
        """
        打系统通知栏（仅支持API 18 以上的安卓系统）
        :return:None
        """
        self.driver.open_notifications()

    @property
    def network_connection(self):
        """
        返回网络类型  数值
        :return:
        """
        return self.driver.network_connection

    def set_network_connection(self, connection_type):
        """
        设置网络类型
        相关值设置:
            Value (Alias)      | Data | Wifi | Airplane Mode
            -------------------------------------------------
            0 (None)           | 0    | 0    | 0
            1 (Airplane Mode)  | 0    | 0    | 1
            2 (Wifi only)      | 0    | 1    | 0
            4 (Data only)      | 1    | 0    | 0
            6 (All network on) | 1    | 1    | 0
        :param connection_type:网络类型值
        :return:
        """
        return self.driver.set_network_connection(connection_type)

    def get_settings(self):
        """
        返回当前会话的appium服务的配置
        :return:dict
        """
        return self.driver.get_settings()

    def update_settings(self, settings):
        """
        修改当前会话的appium服务的配置
        :param settings: 修改的配置
        :return:None
        """
        self.driver.update_settings(settings)

    def toggle_location_services(self):
        """
        打开安卓设备上的位置定位设置
        :return:None
        """
        self.driver.toggle_location_services()

    def set_location(self, latitude, longitude, altitude):
        """
        设置设备的经纬度
        :param latitude:纬度
        :param longitude:经度
        :param altitude:海拔高度
        :return:None
        """
        self.driver.set_location(latitude, longitude, altitude)

    def location_in_view(self, str_type):
        """
        获取元素相对于视图的位置
        :return:
        """
        element = WebDriverWait(self.driver, self.wait_time).\
            until(visibility_of_element_located(self.get_type_value(str_type)), u'页面元素不存在')
        return element.location_in_view

    def get_text(self, str_type):
        """
        获取元素的文本值
        :param str_type:元素类型和值
        :return:str
        """
        element = WebDriverWait(self.driver, self.wait_time).\
            until(visibility_of_element_located(self.get_type_value(str_type)), u'页面元素不存在')
        # element = self.find_type(str_type)
        text = element.text.strip()
        return text

    def get_tag_name(self, str_type):
        """
        获取元素的tag_name,对应ui automator中的class
        :param str_type:元素类型和值
        :return:str
        """
        element = WebDriverWait(self.driver, self.wait_time).\
            until(visibility_of_element_located(self.get_type_value(str_type)), u'页面元素不存在')
        tag_name = element.tag_name.strip()
        return tag_name

    def get_attribute(self, str_type, name):
        """
        返回元素指定的属性值
        1、name为content-desc时，content-desc不为空时返回content-desc的属性值，content-desc为空时会返回text属性值
        2、name为text时，返回text属性值
        3、name为class时，返回class属性值
        4、name为resource-id时，返回resource-id属性值
        :param str_type:元素类型和值
        :param name:元素属性名称(name、text、className、resourceId)
        :return:str
        """
        element = WebDriverWait(self.driver, self.wait_time).\
            until(visibility_of_element_located(self.get_type_value(str_type)), '页面元素不存在')
        attribute_value = element.get_attribute(name).strip()
        return attribute_value

    def back(self):
        self.driver.back()

    def screen_shot(self, case_id):
        """
        截图
        :return: None
        """
        file_name = case_id + '__' + time.strftime("%Y-%m-%d") + '.png'
        image_path = get_project_path() + 'result/web_log/image/'
        if not os.path.isdir(image_path):
            os.mkdir(image_path)
        image_file = '%s%s' % (image_path, file_name)
        self.driver.save_screenshot(image_file)

    def switch_to_context(self, context_name):
        """
        Hybrid混合应用Native、WebView切换
        :param context_name:context_name
        :return:None
        """
        self.driver.switch_to.context(context_name)

    def switch_to_window(self, title):
        end_time = time.time() + self.wait_time
        while True:
            handles = self.driver.window_handles
            print(handles)
            for handle in handles:
                print(handle)
                self.driver.switch_to_window(handle)
                window_title = self.get_title()
                print(window_title)
                if window_title == title:
                    return
            time.sleep(1)
            if time.time() > end_time:
                break
        raise AttributeError('窗口切换错误')

    def open(self, url):
        self.driver.get(url)

    def get_title(self):
        title = self.driver.title
        return title


class RunCase(threading.Thread):
    def __init__(self, driver, cases):
        threading.Thread.__init__(self)
        self.driver = driver
        self.cases = cases

    def run(self):
        for cmd in self.cases:
            cmd = "self.driver." + cmd
            exec(cmd)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    testdriver = AndroidDriver()
    testdriver.open_app('weixin_1320.apk')
    testdriver.swipe2down()