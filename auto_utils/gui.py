#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter.filedialog import *
from tkinter.messagebox import *
from .common import get_project_path


class AutoTestGui:
    def __init__(self):
        self.file_name = ''
        self.root = Tk()
        self.root.title('自动化测试')
        width, height = self.root.winfo_screenwidth(), self.root.winfo_screenwidth()
        self.root.geometry('%sx%s+0+0' % (width, height))
        self.create_menu()
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
        init_dir = get_project_path() + 'data'
        file_name = askopenfilename(filetypes=[('xlsx', 'xls')], initialdir=init_dir)
        if file_name == '':
            self.file_name = None
        else:
            pass


if __name__ == '__main__':
    AutoTestGui()