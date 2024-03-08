# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 21:22
from abc import ABCMeta, abstractmethod

'''
sqlhost实例
'''


class SQLHosts(metaclass=ABCMeta):
    def __init__(self):
        self._name = None

    @property
    def name(self):
        return self._name

    @property
    @abstractmethod
    def session(self):
        pass

    @property
    @abstractmethod
    def path(self):
        pass

    def initialize(self):
        code, out = self.session.run_cmd(f"rm -rf {self.path};touch {self.path}")
        if code != 0:
            raise Exception(f"创建sqlhosts文件失败，错误码{code}, 错误信息{out}")


class CMSQLHosts(SQLHosts):  # 一个实例对应一个集群

    def __init__(self, csdk, name):
        super().__init__()
        self._csdk = csdk
        self._name = name

    @property
    def csdk(self):
        return self._csdk

    @property
    def session(self):
        return self.csdk.session

    @property
    def path(self):
        return f"{self.csdk.path}/etc/sqlhosts.{self.name}"

    def add_group(self, group_name, i, c):
        code, out = self.session.run_cmd(f"echo '{group_name}\tgroup\t-\t-\ti={i},c={c}' >> {self.path}")
        if code != 0:
            raise Exception(f"写入group信息到sqlhosts文件失败，错误码{code}, 错误信息{out}")

    def add_server_to_group(self, server, group_name):
        code, out = self.session.run_cmd(
            f"echo '{server.name}\tonsoctcp\t{server.ip}\t{server.port}\tg={group_name}' >> {self.path}")
        if code != 0:
            raise Exception(f"server信息写入CM sqlhosts文件失败，错误码{code}, 错误信息{out}")


class ServerSQLHosts(SQLHosts):

    def __init__(self, ids, name):
        super().__init__()
        self._ids = ids
        self._name = name
        self._servers = {}

    @property
    def ids(self):
        return self._ids

    @property
    def session(self):
        return self.ids.session

    @property
    def path(self):
        return f"{self.ids.path}/etc/sqlhosts.{self.name}"

    def add_server(self, servername, ip, port):
        self._servers[servername] = (ip, port)
        code, out = self.session.run_cmd(f"echo {servername} onsoctcp {ip} {port} >> {self.path}")
        if code != 0:
            raise Exception(f"添加server到sqlhosts失败，错误码{code}, 错误信息{out}")

    def add_server_to_group(self, servername, ip, port, groupname):
        pass

    def get_port(self, server_name):
        if server_name not in self._servers:
            raise Exception(f"实例 {server_name} 不存在")
        return self._servers.get(server_name)[1]

    def get_ip(self, server_name):
        if server_name not in self._servers:
            raise Exception(f"实例 {server_name} 不存在")
        return self._servers.get(server_name)[0]
