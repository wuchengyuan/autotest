#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from wxpy import *

bot = Bot()
my_friend = bot.friends()
for i in range(1, len(my_friend)):
    time.sleep(1)
    print('-----%d/%d-------'%(i,len(my_friend)))
    my_friend[i].send_msg(" ॣ ॣ ॣ")