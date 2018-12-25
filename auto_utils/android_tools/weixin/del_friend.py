#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auto_utils.android_tools.weixin.chat import *


def del_black_friend(driver, name):
    move2user_display(driver, name)
# for i in range(1, len(my_friend)):
#     time.sleep(1)
#     print('-----%d/%d-------'%(i,len(my_friend)))
#     my_friend.send_msg(" ॣ ॣ ॣ")