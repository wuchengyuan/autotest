#!/usr/bin/env python
# -*- coding: utf-8 -*-
from auto_utils.log import Log
from auto_utils.android_tools.android_verify import *
import auto_utils.database as db1


class CmdSummary(object):
    app_web_cmd = ['type', 'click', 'scroll', 'drag_and_drop', 'screen_shot', 'verify_displayed']
    app_cmd = ['open_app', 'tap', 'swipe', 'flick', 'pinch', 'zoom', 'reset', 'press_keycode', 'background_app',
               'launch_app', 'close_app', 'shake', 'open_notifications', 'swipe2appear']
    web_cmd = ['open']


class AndroidControl(AndroidVerify):
    def __init__(self):
        super(AndroidControl, self).__init__()
        self.case_log = Log()
        self.__conclusion = True
        self.__temp_vars = {}
        self.__globals = {}
        self.__flag = True

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
                logging.error('命令不存在：%s' % step)
                self.case_log.step_log(case_id, 'NONE', 'Fail', step + '【命令不存在】')
                self.__conclusion = False
                return False
            else:
                try:
                    exec('self.' + step)
                    self.case_log.step_log(case_id, level, 'Pass', step)
                except SyntaxError:
                    logging.error('%s 操作执行失败，错误原因：语法错误' % step)
                    self.__conclusion = False
                    self.case_log.step_log(case_id, level, 'FAIL',  step + '【命令语法错误】')
                    self.screen_shot(case_id)
                    return False
                except Exception as e:
                    msg = e.args[0].strip()
                    # 命令执行出错则进行截图操作，不再执行后续命令
                    logging.error('%s 操作执行失败，错误原因：%s' % (step, msg))
                    self.__conclusion = False
                    self.case_log.step_log(case_id, level, 'FAIL',  step + '【' + msg + '】')
                    self.screen_shot(case_id)
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

    @staticmethod
    def validate_cmd(cmd):
        pos = cmd.index('(')
        cmd = cmd[0:pos]
        if cmd in CmdSummary.app_web_cmd:
            return 'app_web'
        elif cmd in CmdSummary.app_cmd:
            return 'app'
        elif cmd in CmdSummary.web_cmd:
            return 'web'
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


if __name__ == '__main__':
    testdriver = AndroidControl()
    testdriver.open_app('ximalayaFM_163.apk')
    print(testdriver.current_activity)
    testdriver.is_displayed('id=com.ximalaya.ting.android:id/tab_finding1')