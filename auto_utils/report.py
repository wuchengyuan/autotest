# -*- encoding: utf-8 -*-

import time
import os
import collections
from auto_utils import common

__version__ = 1.0

__all__ = ["add_report_data",
           "generate_result_xls"]

report_info = collections.OrderedDict(CasesStatus=collections.OrderedDict(), CaseStatistics=collections.OrderedDict())


def add_report_data(case_id, case_name, result, tester):
    resp_tester = "administrator"
    exec_date_time = time.localtime(time.time())
    exec_date = time.strftime("%Y-%m-%d", exec_date_time)
    exec_time = time.strftime("%H:%M:%S", exec_date_time)
    report_info['CasesStatus'][case_id] = {"Name": case_name,
                                           "Status": result,
                                           "RespTester": resp_tester,
                                           "Tester": tester,
                                           "ExecDate": exec_date,
                                           "ExecTime": exec_time}
    try:
        if result == 'Pass':
            report_info['CaseStatistics'][tester]['PassNumber'] += 1
        else:
            report_info['CaseStatistics'][tester]['FailNumber'] += 1
    except KeyError:
        if result == 'Pass':
            report_info['CaseStatistics'][tester] = {'PassNumber': 1, 'FailNumber': 0}
        else:
            report_info['CaseStatistics'][tester] = {'PassNumber': 0, 'FailNumber': 1}


