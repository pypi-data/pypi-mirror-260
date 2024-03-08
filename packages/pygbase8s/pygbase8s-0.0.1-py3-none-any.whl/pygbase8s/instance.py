# coding: utf-8
# @Time    : 2024/3/6 9:15
# @Author  : wangwei
from abc import ABCMeta, abstractmethod

'''
定义GBase8s中操作的实体的抽象类， 包括实例和CM
'''


class Instance(metaclass=ABCMeta):

    def __init__(self):
        self._name = None
        self._ip = None
        self._port = None
        self._onconfig = None
        self._sqlhosts = None
        self._session = None
        self._env = None

    @property
    def name(self):
        return self._name

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def onconfig(self):
        return self._onconfig

    @property
    def sqlhosts(self):
        return self._sqlhosts

    @property
    def env(self):
        return self._env

    @property
    def session(self):
        self._session.env.update(self.env)
        return self._session

    @abstractmethod
    def startup(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    def run_cmd(self, cmd, **kwargs):
        code, out = self.session.run_cmd(cmd, **kwargs)
        return code, out






