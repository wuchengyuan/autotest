#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
mysql数据库操作模块
1、通过select进行数据查询
2、通过update进行数据增加、删除、修改
"""

import time
import functools
import threading
import logging


class Dict(dict):
    """
    字典类,改写构造方法，增加getattr、setattr魔法方法
    """
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def _profiling(start, sql=''):
    """
    监控数据库语句执行时间
    """
    t = time.time() - start
    if t > 0.1:
        logging.warning('[PROFILING] [DB] %s: %s' % (t, sql))
    else:
        logging.info('[PROFILING] [DB] %s: %s' % (t, sql))


class DBError(Exception):
    pass


class MultiColumnsError(DBError):
    pass


class _LazyConnection(object):
    """
    惰性连接类，只有在执行操作时才进行数据库连接
    """

    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            self.connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(self.connection)))
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            logging.info('close connection <%s>...' % hex(id(self.connection)))
            self.connection.close()
            self.connection = None


class _DbCtx(threading.local):
    """
    多线程连接对象，用来连接上下文.
    """
    def __init__(self):
        super(_DbCtx, self).__init__()
        self.connection = None
        self.transactions = 0

    def is_init(self):
        """
        判断连接是否存在
        """
        return not (self.connection is None)

    def init(self):
        """
        执行连接初始化
        """
        logging.info('open lazy connection...')
        self.connection = _LazyConnection()
        self.transactions = 0

    def cleanup(self):
        """
        清除数据库连接
        """
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        """
        返回游标信息
        """
        return self.connection.cursor()


_db_ctx = _DbCtx()


engine = None


class _Engine(object):

    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()


def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
    """
    创建数据库连接对象
    :param user:数据库用户名
    :param password:数据库密码
    :param database:数据库名称
    :param host:数据库主机地址
    :param port:数据库端口
    :param kw:数据库参数
    :return:数据库连接对象
    """
    import mysql.connector
    global engine
    if engine is not None:
        raise DBError('Engine is already initialized.')
    params = dict(user=user, password=password, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.items():
        params[k] = kw.pop(k, v)
    params.update(kw)
    params['buffered'] = True
    engine = _Engine(lambda: mysql.connector.connect(**params))
    logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))


class _ConnectionCtx(object):
    """
    方法可通过with来实现连接和自动关闭数据库的操作
    """
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()


def with_connection(func):
    """
    装饰器方法，通过@with_connection来对方法附加额外功能
    1、通过_ConnectionCtx实现对数据库实现连接和自动关闭
    2、通过_profiling监控sql语句的执行时间
    :param func:
    :return:
    """
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        _start = time.time()
        with _ConnectionCtx():
            f = func(*args, **kw)
            _profiling(_start, *args)
            return f
    return _wrapper


@with_connection
def db_select(sql):
    """
    查询方法
    :param sql:sql语句
    :return:查询结果值：字典类型
    """
    global _db_ctx
    cursor = None
    result = None
    logging.info('SQL: %s' % sql)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql)
        if cursor.description:
            names = [x[0] for x in cursor.description]
            values = cursor.fetchone()
            # result = Dict(names, values)
            if values is not None:
                result = str(values[0])
        logging.info(u'数据库查询数据：%s' % result)
        return result
    finally:
        if cursor:
            cursor.close()


@with_connection
def db_update(sql):
    global _db_ctx
    cursor = None
    logging.info('SQL: %s' % sql)
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql)
        r = cursor.rowcount
        if _db_ctx.transactions == 0:
            logging.info('auto commit')
            _db_ctx.connection.commit()
        return r
    finally:
        if cursor:
            cursor.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
