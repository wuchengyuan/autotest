# -*- encoding: utf-8 -*-

import sys
from auto_utils.common import *


class Log:
    def __init__(self):
        self.case_log_path = get_project_path() + "result/web_log/log"

    @staticmethod
    def get_stamp_date():
        return time.strftime("%Y-%m-%d")

    @staticmethod
    def get_stamp_datetime():
        return time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_stamp_datetime_coherent():
        return time.strftime("%Y-%m-%d_%H_%M_%S")

    @staticmethod
    def make_dirs(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def begin_log(self, case_id, discription):
        self.make_dirs(self.case_log_path)
        log_file_name = "%s__%s.log" % (case_id, self.get_stamp_date())
        log_file = os.path.join(self.case_log_path, log_file_name)
        with open(log_file, "w") as f:
            f.write("**************  微医集团自动化测试  [%s[%s]]  ***************\n"
                    "测试时间                命令类型        测试结果        测试方法【错误原因】\n" % (case_id, discription))

        return log_file

    def step_log(self, case_id, level, info, msg):
        log_file_name = "%s__%s.log" % (case_id, self.get_stamp_date())
        log_file = os.path.join(self.case_log_path, log_file_name)
        info = info.upper()
        level = level.upper()
        with open(log_file, "a") as f:
            f.write("%-20s\t%-10s\t%-10s\t%s\n" % (self.get_stamp_datetime_coherent(), level, info, msg))

if __name__ == '__main__':
    l = Log()
    l.begin_log('ATP-001', 'test start')
    l.step_log('ATP-001', 'cmd', 'click', 'Pass')
