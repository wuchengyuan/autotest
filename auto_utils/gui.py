#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter.ttk import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from auto_utils.common import get_project_path
from auto_utils.excel_read import Excel


class AutoTestGui:
    def __init__(self):
        self.file_name = ''
        self.root = Tk()
        self.root.title('自动化测试')
        self.create_menu()
        width, height = self.root.winfo_screenwidth(), self.root.winfo_screenwidth()
        # self.root.geometry('%sx%s+0+0' % (width, height))
        label_case_name = LabelFrame(self.root, text='用例集')
        label_step = LabelFrame(self.root, text='测试用例')
        columns = ("ID", "用例名称", "用例类型", '用例编写人')
        label_case_name.grid(row=0, column=0)
        label_step.grid(row=0, column=1)
        tree = Treeview(label_case_name, show="headings", columns=columns)

        tree.column("ID")  # 表示列,不显示
        tree.column("用例名称")
        tree.column("用例类型")
        tree.column("用例编写人")
        tree.heading("ID", text="用例ID")  # 显示表头
        tree.heading("用例名称", text="用例名称")  # 显示表头
        tree.heading("用例类型", text="用例类型")
        tree.heading("用例编写人", text="用例编写人")
        tree.insert("", 0, text="line1", values=("1", "2", "3"))  # 插入数据，
        tree.insert("", 1, text="line1", values=("1", "2", "3"))
        tree.insert("", 2, text="line1", values=("1", "2", "3"))
        tree.insert("", 3, text="line1", values=("1", "2", "3"))
        tree.insert("", 4, text="line1", values=("1", "2", "3"))
        tree.pack(side=RIGHT, fill=BOTH)


        columns = ("ID", "用例名称", "用例类型", '用例编写人')
        tree = Treeview(label_step, show="headings", columns=columns)

        tree.column("ID")  # 表示列,不显示
        tree.column("用例名称")
        tree.column("用例类型")
        tree.column("用例编写人")
        tree.heading("ID", text="用例ID")  # 显示表头
        tree.heading("用例名称", text="用例名称")  # 显示表头
        tree.heading("用例类型", text="用例类型")
        tree.heading("用例编写人", text="用例编写人")
        tree.insert("", 0, text="line1", values=("1", "2", "3"))  # 插入数据，
        tree.insert("", 1, text="line1", values=("1", "2", "3"))
        tree.insert("", 2, text="line1", values=("1", "2", "3"))
        tree.insert("", 3, text="line1", values=("1", "2", "3"))
        tree.insert("", 4, text="line1", values=("1", "2", "3"))
        tree.pack(side=RIGHT, fill=BOTH)

        self.root.mainloop()

    def create_menu(self):
        menubar = Menu(self.root)
        file_menu = Menu(menubar)
        file_menu.add_command(label='新建', accelerator='Ctrl + N', command='')
        file_menu.add_command(label='打开', accelerator='Ctrl + O', command=self.open_excel)
        file_menu.add_command(label='保存', accelerator='Ctrl + S', command='')
        file_menu.add_command(label='另存为', accelerator='Ctrl + Shift + S', command='')
        menubar.add_cascade(label='文件', menu=file_menu)
        self.root.config(menu=menubar)

    def open_excel(self):
        init_dir = get_project_path() + 'data/'
        print(init_dir)
        file_name = askopenfilename(filetypes=[('xls', 'xlsx')], initialdir=init_dir)
        if file_name == '':
            self.file_name = None
        else:
            case_data = Excel()
            case_data.set_excel_file(file_name)
            case_data.open_sheet('TestCase')
            return case_data.cases_value()



if __name__ == '__main__':
    AutoTestGui()