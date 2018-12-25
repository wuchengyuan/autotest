#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import auto_utils.database as db1
import auto_utils.database_local as db2
from auto_utils.web_tools.web_verify import WebVerify
from auto_utils.log import *


class WebControl(WebVerify):
    def __init__(self):
        super(WebControl, self).__init__()
        self.case_log = Log()
        self.__conclusion = True
        self.__temp_vars = {}
        self.__globals = {}
        self.__flag = True
        self.__cmd_browser = ['window_maximize', 'set_window', 'open_browser', 'open', 'refresh', 'open_new_window',
                              'quit', 'close', 'back', 'forward', 'alert_accept', 'alert_dismiss']
        self.__cmd_element = ['type', 'click', 'click_text', 'click_attr', 'execute_script', 'wait', 'switch_to_frame',
                              'switch_to_frame_out', 'selected', 'selected_text', 'click_date', 'click_num',
                              'get_order_no']
        self.__cmd_event = ['right_click', 'right_click_text', 'move_to_element', 'double_click', 'double_click_text',
                            'drag_and_drop',
                            'click_and_hold', 'ctrl', 'alt', 'space', 'enter', 'backspace', 'tab', 'escape']
        self.__cmd_verify = ['verify_title', 'verify_url', 'verify_text', 'verify_attr',
                             'verify_displayed', 'verify_not_exists', 'verify_count', 'verify_db',
                             'verify_text_displayed']
        self.__cmd_other = ['screen_shot', 'scroll',  'upload', 'time_sleep', 'set', 'alipay_login', 'alipay_pay']
        self.__cmd_db = ['db_select', 'db_update']
        self.__cmd_get = ['get_attr', 'get_text']

    def exec_command(self, case_id, commands, desc):
        if len(commands) == 0:
            return True
        for step in commands:
            step = self.replace_var(step)
            if 'set(' not in step:
                time.sleep(0.5)
            logging.info(u'----------开始执行步骤：%s' % step)
            level = self.validate_cmd(step)
            if level is None:
                logging.error(u'不存在：%s' % step)
                self.case_log.step_log(case_id, 'NONE', 'Fail', u'命令不存在：' + step)
                self.__conclusion = False
                return False
            else:
                try:
                    exec('self.' + step)
                    self.case_log.step_log(case_id, level, 'Pass', step)
                except Exception as e:
                    msg = e.args[0].strip()
                    if msg.find('no such session') != -1 or msg.find('10061') != -1:
                        self.case_log.step_log(case_id, level, 'Pass', step)
                    else:
                        # 命令执行出错则进行截图操作，不再执行后续命令
                        logging.error(u'%s操作执行失败，错误：%s' % (step, msg))
                        self.__conclusion = False
                        self.case_log.step_log(case_id, level, 'FAIL', step + '【' + msg + '】')
                        try:
                            self.screen_shot(case_id)
                        except AttributeError:
                            return False

        return True

    def exec_whole_case(self, case_id, pre_command, steps, verify, postcommand, configs, desc):
        self.__conclusion = True
        self.__temp_vars = configs
        self.__flag = self.exec_command(case_id, pre_command, desc)
        if self.__flag:
            self.__flag = self.exec_command(case_id, steps, desc)
        if self.__flag:
            self.__flag = self.exec_command(case_id, verify, desc)
        self.exec_command(case_id, postcommand, desc)

    def get_result(self):
        return 'Pass' if self.__conclusion else 'Fail'

    def validate_cmd(self, cmd):
        pos = cmd.index('(')
        cmd = cmd[0:pos]
        if cmd in self.__cmd_browser:
            return 'browser'
        elif cmd in self.__cmd_element:
            return 'element'
        elif cmd in self.__cmd_event:
            return 'event'
        elif cmd in self.__cmd_verify:
            return 'verify'
        elif cmd in self.__cmd_other:
            return 'other'
        elif cmd in self.__cmd_db:
            return 'db'
        elif cmd in self.__cmd_get:
            return 'get'
        else:
            return None

    def replace_var(self, step):
        keys = re.findall('%(.*?)%', step)
        for key in keys:
            var = self.get(key)
            step = step.replace('%' + key + '%', var)
        return step

    def set(self, key, val=None):
        """
        设置全局变量,可通过表达式获取值后再赋值给变量
        :param key: 键
        :param val: 值
        """
        if val is None:
            global_var[key] = time.strftime('%d%H%M%S', time.localtime())
        else:
            try:
                global_var[key] = str(eval('self.' + val))
            except Exception as e:
                logging.debug(e)
                global_var[key] = val

    def get(self, key):
        """
        获取全局参数
        :param key: 键
        :return: 值
        """
        if key in global_var.keys():
            return global_var.get(key, '')
        elif key in self.__temp_vars.keys():
            return self.__temp_vars.get(key, '')
        else:
            return ''

    @staticmethod
    def db_select(sql, key=None):
        now = time.time()
        while True:
            rec = db1.db_select(sql)
            if key and rec is not None:
                global_var[key] = rec
            if rec is not None:
                return rec
            time.sleep(2)
            if time.time() > now + 4:
                break

    @staticmethod
    def db_update(sql):
        return db1.db_update(sql)

    def click_date(self):
        today = datetime.datetime.now()
        for i in range(1,8):
            delta = datetime.timedelta(i)
            n_days = today + delta
            day_str = n_days.strftime('%Y-%m-%d')
            str_type = 'css=[data-date="%s"]' % day_str
            logging.info(u'元素表达式为：%s' % str_type)
            try:
                self.click(str_type)
                return day_str
            except Exception as e:
                logging.warning(e)
        raise Exception(u'科室下没有号源')

    def click_num(self):
        msg = None
        end_time = time.time() + self.wait_time
        while True:
            try:
                elements = self.find_type('css=.source-num>.green-ft')
                for element in elements:
                    num = element.text
                    logging.info(u'号源数为：%s' % num)
                    if int(num) > 0:
                        element.click()
                        return
            except Exception as e:
                msg = e
            time.sleep(1)
            if time.time() > end_time:
                break
        if msg:
            logging.error(msg)
        raise Exception(u'医生下没有号源')

    def get_order_no(self):
        msg = None
        end_time = time.time() + self.wait_time
        while True:
            if self.get_title() == u'订单支付':
                try:
                    text = self.find_type('css=#orderInfo>li:nth-child(1)>span', False).text
                    if text:
                        global_var['order_no'] = text
                        logging.info(u'获取文本值：%s' % text)
                        return text
                except Exception as e:
                    msg = e
                    self.refresh()
                time.sleep(2)
            if time.time() > end_time:
                break
            time.sleep(2)
        logging.error(msg)
        raise Exception(u'获取不到文本值')

    def alipay_login(self):
        while True:
            try:
                title = self.get_title()
                if title == '登录':
                    break
                self.open('http://qlcqd.test.jkt.guahao-inc.com/User/login?um=QLCCSYY_ZFB')
                self.execute_script("document.querySelector('#J-loginMethod-tabs>li:nth-child(2)').click()")
                # self.click('css=#J-loginMethod-tabs>li:nth-child(2)')
                self.execute_script("document.getElementById('J-input-user').value='hz_ghwcs2@sina.com'")
                self.click('id=J-input-user')
                # self.type('id=J-input-user', 'hz_ghwcs2@sina.com')
                self.execute_script("document.querySelector('#password_container>input').value='ceshi123'")
                # self.type('css=#password_container>input', 'ceshi123')
                self.click('css=#password_container>input')
                time.sleep(2)
                # self.execute_script("document.getElementById('J-login-btn').click()")
                self.click('id=J-login-btn')
            except Exception as e:
                logging.warning(e)

    def alipay_pay(self):
        self.click('link=确认支付')
        self.click_text('css=.am-button', '继续支付')
        if self.find_text_element('css=.am-button', '下一步'):
            self.click('link=支付宝账户登录')
            # while True:
            self.click('id=logon_id')
            for i in '13549627060':
                self.type('id=logon_id', i, False)
            self.execute_script("document.getElementById('pwd_unencrypt').value='865643'")
            self.execute_script("$('[type=\"submit\"]').click()")
            self.click('css=[type="submit"]')
            self.time_sleep(4)
        if self.find_text_element('css=.am-button', '确认付款'):
            self.click('css=[type="submit"]')
            self.type('id=spwd_unencrypt', '865643')
            self.time_sleep(4)


if __name__ == '__main__':
    w = WebControl()
    w.open_browser('chrome')

