#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver

drvier = webdriver.Chrome()
drvier.get('http://www.welhome1818.com/html/zmzz/')
import time
time.sleep(5)
drvier.find_element_by_link_text('998').click()