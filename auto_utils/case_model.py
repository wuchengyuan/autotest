# -*- coding: utf-8 -*-
"""
请求解析实体类
"""
import re


class Model:
    def __init__(self, case):
        if case != '':
            self.__case_id = case['req']['test_case']['case_id']
            self.__description = case['req']['test_case']['description']  # 用例描述
            self.__pre_command = case['req']['test_case']['pre_command']  # 前置命令
            self.__step = case['req']['test_case']['step']  # 用例步骤
            self.__verify = case['req']['test_case']['verify']  # 结果校验
            self.__postcommand = case['req']['test_case']['postcommand']  # 后置命令
            self.__case_type = case['req']['test_case']['case_type']  # 后置命令
            self.__tester = case['req']['test_case']['tester']  # 用户名称
            self.__config = case['req']['config']  # 全局变量

    @property
    def case_id(self):
        return self.command2list(self.__case_id.strip())

    @property
    def step(self):
        return self.command2list(self.__step.strip())

    @property
    def description(self):
        return self.__description

    @property
    def pre_command(self):
        return self.command2list(self.__pre_command.strip())

    @property
    def postcommand(self):
        return self.command2list(self.__postcommand.strip())

    @property
    def verify(self):
        return self.command2list(self.__verify.strip())

    @property
    def case_type(self):
        return self.__case_type.strip()

    @property
    def tester(self):
        return self.__tester

    @property
    def config(self):
        return self.__config

    @staticmethod
    def command2list(command):
        """
        将unicode转换为list
        :param command: unicode
        :return: list
        """
        if re.search('\w', command):
            obj_list = []
            if command.find('\n') == -1:
                obj_list.append(command)
                [obj_list.remove('') for i in range(len(obj_list) - 1) if obj_list[i] == '']
                return obj_list
            else:
                while True:
                    flag = command.find(')\n')
                    if flag != -1:
                        obj_list.append(command[:flag+1])
                        command = command[flag+2:]
                    else:
                        obj_list.append(command)
                        break
                [obj_list.remove('') for i in range(len(obj_list) - 1) if obj_list[i] == '']
                return obj_list
        else:
            return ''
