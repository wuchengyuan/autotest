#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import base64
import json
import auto_utils.database as db1
from auto_utils.common import *


def time_statistics(func):
    """
    装饰函数，计算步骤执行时间
    :param func:
    :return:
    """
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        start_time = time.time()
        f = func(*args, **kw)
        end_time = time.time()
        during_time = end_time - start_time
        logging.info(u'%s操作耗时：%s秒' % (func.__name__, during_time))
        if during_time > 2:
            logging.warning(u'接口响应时间大于2S')
        return f
    return _wrapper


class IntDriver:
    def __init__(self):
        self.session = requests.session()
        self.key = '2098D32C4D1399EC'
        self.text = ''

    @time_statistics
    def get(self, url, session=True, batch_jobs=False, **kwargs):
        if session:
            rec = self.session.get(url, **kwargs)
        else:
            rec = requests.get(url, **kwargs)
        if batch_jobs:
            result = json.loads(rec.text)
            if result.get('returnCode') == 'SUCCESS':
                self.text = json.loads(rec.text).get('response').get('nodeValue')
                logging.info('xml返回值为：%s' % self.text)
                return self.text
        else:
            self.text = rec.text
        logging.info(self.text)

    @time_statistics
    def post(self, url, data=None, json=None, session=True, **kwargs):
        if session:
            rec = self.session.post(url, data, json, **kwargs)
        else:
            rec = requests.post(url, data, json, **kwargs)
        self.text = rec.text
        logging.info(self.text)

    @staticmethod
    def db_select(sql):
        rec = db1.db_select(sql)
        return rec

    @staticmethod
    def db_update(sql):
        return db1.db_update(sql)

    def req_encrypted(self, text):
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        crypt = AES.new(self.key)
        text = text.encode('unicode_escape').decode('gb2312')
        text = crypt.encrypt(pad(text))
        return base64.b64encode(text).decode("gb2312")

    def sign_encrypted(self, fun_code, user_id, req_encrypted):
        req_encrypted = req_encrypted
        sign_str = 'FUN_CODE='+fun_code+'&REQ_ENCRYPTED='+req_encrypted+'&USER_ID='+user_id+'&KEY='+self.key
        sign_encrypted = md5_encryption(sign_str)
        return sign_encrypted.upper()

    def build_xml(self, fun_code, user_id, text):
        req_encrypted = self.req_encrypted(text)
        sign_encrypted = self.sign_encrypted(fun_code, user_id, req_encrypted)
        xml = """<?xml version="1.0" encoding="utf-8"?>\
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">\
<soap:Body><RegService xmlns="http://tempuri.org/"><xml>\
&lt;?xml version="1.0" encoding="UTF-8"?&gt;\
&lt;ROOT&gt;\
&lt;FUN_CODE&gt;&lt;![CDATA[%s]]&gt;&lt;/FUN_CODE&gt;\
&lt;USER_ID&gt;&lt;![CDATA[%s]]&gt;&lt;/USER_ID&gt;\
&lt;SIGN&gt;&lt;![CDATA[%s]]&gt;&lt;/SIGN&gt;\
&lt;SIGN_TYPE&gt;&lt;![CDATA[MD5]]&gt;&lt;/SIGN_TYPE&gt;\
&lt;REQ_ENCRYPTED&gt;&lt;![CDATA[%s]]&gt;&lt;/REQ_ENCRYPTED&gt;\
&lt;/ROOT&gt;\
</xml></RegService></soap:Body></soap:Envelope>""" % (fun_code, user_id, sign_encrypted, req_encrypted)
        return xml

    def res_regex(self):
        regex = re.compile(r"RES_ENCRYPTED&gt;&lt;!\[CDATA\[(.+)\]{2}")
        regex_text = regex.search(self.text)
        if regex_text:
            return regex_text.group(1)

    def res_decrypt(self):
        text = self.res_regex()
        if text:
            crypt = AES.new(self.key)
            text = crypt.decrypt(base64.b64decode(text))
            logging.info('res解密后的XML为：%s' % text)
            return text

    @staticmethod
    def xml_replace(xml, old, new):
        res_path = get_project_path() + 'service/4.0前置模拟服务/config/res/'
        xml_path = os.path.join(res_path, xml)
        if not os.path.isfile(xml_path):
            raise Exception(u'XML文件不存在')
        with open(xml_path, 'r') as f:
            content = f.read()
            content = re.sub('gb2312', 'utf-8', content)
            content = content.replace(old, new)
        with open(xml_path, 'w') as f:
            f.write(content)

if __name__ == '__main__':
    driver = IntDriver()
    headers = {'Content-type': 'text/xml'}
    url = 'http://qlcyy.test.jkt.guahao-inc.com/ApiService.asmx'
    data = driver.build_xml('5001','QLCCSYY_WX','<REQ>  <STOP_TIME>    <DEPT_ID><![CDATA[0401]]></DEPT_ID>    <DOCTOR_ID><![CDATA[080]]></DOCTOR_ID>    <REG_DATE><![CDATA[2018-04-04]]></REG_DATE>    <TIME_FLAG><![CDATA[1]]></TIME_FLAG>    <BEGIN_TIME><![CDATA[]]></BEGIN_TIME>    <END_TIME><![CDATA[]]></END_TIME>  </STOP_TIME>  <STOP_REMARK><![CDATA[自动化测试]]></STOP_REMARK>  <HOS_ID><![CDATA[21010001]]></HOS_ID></REQ>')
    driver.post(url=url, data=data, headers=headers)
    print(driver.text)
