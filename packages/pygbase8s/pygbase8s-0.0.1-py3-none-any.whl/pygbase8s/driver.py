# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/25 10:56
from abc import ABCMeta, abstractmethod
from pygbase8s.connection import JDBCConnection
'''
驱动
'''
class Driver(metaclass=ABCMeta):

    @abstractmethod
    def get_connection(self, server, username, password):
        pass


class JDBCDriver(Driver):

    def get_connection(self, server, username, password):
        return JDBCConnection()