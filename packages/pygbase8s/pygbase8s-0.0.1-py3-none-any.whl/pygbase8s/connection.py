# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/25 10:58
from abc import ABCMeta, abstractmethod
'''
数据库连接对象
'''
class Connection:

    @abstractmethod
    def execute(self, sql):
        pass


class JDBCConnection(Connection):
    def execute(self, sql):
        print("使用jdbc执行sql：{}".format(sql))