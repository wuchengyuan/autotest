#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
from auto_utils.common import *
from auto_utils.web_tools.web_browser import Browser


class WebDriver(Browser):
    """
    元素操作模块
    """

    def __init__(self):
        super(WebDriver, self).__init__()
        self.types = {'css': By.CSS_SELECTOR, 'id': By.ID, 'name': By.NAME, 'class': By.CLASS_NAME, 'tag': By.TAG_NAME,
                      'xpath': By.XPATH, 'link': By.LINK_TEXT, 'plink': By.PARTIAL_LINK_TEXT}
        self.__url = None

    def get_type_value(self, str_type):
        """
        获取type和value值
        :param str_type: 如id=aa
        :return: {'type','value'}
        """
        new_str = str_type.replace('=', '$', 1)
        tmp = new_str.split('$')
        by_type = tmp[0].lower()
        by_value = tmp[1]
        if by_type not in self.types:
            raise Exception('不支持%s类型查询方式' % by_type)
        return {'type': self.types[by_type], 'value': by_value}

    def find_type(self, str_type, elements=True):
        tmp = self.get_type_value(str_type)
        by_type = tmp["type"]
        by_value = tmp["value"]
        if elements:
            return self.driver.find_elements(by_type, by_value)
        else:
            element = WebDriverWait(self.driver, 3).\
                until(visibility_of_element_located((by_type, by_value)), u'页面元素不存在')
            # element = self.driver.find_element(by_type, by_value)
            self.execute_script('arguments[0].style.border = "1px solid yellow"', element)
            return element

    def find_text_element(self, str_type, text):
        """
        检查元素文本值
        :param str_type: 指定元素
        :param text: 待匹配的字符串
        :return: 元素列表
        """
        elements = self.find_type(str_type)
        for element in elements:
            logging.info(u'找到%s的文本：“%s”' % (str_type, element.text))
            if element.text.strip() == text:
                self.execute_script('arguments[0].style.border = "1px solid yellow"', element)
                return element

    @time_statistics
    def click(self, str_type, title=None):
        """
        浏览器点击方法，点击之前判断元素是否可见
        :param str_type:
        :return:
        """
        msg = None
        end_time = time.time() + self.wait_time
        while True:
            try:
                element = self.find_type(str_type, False)
                element.click()
                if title is not None:
                    if self.get_title() == title:
                        return
                    else:
                        logging.warning(u'点击未生效，页面未跳转！')
                        time.sleep(3)
                else:
                    return
            except Exception as e:
                msg = e
            time.sleep(1)
            if time.time() > end_time:
                break
        logging.error(msg)
        raise Exception('查找不到元素或元素不可用！')

    @time_statistics
    def click_text(self, str_type, text):
        """
        根据元素和文本执行点击操作
        :param str_type:
        :param text:
        :return:
        """
        msg = None
        end_time = time.time() + self.wait_time
        while True:
            try:
                element = self.find_text_element(str_type, text)
                if element.is_displayed() and element.is_enabled():
                    time.sleep(0.3)
                    element.click()
                    return
            except Exception as e:
                msg = e
            time.sleep(1)
            if time.time() > end_time:
                break
        if msg:
            logging.error(msg)
        raise Exception('查找不到元素或元素不可用！')

    @time_statistics
    def right_click(self, str_type, sec=0):
        """
        鼠标右键点击事件
        :param str_type: 如'id=aa'
        """
        time.sleep(sec)
        elements = self.find_type(str_type)
        if elements[0].is_displayed():
            ActionChains(self.driver).context_click(elements[0]).perform()
        else:
            raise Exception(u'元素不可见')

    @time_statistics
    def right_click_text(self, str_type, text, sec=0):
        """
        根据文本内容点击元素
        :param str_type: 'id=aa'/['id=aa',...]
        :param text: 文本内容
        """
        time.sleep(sec)
        elements = self.find_text_element(str_type, text)
        if elements[0].is_displayed():
            ActionChains(self.driver).context_click(elements[0]).perform()
        else:
            raise Exception(u'元素不可见')

    @time_statistics
    def double_click(self, str_type, sec=0):
        """
        鼠标双击事件
        :param str_type: 如'id=aa'
        """
        time.sleep(sec)
        elements = self.find_type(str_type)
        if elements[0].is_displayed():
            ActionChains(self.driver).double_click(elements[0]).perform()
        else:
            raise Exception(u'元素不可见')

    @time_statistics
    def double_click_text(self, str_type, text, sec=0):
        """
        根据文本内容双击元素
        :param str_type: 'id=aa'/['id=aa',...]
        :param text: 文本内容
        """
        time.sleep(sec)
        elements = self.find_text_element(str_type, text)
        if elements[0].is_displayed():
            ActionChains(self.driver).double_click(elements[0]).perform()
        else:
            raise Exception(u'元素不可见')

    def type(self, str_type, value, clear=True):
        msg = None
        end_time = time.time() + self.wait_time
        while True:
            try:
                elements = self.find_type(str_type)
                for element in elements:
                    self.execute_script('arguments[0].style.border = "1px solid yellow"', element)
                    try:
                        if clear:
                            element.clear()
                    except Exception as e:
                        logging.warning(u'清除输入框出现错误:%s' % e)
                    element.send_keys(value)
                    return
            except Exception as err:
                msg = err
            time.sleep(1)
            if time.time() > end_time:
                break

        logging.error(msg)
        raise Exception('查找不到元素！')

    def get_attr(self, str_type, attribute):
        """
        获取指定元素的指定属性值
        :param str_type: 'id=aa'
        :param attribute: 要获取的属性
        :return 返回属性值，有多个只返回第一个
        """
        elements = self.find_type(str_type)
        attr_value = elements[0].get_attribute(attribute)
        if attr_value:
            logging.info(u'%s：获取页面元素属性值为：%s' % (str_type, attr_value))
            return attr_value
        else:
            raise Exception(u'获取不到页面元素属性值')

    def get_text(self, str_type, key=None):
        """
        获取指定元素的文本值
        :param str_type: 'id=aa'
        :return 返回元素的文本内容，有多个只返回第一个
        """
        msg = None
        end_time = time.time() + self.wait_time
        while True:
            try:
                text = self.find_type(str_type, False).text
                if text and key:
                    global_var[key] = text
                logging.info(u'获取文本值：%s' % text)
                return text
            except Exception as e:
                msg = e
            time.sleep(1)
            if time.time() > end_time:
                break
        logging.error(msg)
        raise Exception(u'获取不到文本值')

    def selected(self, str_type, selected=True):
        """
        元素选择方法
        :param str_type:
        :param selected:
        :return:
        """
        elements = self.find_type(str_type)
        result = elements[0].is_selected()
        logging.info(u'result:%s' % result)
        if selected and not result:
            elements[0].click()
        elif not selected and result:
            elements[0].click()

    def selected_text(self, str_type, text, selected=True):
        """
        元素选择方法
        :param str_type:
        :param selected:
        :return:
        """
        elements = self.find_text_element(str_type, text)
        result = elements[0].is_selected()
        logging.info(u'result:%s' % result)
        if selected and not result:
            elements[0].click()
        elif not selected and result:
            elements[0].click()

    def size(self, str_type):
        """
        获取指定元素宽高
        :param str_type: 如'id=aa'
        :return 返回元素宽高，有多个只返回第一个
        """
        elements = self.find_type(str_type)
        return elements[0].size

    def move_to_element(self, str_type):
        """
        鼠标悬停在指定元素上的操作
        :param str_type: 如'id=aa'
        """
        elements = self.find_type(str_type)
        if len(elements) > 0:
            ActionChains(self.driver).move_to_element(elements[0]).perform()

    def drag_and_drop(self, source, target):
        """
        鼠标拖动事件
        :param source: 源对象
        :param target: 目标对象
        """
        elements_1 = self.find_type(source)
        elements_2 = self.find_type(target)
        ActionChains(self.driver).drag_and_drop(elements_1[0], elements_2[0]).perform()

    def click_and_hold(self, str_type):
        """
        鼠标左键按住事件
        :param str_type: 如'id=aa'
        """
        elements = self.find_type(str_type)
        ActionChains(self.driver).click_and_hold(elements[0]).perform()

    def accept_alert(self):
        """
        获取alert对象
        """
        return self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        关闭alert
        """
        self.driver.switch_to.alert.dismiss()

    def switch_to_frame(self, frame):
        """
        切换到frame
        :param frame: frameid
        """
        self.driver.switch_to.frame(frame)

    def switch_to_frame_out(self):
        """
        退出当前frame
        """
        self.driver.switch_to.default_content()

    # 打开新窗口
    def open_new_window(self, str_type):
        """
        打开新窗口
        :param str_type: 如'id=aa'
        """
        now_handle = self.driver.current_window_handle
        self.click(str_type)
        time.sleep(2)
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle != now_handle:
                self.driver.switch_to.window(handle)

    # 文件上传
    def upload(self, str_type, name):
        """
        文件上传
        :param str_type: 如'id=aa'
        :param name: 文件名(文件必须存在在工程resource目录下)
        """
        path = get_project_path() + '\\download\\' + name
        if os.path.isdir(path):
            self.click(str_type)
            os.system(get_project_path() + '\\web_tools\\upload.exe %s' % path)
        else:
            raise Exception('%s is not exists' % path)

    def execute_script(self, js, *args):
        """
        调用js函数
        :param js: js
        """
        time.sleep(0.5)
        js = str(js)
        result = self.driver.execute_script(js, *args)
        time.sleep(0.5)
        return result

    def scroll(self, top=10000):
        """
        控制滚动条，0为顶部，10000为底部
        :param top: 数字
        :return:
        """
        js = 'document.body.scrollTop=%s' % top
        self.execute_script(js)

    def wait(self, sec):
        """
        智能等待
        :param sec: 秒数
        """
        self.driver.implicitly_wait(sec)

    @staticmethod
    def time_sleep(sec):
        """
        等待时间
        :param sec: 秒数
        """
        time.sleep(sec)

    def ctrl(self, str_type, key):
        """
        在指定元素上执行ctrl组合键事件
        :param str_type: 如'id=aa'
        :param key: 如'X'
        """
        elements = self.find_type(str_type)
        elements[0].send_keys(Keys.CONTROL, key)

    def alt(self, str_type, key):
        """
        在指定元素上执行alt组合事件
        :param str_type: 如'id=aa'
        :param key: 如'X'
        """
        elements = self.find_type(str_type)
        elements[0].send_keys(Keys.ALT, key)

    def space(self, str_type):
        """
        在指定输入框发送空格
        :param str_type: 如'id=aa'
        """
        elements = self.find_type(str_type)
        elements[0].send_keys(Keys.SPACE)

    def enter(self, str_type):
        """
        在指定输入框发送回车键
        :param str_type: 如'id=aa'
        """
        elements = self.find_type(str_type)
        elements[0].send_keys(Keys.ENTER)

    def backspace(self, str_type):
        """
        在指定输入框发送回退键
        :param str_type: 如'id=aa'
        """
        elements = self.find_type(str_type)
        elements[0].send_keys(Keys.BACK_SPACE)

    def tab(self, str_type):
        """
        在指定输入框发送回制表键
        :param str_type: 如'id=aa'
        """
        elements = self.find_type(str_type)
        elements[0].send_keys(Keys.TAB)

    def escape(self, str_type):
        """
        在指定输入框发送回制表键
        :param str_type: 如'id=aa'
        """
        elements = self.find_type(str_type)
        elements[0].send_keys(Keys.ESCAPE)

    def load_error_refresh(self, text):
        element_text = self.find_type('tag=body', False).text
        if text not in element_text:
            self.refresh()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    web = WebDriver()
    web.open_browser('chrome')
    web.open('http://qlcht.test.jkt.guahao-inc.com/Index/Index')
