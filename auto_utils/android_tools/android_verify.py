#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_utils.android_tools.android_driver import *
from selenium.common.exceptions import *


class AndroidVerify(AndroidDriver):

    def verify_displayed(self, str_type, exist=True):
        """
        检查元素是否可见
        :param str_type: 元素查找类型和元素，如：id=a
        :param exist: bool，默认时验证元素是否存在，false时验证元素不存在
        :return:
        """
        if exist:
            self.is_displayed(str_type)
        else:
            try:
                self.is_displayed(str_type)
                raise AttributeError('页面查找到元素')
            except TimeoutException:
                logging.info('页面没有查找到元 %s 元素' % str_type)

    def verify_attribute(self, str_type, name, value):
        attribute_value = self.get_attribute(str_type, name)
        if attribute_value == value.strip():
            logging.info('页面 %s 元素的 %s 属性值检验通过')
        else:
            logging.error('页面 %s 元素的 %s 属性值检验通过')
            raise Exception()
