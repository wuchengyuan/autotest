# !/usr/bin/env python
# -*- coding: utf-8 -*-
import auto_utils.web_tools.web_control as web
import auto_utils.interface_tools.interface_control as interface
import auto_utils.android_tools.android_control as android
import auto_utils.case_model as case_model
import auto_utils.excel_read as excel_read
import auto_utils.report as report
import auto_utils.common as common
from auto_utils.log import *

import auto_utils.database as db1
import auto_utils.database_local as db2


class Run:
    def __init__(self):
        self.case_log = Log()
        common.log_on()
        db1.create_engine('test', 'test@test', 'test', '1.1.1.1', 3307)
        db2.create_engine('test', 'test', 'test')
        self.cfg = get_config()

    def case_run(self, driver, case_id, case_data):
        logging.info(u'================================================开始执行用例：%s %s' % (case_id, case_data.description))
        self.case_log.begin_log(case_id, case_data.description)
        driver.exec_whole_case(case_id, case_data.pre_command, case_data.step, case_data.verify,
                               case_data.postcommand, case_data.config, case_data.description)
        result = driver.get_result()
        self.case_log.step_log(case_id, 'result', result, 'complete')
        report.add_report_data(case_id, case_id + case_data.description, result, case_data.tester)

    def start(self):
        info = None
        status = 'run'
        test = excel_read.Excel()
        excel_list = self.cfg.get('project_config').get('excel_cases').split(',')
        web_driver = web.WebControl()
        int_driver = interface.IntControl()
        app_driver = android.AndroidControl()
        for excel in excel_list:
            test.set_excel_file(excel)
            cases_data = test.cases_value()
            start_time = time.time()
            cases = [(k, cases_data[k]) for k in sorted(cases_data.keys())]
            for k, v in cases:
                if status == 'pause':
                    while True:
                        time.sleep(2)
                        if status == 'run':
                            break

                now = time.time()
                case_mode = case_model.Model(v)
                if case_mode.case_type == 'WEB':
                    self.case_run(web_driver, k, case_mode)
                elif case_mode.case_type == 'INT':
                    self.case_run(int_driver, k, case_mode)
                elif case_mode.case_type =='APP':
                    self.case_run(app_driver, k, case_mode)
                stop_time = time.time()
                info = report.generate_result_html(start_time, now, stop_time)
        # sql = "INSERT INTO total_info (total_case_number,pass_case_number,pass_percent,duration_seconds) " \
        #       "VALUES (%d,%d,'%s',%d)" % info
        # web.db2.db_update(sql)
if __name__ == '__main__':
    r = Run()
    r.start()
