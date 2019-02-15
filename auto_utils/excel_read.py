# -*- encoding: utf-8 -*-
import xlrd
from auto_utils.common import *


class Excel:
    """
    EXCEL用例读取模块
    """
    def __init__(self):
        """
        EXCEL文件读取路径
        :return:空
        """
        self.__project_path = get_project_path()
        self.__excel_file = ''
        self.__sheet = None

    @property
    def excel_file(self):
        """
        返回Excel路径
        :return:Excel路径
        """
        return self.__excel_file

    def set_excel_file(self, name):
        """
        设置Excel路径
        :param name:Excel文件名称
        :return:
        """
        if os.path.isfile(name):
            file_path = name
        else:
            file_path = os.path.join(self.__project_path, r"data\%s" % name)
        if os.path.isfile(file_path):
            self.__excel_file = file_path
        else:
            logging.error(u'data目录下不存在%s文件' % file_path)
            raise Exception("%s文件不存在" % file_path)

    def open_sheet(self, sheet):
        """
        打开Excel的sheet
        :param sheet:Excel的sheet名称
        """
        excel_file = self.__excel_file
        if os.path.isfile(excel_file):
            excel = xlrd.open_workbook(excel_file)
            self.__sheet = excel.sheet_by_name(sheet)
        else:
            raise Exception("%s文件不存在%s" % (excel_file, sheet))

    def excel_rows(self):
        """
        获取sheet的行数
        :return:sheet的行数
        """
        return self.__sheet.nrows

    def excel_cols(self):
        """
        获取sheet的列数
        :return:sheet的列数
        """
        return self.__sheet.ncols

    def excel_cell(self, row, col):
        """
        获取单元格的数据
        :param row: 行
        :param col: 列
        :return:
        """
        cell_value = self.__sheet.cell(row, col).value
        return cell_value

    def excel_col_name_cell(self, row, col_name):
        """
        根据列名获取给出行号的单元格数据
        :param row:行号
        :param col_name:列表
        :return:单元格值
        """
        for col in range(0, self.excel_cols()):
            if self.excel_cell(0, col) == col_name:
                return self.excel_cell(row, col)
        err_msg = 'Excel中不存在该列：%s' % col_name
        raise Exception(err_msg)

    def cases_value(self, sheet_name='TestCase'):
        """
        返回固定格式的用例数据
        :return:
        """

        self.open_sheet(sheet_name)
        # 依据 TestCaseID 获取测试步骤信息
        cases = {}
        for i in range(1, self.excel_rows()):
            case_id = self.excel_col_name_cell(i, "TestCaseID")
            if not (case_id and re.search("^[\w-]+$", case_id)):
                continue
            step = self.excel_col_name_cell(i, "Steps")
            description = self.excel_col_name_cell(i, "Description")
            pre_command = self.excel_col_name_cell(i, "PreCommand")
            post_command = self.excel_col_name_cell(i, "PostCommand")
            verify = self.excel_col_name_cell(i, "Verify")
            tester = self.excel_col_name_cell(i, "Tester")
            case_type = self.excel_col_name_cell(i, "CaseType")
            config = get_config()
            cases[case_id] = {"req": {"test_case": {"case_id": case_id,
                                                    "step": step,
                                                    "description": description,
                                                    "pre_command": pre_command,
                                                    "postcommand": post_command,
                                                    "verify": verify,
                                                    "tester": tester,
                                                    "case_type": case_type},
                                      "config": config
                                      }}
        return cases


if __name__ == '__main__':
    test = Excel()
    test.set_excel_file('qlccs-qd-web-4.2.1.xlsx')
    test.open_sheet('TestCase')
    print(test.cases_value())
