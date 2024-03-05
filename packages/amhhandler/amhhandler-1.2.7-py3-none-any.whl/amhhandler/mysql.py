#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@time   : 2020/9/21 16:39
@file   : mysql.py
@author : 
@desc   : 
@exec   : 
"""
import sys
import pymysql
from pymysql.cursors import DictCursor


class Conn(object):
    """定义一个 MySQL 操作类"""

    def __init__(self, **config):
        """初始化数据库信息并创建数据库连接"""
        if config:
            for k, v in config.items():
                if k == 'charset' and v not in ('utf8', 'utf8mb4'):
                    config[k] = 'utf8mb4'
                if k == 'port' and not isinstance(v, int):
                    try:
                        config[k] = int(v)
                    except:
                        config[k] = 3306
        else:
            sys.exit("Connect config can not be empty!")

        try:
            self.conn = pymysql.connect(**config)
        except Exception as e:
            sys.exit(e)
        try:
            # 测试mysql是否通
            self.cur = self.conn.cursor()
        except Exception as e:
            sys.exit(e)

    def select(self, select_sql, return_type=None):
        """执行select, show 类查询，有返回值"""
        if return_type and return_type.lower() in ("dict", "d"):
            self.cur = self.conn.cursor(DictCursor)
        try:
            self.cur.execute(select_sql)
            rt_tuple = self.cur.fetchall()
            return rt_tuple
        except Exception as e:
            print(e)
            return b''

    def exec(self, sql):
        """执行非查询类语句"""
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)

    def close(self):
        self.cur.close()
        self.conn.close()
