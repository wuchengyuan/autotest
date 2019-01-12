#!/usr/bin/env python
# -*- coding: utf-8 -*-
from auto_utils.android_tools.android_driver import *
from auto_utils.android_tools.weixin.command import *


def search_tel_add_friend():
    driver = AndroidDriver()
    driver.open_app('weixin_1320.apk')
    driver.click('aid=更多功能按钮')
    driver.click('ui=new UiSelector().className("android.widget.TextView").textContains("添加朋友")')
    driver.click('id=com.tencent.mm:id/ji')
    tel_no = 18974880025
    for i in range(10000):
        tel_no += 1
        driver.type('id=com.tencent.mm:id/ji', '%s' % tel_no)
        driver.click('id=com.tencent.mm:id/lf')
        result = driver.is_displayed('id=com.tencent.mm:id/bot', 5)
        if not result:
            if driver.is_displayed('id=com.tencent.mm:id/awc', 5):
                print('tel %s was added!' % tel_no)
                driver.click('id=com.tencent.mm:id/jc')
            else:
                driver.click('id=com.tencent.mm:id/awb')
                driver.click('id=com.tencent.mm:id/j0')
                driver.is_displayed('id=com.tencent.mm:id/awb')
                driver.click('id=com.tencent.mm:id/jc')


def address_list_add_friend():
    driver = AndroidDriver()
    driver.open_app('weixin_1320.apk')
    driver.click('ui=new UiSelector().textContains("通讯录")')
    driver.click('id=com.tencent.mm:id/bm4')
    i = 1
    while True:
        flag = driver.is_displayed('id=com.tencent.mm:id/j0', 3)
        if flag:
            elements = driver.find_type('id=com.tencent.mm:id/bme')
            if len(elements) == 0:
                driver.swipe2down()
            else:
                try:
                    for element in elements:
                        element.click()
                        result = driver.is_displayed('id=com.tencent.mm:id/au_', 3)
                        if result:
                            driver.click('id=com.tencent.mm:id/au_')
                            driver.tap(element, 3000)
                            driver.click('id=com.tencent.mm:id/cj')
                        i += 1
                        print(i)
                except Exception:
                    pass
        else:
            if driver.get_text('id=android:id/text1') == '详细资料':
                driver.click('com.tencent.mm:id/jc')