def generate_result_html(s_time, now, e_time):
    case_detail = author_detail = ""
    total_case_num = len(report_info['CasesStatus'])
    pass_case_num = 0
    fail_cases_num = 0
    cases_status = report_info['CasesStatus']
    for case in cases_status:
        case_id = case
        case_name = cases_status[case]["Name"]
        case_status = cases_status[case]["Status"]
        if case_status == 'Pass':
            pass_case_num += 1
            c_style = "tr_pass"
        else:
            fail_cases_num += 1
            c_style = "tr_fail"
        tester = cases_status[case]["Tester"]
        exec_date = cases_status[case]["ExecDate"]
        exec_time = cases_status[case]["ExecTime"]
        log_url = "./web_log/log/%s__%s.log" % (case_id, exec_date)
        img_url = "./web_log/image/%s__%s.png" % (case_id, exec_date)
        img_tag = ''
        img_full_path = common.get_project_path() + 'result' + img_url.replace('.', '', 1)
        if os.path.isfile(img_full_path) and case_status == 'Fail':
            img_tag = u"<a target='_blank' href='%s'>查看截图</a>" % img_url
        part_of_report_line = u"""
                        <tr>
                            <td class='tr_normal'><a target='_blank' href='%s'>%s</a></td>
                            <td class='%s'>%s</td>
                            <td class='tr_normal'>%s</td>
                            <td class='tr_normal'>%s</td>
                            <td class='tr_normal'>%s</td>
                        </tr>
                        """ % (log_url, case_name, c_style, case_status, tester, exec_time, img_tag)
        case_detail = "%s%s" % (case_detail, part_of_report_line)
    pass_case_percent = '%.2f' % (float(pass_case_num)/total_case_num*100)
    case_statistics = report_info['CaseStatistics']
    for author in case_statistics:
        author_pass_num = case_statistics[author]['PassNumber']
        author_fail_num = case_statistics[author]['FailNumber']
        author_total_num = author_pass_num + author_fail_num
        author_pass_per = '%.2f' % (float(author_pass_num)/author_total_num*100)
        part_of_author_line = u"""
                        <tr>
                            <td class='tr_normal'>%s</td>
                            <td class='tr_normal'>%s</td>
                            <td class='tr_normal'>%s</td>
                            <td class='tr_normal'>%s</td>
                            <td class='tr_normal'>%s</td>
                        </tr>
                          """ % (author, author_total_num,author_pass_num, author_fail_num, author_pass_per)
        author_detail = "%s%s" % (author_detail, part_of_author_line)

    project_start_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(s_time))
    project_stop_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(e_time))
    duration_seconds = float("%.2f" % (e_time - s_time))

    template_html_report = u"""
<META HTTP-EQUIV='Content-Type' CONTENT='text/html; charset=gbk'>
<HTML>
    <HEAD>
        <TITLE>自动化测试报告</TITLE>
        <STYLE>
            .textfont {font-weight: normal; font-size: 12px; color: #000000; font-family: verdana, arial, helvetica, sans-serif }
            .owner {width:100%%; border-right: #6d7683 1px solid; border-top: #6d7683 1px solid; border-left: #6d7683 1px solid; border-bottom: #6d7683 1px solid; background-color: #a3a9b1; padding-top: 3px; padding-left: 3px; padding-right: 3px; padding-bottom: 10px; }
            .product {color: white; font-size: 22px; font-family: Calibri, Arial, Helvetica, Geneva, Swiss, SunSans-Regular; background-color: #59A699; padding: 5px 10px; border-top: 5px solid #a9b2c5; border-right: 5px solid #a9b2c5; border-bottom: #293f6f; border-left: 5px solid #a9b2c5;}
            .rest {color: white; font-size: 24px; font-family: Calibri, Arial, Helvetica, Geneva, Swiss, SunSans-Regular; background-color: white; padding: 10px; border-right: 5px solid #a9b2c5; border-bottom: 5px solid #a9b2c5; border-left: 5px solid #a9b2c5 }
            .chl {font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; width: 17%%; height: 20px; border-bottom: 1px solid white }
            a {color: #336 }
            a:hover {color: #724e6d }
            .ctext {font-size: 11px; padding-right: 5px; padding-left: 5px; width: 80%%; height: 20px; border-bottom: 1px solid #eee }
            .hl {color: #724e6d; font-size: 12px; font-weight: bold; background-color: white; height: 20px; border-bottom: 2px dotted #a9b2c5 }
            .space {height: 10px;}
            h3 {font-weight: bold; font-size: 11px; color: white; font-family: verdana, arial, helvetica, sans-serif;}
            .tr_normal {font-size: 10px; font-weight: normal; background-color: #eee; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;}
            .tr_pass {font-size: 10px; font-weight: normal; background-color: #eee; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;}
            .tr_fail {font-size: 10px; font-weight: normal; background-color: #eee; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white; color: red;}
        </STYLE>
        <META content='MSHTML 6.00.2800.1106'>
    </HEAD>
    <body leftmargin='0' marginheight='0' marginwidth='0' topmargin='0'>
        <table width='100%%' border='0' cellspacing='0' cellpadding='0'>
            <tr>
                <td class='product'>自动化测试报告</td>
            </tr>
            <tr>
                <td class='rest'>
                    <table class='space' width='100%%' border='0' cellspacing='0' cellpadding='0'>
                        <tr>
                            <td></td>
                        </tr>
                    </table>                                                                        
                    <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                        <tbody>
                            <tr>
                                <td>
                                    <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                                        <tbody>
                                            <tr>
                                                <td class='chl' width='20%%'>项目名称</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>测试项目</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>开始时间</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>结束时间</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>持续时间</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>用例总数</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>通过用例</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>总通过率</td>
                                                <td class='ctext'>%s</td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>详细日志</td>
                                                <td class='ctext'><a target='_blank' href='./logging.log'>查看日志</a></td>
                                            </tr>
                                            <tr>
                                                <td class='chl' width='20%%'>问题反馈</td>
                                                <td class='ctext'>wucy@guahao.com</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td class='space'></td>
                            </tr>
                        </tbody>
                    </table>
                    <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                      <tbody>
                            <tr>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>用例撰写人</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>用例的总数</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>用例通过数</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>用例失败数</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>用例通过率</td>
                            <tr>
                            %s
                            </tr>
                            </tr>
                        </tbody>
                            <tr>
                                <td class='space'></td>
                            </tr>
                    <table class='textfont' cellspacing='0' cellpadding='0' width='100%%' align='center' border='0'>
                        <tbody>
                            <tr>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>用例序号标题</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>用例执行状态</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>用例撰写人员</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>用例执行时间</td>
                                <td style='font-size: 10px; font-weight: bold; background-color: #D9D1DF; padding-right: 5px; padding-left: 5px; height: 20px; border-bottom: 1px solid white;'>失败用例截图</td>
                            </tr>
                            %s
                        </tbody>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</HTML>
""" % ('微医自动化', '全流程测试', project_start_at, project_stop_at, duration_seconds, total_case_num, pass_case_num,
       pass_case_percent, author_detail, case_detail)

    html_report = os.path.join(common.get_project_path(), "result/result.html")
    with open(html_report, 'w') as f:
        f.write(str(template_html_report))
    return total_case_num, pass_case_num, pass_case_percent, duration_seconds
