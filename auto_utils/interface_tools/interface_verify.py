#!/usr/bin/env python
# -*- coding: utf-8 -*-
from auto_utils.interface_tools.interface_driver import *
from auto_utils.database import *


class IntVerify(IntDriver):
    def __init__(self):
        super(IntVerify, self).__init__()

    def verify_contain(self, result):
        if self.text is not None and result in self.text:
            logging.info('结果校验成功')
        else:
            logging.error('结果校验失败，返回结果：\n%s' % self.text)
            raise Exception('结果校验失败')

    @staticmethod
    def verify_db(sql, value):
        rec = db_select(sql)
        if rec is not None and rec == value:
            return
        else:
            logging.error(u'数据库查询结果：“%s”与期望值：“%s”不一致' % (rec, value))
            raise Exception(u'数据库查询结果与期望不一致')

    def verify_decrypt(self, result):
        if self.text is not None and result in self.res_decrypt():
            logging.info('结果校验成功')
        else:
            logging.error('结果校验失败，返回结果：\n%s' % self.text)
            raise Exception('结果校验失败')
