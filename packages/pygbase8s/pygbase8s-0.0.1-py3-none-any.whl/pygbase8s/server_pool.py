# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 11:56
from pygbase8s.server import Server
from pygbase8s.cluster import *
from pygbase8s.onconfig import ServerOnconfig
from pygbase8s.sqlhosts import ServerSQLHosts
from multiprocessing import Lock

'''
实例池
'''


class ServerPool:

    def __init__(self, ids, count):
        self.ids = ids
        self.count = count
        self.base_name = 'gbase'
        self.servers = []
        self.lock = Lock()
        self.ports = []

    @property
    def session(self):
        return self.ids.session

    def initialize(self):  # 初始化实例池中的实例
        server_nums = self._get_free_server_num(self.count)
        self.ports = self._get_free_server_port(self.count)
        sqlhosts = ServerSQLHosts(ids=self.ids, name=self.base_name)
        sqlhosts.initialize()
        for i in range(self.count):
            server_name = self.base_name + str(i)
            onconfig = ServerOnconfig(ids=self.ids, name=server_name)
            onconfig.initialize()
            onconfig.set_variable("DBSERVERNAME", server_name)
            onconfig.set_variable("SERVERNUM", server_nums[i])
            sqlhosts.add_server(servername=server_name, ip=self.ids.session.ip, port=self.ports[i])
            server = Server(ids=self.ids, name=server_name, onconfig=onconfig, sqlhosts=sqlhosts)
            server.run_cmd(f"cd {self.ids.path}; mkdir {server.name};chmod 755 {server.name}")
            server.path = f"{self.ids.path}/{server.name}"
            self.servers.append(server)

    def get_server(self):  # 从实例池中返回一个实例
        with self.lock:
            while True:
                for server in self.servers:
                    if server.is_idle():  # 返回一个空闲的实例，并设置为使用状态
                        server.occupy()
                        return server

    def get_cluster(self, type: str):  # 从实例池中返回一个集群
        primary_node = self.get_server()
        bak_node = self.get_server()
        if type.upper() == 'SDS':
            return SDSCluster(primary_node, bak_node)
        elif type.upper() == 'HDR':
            return HDRCluster(primary_node, bak_node)
        elif type.upper() == 'RSS':
            return RSSCluster(primary_node, bak_node)

    def set_base_name(self, base_name):
        self.base_name = base_name

    def _get_free_server_num(self, count):
        server_nums = []
        for i in range(count):
            server_nums.append(self.ids.machine.get_available_server_num())
        return server_nums

    def _get_free_server_port(self, count):
        ports = []
        for i in range(count):
            ports.append(self.ids.machine.get_available_server_port())
        return ports