def group_chat_add_friend():
    driver = AndroidDriver()
    driver.open_app('weixin_1320.apk')
    driver.click('ui=new UiSelector().text("通讯录")')
    driver.click('ui=new UiSelector().text("群聊")')
    time.sleep(10)
    group_names = get_all_group_name(driver)
    logging.info('group num is %s ' % len(group_names))
    for group_name in group_names:
        element = move2group_display(driver, group_name)
        group_name = element.text
        logging.info('start add group %s' % group_name)
        element.click()
        in_chat = driver.is_displayed('aid=聊天信息', 5)
        if in_chat:
            driver.click('aid=聊天信息')
        else:
            element.click()
            driver.click('aid=聊天信息')
        username = None
        swipe_num = 0
        while True:
            logging.info('try get username.')
            in_group = driver.is_displayed('ui=new UiSelector().textContains("聊天信息")', 2)
            if not in_group:
                try:
                    driver.click('id=com.tencent.mm:id/j1')
                except Exception as e:
                    logging.info(e)
            flag = driver.is_displayed('ui=new UiSelector().text("等待")', 1)
            if flag:
                driver.click('ui=new UiSelector().text("等待")')
            result = driver.is_displayed('ui=new UiSelector().text("删除并退出")', 3)
            if result:
                username = driver.get_text('id=android:id/summary')
                break
            else:
                driver.swipe2down()
        if username == '飞燕':
            logging.info('group %s is added,continue' % group_name)
            # for i in range(4):
            #     driver.back()
            #     if driver.is_displayed('ui=new UiSelector().text("通讯录")', 5):
            #         driver.click('ui=new UiSelector().text("通讯录")')
            #         driver.click('ui=new UiSelector().text("群聊")')
            #         break
            continue
        all_member_button = False
        for i in range(5):
            all_member_button = driver.is_displayed('ui=new UiSelector().text("查看全部群成员")', 3)
            if all_member_button:
                driver.click('ui=new UiSelector().text("查看全部群成员")')
                break
            else:
                driver.swipe2up()
        if not all_member_button:
            # for i in range(4):
            #     driver.back()
            #     if driver.is_displayed('ui=new UiSelector().text("通讯录")', 5):
            #         driver.click('ui=new UiSelector().text("通讯录")')
            #         driver.click('ui=new UiSelector().text("群聊")')
            #         break
            continue
        for i in range(5):
            driver.swipe2up()
        names = []
        title = driver.get_text('ui=new UiSelector().textContains("聊天成员")')
        members_count = re.search('\d+', title)
        members_count = int(members_count.group())
        logging.info('group member count: %s' % members_count)
        while True:
            members = driver.find_type('id=com.tencent.mm:id/ats')
            for member in members:
                try:
                    name = member.text
                except NoSuchElementException:
                    logging.error('member element is not find!')
                    break
                logging.info('find member name: %s' % name)
                if name not in names:
                    names.append(name)
                    member.click()
                    logging.info('member %s is add!' % name)
                    if driver.is_displayed('ui=new UiSelector().text("发消息")', 5):
                        driver.click('aid=返回')
                    else:
                        try:
                            driver.click('ui=new UiSelector().text("添加到通讯录")')
                            driver.click('ui=new UiSelector().text("发送")')
                        except Exception as e:
                            logging.error(e)
                        if driver.is_displayed('aid=返回', 20):
                            driver.click('aid=返回')
                            back_flag = driver.is_displayed('ui=new UiSelector().textContains("聊天成员")', 20)
                            if not back_flag:
                                logging.error('back to member page error')
                                driver.click('aid=返回')
                        elif driver.is_displayed('ui=new UiSelector().text("确定")', 5):
                            driver.click('ui=new UiSelector().text("确定")')
                            driver.click('aid=返回')
            logging.info('names:%s! all_member_count:%s!' % (len(names), members_count))
            if members_count - len(names) < 20 or swipe_num > 50:
                logging.info('all member is added! total members is: %s' % len(names))
                break
            else:
                swipe_num += 1
                logging.info('swipe2down!')
                driver.swipe2down()
        back_contacts_page(driver)


def in_group_chat(driver):
    error = driver.is_displayed('ui=new UiSelector().text("等待")', 3)
    if error:
        driver.click('ui=new UiSelector().text("等待")')
    back_contacts_page(driver)
    driver.click('ui=new UiSelector().text("群聊")')
    if driver.is_displayed('ui=new UiSelector().resourceId("android:id/text1").text("群聊")', 5):
        logging.info('in group success')
        return True
    else:
        logging.info('in group fail')
        return False


def get_all_group_name(driver):
    while True:
        result = in_group_chat(driver)
        if result:
            break
    group_names = []
    while True:
        group_num = len(group_names)
        elements = driver.find_type('id=com.tencent.mm:id/my')
        for element in elements:
            group_name = element.text
            if group_name not in group_names:
                logging.info('get group name:%s' % group_name)
                group_names.append(group_name)
        if len(group_names) > group_num:
            driver.swipe2down()
        else:
            break
    logging.info('group count: %s' % len(group_names))
    return group_names


def move2group_display(driver, group_name):
    while True:
        result = in_group_chat(driver)
        if result:
            break
    while True:
        elements = driver.find_type('id=com.tencent.mm:id/my')
        for element in elements:
            current_name = element.text
            if current_name == group_name:
                logging.info('%s is display' % group_name)
                return element
        logging.info('%s is not display,swipe2down' % group_name)
        driver.swipe2down()


def group_need_add(driver, name, flag='飞燕'):
    move2group_display(driver, name)
    driver.click_text('', name)
    in_chat = driver.is_displayed('aid=聊天信息', 5)
    if in_chat:
        driver.click('aid=聊天信息')
    else:
        logging.error('找不到聊天信息按钮')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    group_chat_add_friend()

