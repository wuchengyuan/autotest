#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import os
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def mail_message(sender, receivers, file_path):
    message = MIMEMultipart()
    message['From'] = Header('自动化测试<%s>' % sender, 'utf-8')
    message['To'] = Header(','.join(receivers), 'utf-8')
    subject = '自动化测试结果%s' % time.strftime('%Y-%m-%d', time.localtime())
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText('各位好：\n自动化测试结果见附件！', 'plain', 'utf-8'))
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        att1 = MIMEText(f.read(), 'base64', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'
    att1['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    message.attach(att1)
    return message


def send_mail(mail_host, mail_user, mail_pass, sender, receivers, file_path):
    message = mail_message(sender, receivers, file_path)
    try:
        smtp_obj = smtplib.SMTP_SSL(mail_host, 465)
        smtp_obj.login(mail_user, mail_pass)
        smtp_obj.sendmail(sender, receivers, message.as_string())
        logging.info('邮件发送成功！')
    except smtplib.SMTPAuthenticationError:
        logging.error('用户认证失败，请检查用户名、密码是否正确！')
    except TimeoutError:
        logging.error('服务器连接超时，请检查发件服务器是否正确！')

if __name__ == '__main__':
    mail_host = 'smtp.exmail.qq.com'
    mail_user = 'wuchengyuan@idvert.com1'
    mail_pass = 'Wcy!23456'
    sender = 'wuchengyuan@idvert.com'
    receivers = ['wuchengyuan@idvert.com']
    file_path = r'D:\web_auto3\result\result.html'
    send_mail(mail_host, mail_user, mail_pass, sender, receivers, file_path)