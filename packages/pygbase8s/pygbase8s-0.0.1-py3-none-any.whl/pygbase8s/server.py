# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 12:06
from multiprocessing import Value
from pygbase8s.instance import Instance
from pygbase8s.env import ENV

'''
实例
'''


class Server(Instance):

    def __init__(self, name, ids, onconfig, sqlhosts):
        super().__init__()
        self._ids = ids
        self._name = name
        self._onconfig = onconfig
        self._sqlhosts = sqlhosts
        self._idle = Value('b', True)
        self._path = "{ids_path}/{server_name}".format(
            ids_path=self.ids.path,
            server_name=self.name)
        self._env = ENV()
        self._env.set_variable('GBASEDBTDIR', self.ids.path)
        self._env.set_variable('ONCONFIG', f'onconfig.{self.onconfig.name}')
        self._env.set_variable('GBASEDBTSQLHOSTS', self.sqlhosts.path)
        self._env.set_variable('GBASEDBTSERVER', self.name)
        self._env.set_variable('PATH', f"{self.ids.path}/bin:{self.ids.path}/extend/krakatoa/jre/bin:$PATH")

    def reconnect(self):
        self.ids.machine.reconnect()

    @property
    def ids(self):
        return self._ids

    @property
    def session(self):
        self.ids.session.env.update(self.env)
        return self.ids.session

    @property
    def ip(self):  # 返回实例ip
        return self.sqlhosts.get_ip(self.name)

    @property
    def port(self):
        return self.sqlhosts.get_port(self.name)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def idle(self):
        return self._idle

    def initialize(self):  # 初始化实例
        code, out = self.run_cmd("touch rootdbs;chmod 660 rootdbs;chown gbasedbt:gbasedbt rootdbs", cwd=self.path)
        if code != 0:
            raise Exception(f"修改rootdbs权限失败，错误码{code}, 错误信息{out}")
        code, out = self.run_cmd("oninit -ivwy", cwd=self.path)
        if code != 0:
            raise Exception(f"实例初始化失败，错误码{code}, 错误信息{out}")

    def startup(self):  # 启动实例
        code, out = self.run_cmd('oninit -vwy', cwd=self.path)
        if code != 0:
            raise Exception(f"实例启动失败，错误码{code}, 错误信息{out}")

    def shutdown(self):  # 关停实例
        code, out = self.run_cmd('onmode -ky;onclean -ky')
        if code != 0:
            raise Exception(f"关停实例失败，错误码{code}, 错误信息{out}")

    def release(self):  # 设置实例状态为空闲状态
        with self.idle.get_lock():
            self.idle.value = True

    def is_idle(self):  # 返回实例是否空闲
        return self.idle.value

    def occupy(self):  # 设置实例状态为使用状态
        with self.idle.get_lock():
            self.idle.value = False
