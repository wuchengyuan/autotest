#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


def back_contacts_page(driver):
    for i in range(5):
        result = driver.is_displayed('ui=new UiSelector().text("通讯录")', 8)
        if result:
            contacts_page_flag = driver.is_displayed('id=com.tencent.mm:id/ll', 3)
            if contacts_page_flag:
                return True
            else:
                driver.click('ui=new UiSelector().text("通讯录")')
            return True
        else:
            current_activity = driver.current_activity
            if current_activity == 'com.android.launcher2.Launcher':
                driver.launch_app()
            else:
                driver.back()
    logging.error('返回首页失败')