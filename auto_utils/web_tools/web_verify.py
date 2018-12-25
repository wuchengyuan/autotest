# -*- coding: utf-8 -*-
from auto_utils.web_tools.web_driver import WebDriver
from auto_utils.database import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *


class WebVerify(WebDriver):
    def verify_displayed(self, str_type, exist=True):
        """
        检查元素是否可见
        :param str_type: 元素查找类型和元素，如：id=a
        :param exist: bool，默认时验证元素是否存在，false时验证元素是否不存在
        :return:
        """
        tmp = self.get_type_value(str_type)
        by_type = tmp["type"]
        by_value = tmp["value"]
        if exist:
            element = WebDriverWait(self.driver, self.wait_time).\
                until(visibility_of_element_located((by_type, by_value)), u'页面元素不存在')
            self.execute_script('arguments[0].style.border = "5px solid yellow"', element)
            logging.info(u'页面元素“%s”可见' % str_type)
        else:
            WebDriverWait(self.driver, self.wait_time).\
                until(invisibility_of_element_located((by_type, by_value)), u'页面元素存在')
            logging.info(u'页面元素：“%s”不可见' % str_type)

    def verify_text_displayed(self, str_type, text):
        """
        检查元素是否可见
        :param str_type: 元素查找类型和元素，如：id=a
        :return:
        """
        tmp = self.get_type_value(str_type)
        by_type = tmp["type"]
        by_value = tmp["value"]
        WebDriverWait(self.driver, self.wait_time).\
            until(text_to_be_present_in_element((by_type, by_value), text), u'页面元素不存在')
        logging.info(u'元素%s中的文本值可见' % str_type)

    def verify_title(self, title):
        result = WebDriverWait(self.driver, self.wait_time).until(title_contains(title), 'Title校验错误')
        if result:
            logging.info(u'Title校验通过')

    def verify_text(self, str_type, text):
        end_time = time.time() + self.wait_time
        while True:
            try:
                element = self.find_text_element(str_type, text)
                if element:
                    logging.info(u'文本校验通过')
                    return True
            except Exception as e:
                logging.error(e)
            time.sleep(0.5)
            if time.time() > end_time:
                break
        raise Exception('查找不到元素或元素不可用！')

    @staticmethod
    def verify_db(sql, value):
        rec = db_select(sql)
        if rec is not None and rec == value:
            return
        else:
            logging.error(u'数据库查询结果：“%s”与期望值：“%s”不一致' % (rec, value))
            raise Exception(u'数据库查询结果与期望不一致')
