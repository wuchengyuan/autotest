#!/usr/bin/env python
# -*- coding: utf-8 -*-
import auto_utils.database as db1
from auto_utils.interface_tools.interface_verify import IntVerify
from auto_utils.log import *
from auto_utils.common import *


class IntControl(IntVerify):
    def __init__(self):
        super(IntControl, self).__init__()
        self.case_log = Log()
        self.__conclusion = True
        self.__temp_vars = {}
        self.__flag = True
        self.__cmd_interface = ['get', 'post']
        self.__cmd_verify = ['verify_contain', 'verify_url',  'verify_db', 'verify_decrypt']
        self.__cmd_other = ['time_sleep', 'set', 'build_xml']
        self.__cmd_db = ['db_select', 'db_update']

    def exec_command(self, case_id, commands, desc):
        if len(commands) == 0:
            return True
        for step in commands:
            step = self.replace_var(step)
            step = step.replace('\n', '')
            logging.info(u'----------开始执行步骤：%s' % step)
            level = self.validate_cmd(step)
            if level is None:
                logging.error(u'命令不存在：%s' % step)
                self.case_log.step_log(case_id, 'NONE', 'Fail', u'命令不存在：' + step)
                self.__conclusion = False
                return False
            else:
                try:
                    exec('self.' + step)
                    self.case_log.step_log(case_id, level, 'Pass', step)
                except Exception as e:
                    msg = e.args[0].strip()
                    logging.error(u'%s操作执行失败，错误：%s' % (step, msg))
                    self.__conclusion = False
                    self.case_log.step_log(case_id, level, 'FAIL',  step + '【' + msg + '】')
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
        if cmd in self.__cmd_interface:
            return 'browser'
        elif cmd in self.__cmd_verify:
            return 'verify'
        elif cmd in self.__cmd_other:
            return 'other'
        elif cmd in self.__cmd_db:
            return 'db'
        else:
            return None

    def replace_var(self, step):
        keys = re.findall('%(.*?)%', step)
        for key in keys:
            var = self.get_param(key)
            step = step.replace('%' + key + '%', var)
        return step

    def set(self, key, val=None):
        """
        设置全局变量,可通过表达式获取值后再赋值给变量
        :param key: 键
        :param val: 值
        """
        if val is None:
            global_var[key] = time.strftime('%Y%d%H%M%S', time.localtime())
        else:
            try:
                global_var[key] = str(eval('self.' + val))
            except Exception as e:
                logging.debug(e)
                global_var[key] = val

    def get_param(self, key):
        """
        获取全局参数
        :param key: 键
        :return: 值
        """
        if key in global_var:
            return global_var[key]
        elif key in self.__temp_vars.keys():
            return self.__temp_vars[key]
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

    @staticmethod
    def time_sleep(sec):
        """
        等待时间
        :param sec: 秒数
        """
        time.sleep(sec)

if __name__ == '__main__':
    w = IntControl()
    w.set('data', "build_xml('5001','QLCCSYY_WX','123')")
