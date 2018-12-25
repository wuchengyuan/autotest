# coding:utf-8
import urllib2
import sys
import ssl

url = 'https://120.24.246.124:8888/svn/中科信/版本管理/测试版本管理/4.0健康通/wap网站/更新包'
username = 'wucy'
password = 'Wcy#123'

context = ssl._create_unverified_context()

req = urllib2.Request(url)
try:
    handle = urllib2.urlopen(req, context=context)
except IOError, e:
    print e
else:
    print "This page isn't protected by authentication."
    sys.exit(1)

getrealm = e.headers['www-authenticate']
print getrealm