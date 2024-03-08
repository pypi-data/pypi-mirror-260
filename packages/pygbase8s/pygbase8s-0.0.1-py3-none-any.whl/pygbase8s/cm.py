# coding: utf-8
# @Time    : 2024/3/5 13:39
# @Author  : wangwei
from pygbase8s.instance import Instance
from pygbase8s.env import ENV
from pygbase8s.sqlhosts import CMSQLHosts
from pygbase8s.onconfig import CMOnconfig

'''
Cluster Manager
'''


class CM(Instance):

    def __init__(self, csdk, cluster, name: str=None, port: int=None):
        super().__init__()
        self._csdk = csdk
        self._cluster = cluster
        if not port:
            self._port = self.csdk.machine.get_available_server_port()
        else:
            self._port = port
        if not name:
            self._name = f"{self.cluster.primary_node.name}_{self.cluster.bak_node.name}"
        else:
            self._name = name
        self._sqlhosts = None
        self._onconfig = None
        self._path = self.csdk.path
        self._env = ENV()
        self._env.set_variable('GBASEDBTDIR', self.csdk.path)
        self._env.set_variable('GBASEDBTSQLHOSTS', self.sqlhosts.path)
        self._env.set_variable('GBASEDBTSERVER', None)
        self._env.set_variable('ONCONFIG', self.onconfig.path)
        self._env.set_variable('PATH', f"{self.csdk.path}/bin:$PATH")

    def reconnect(self):
        self.csdk.machine.reconnect()

    @property
    def onconfig(self):
        if not self._onconfig:
            self._onconfig = CMOnconfig(self.csdk, self.name)
            self._onconfig.initialize()
            cluster_info = f'''
            GBASEDBTSERVER db_group
            SLA {self.name} DBSERVERS=PRI+{self.cluster.type.upper()} WORKERS=16
            FOC ORDER=ENABLED TIMEOUT=10 RETRY=1 PRIORITY=1'''
            self._onconfig.add_cluster_info(cluster_info)
        return self._onconfig

    @property
    def sqlhosts(self):
        if not self._sqlhosts:
            self._sqlhosts = CMSQLHosts(self.csdk, self.name)
            self._sqlhosts.initialize()
            self._sqlhosts.add_group(group_name='db_group', i=10, c=1)
            self._sqlhosts.add_server_to_group(self.cluster.primary_node, 'db_group')
            self._sqlhosts.add_server_to_group(self.cluster.bak_node, 'db_group')
            self._sqlhosts.add_group(group_name='cm', i=12, c=0)
            self._sqlhosts.add_server_to_group(self, 'cm')
        return self._sqlhosts

    @property
    def cluster(self):
        return self._cluster

    @property
    def session(self):
        self.csdk.session.env.update(self.env)
        return self.csdk.session

    @property
    def csdk(self):
        return self._csdk

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def ip(self):
        return self.session.ip

    @property
    def port(self):
        return self._port

    def startup(self):  # 启动实例
        code, out = self.run_cmd(f'oncmsm -c {self.onconfig.path}\n', username='gbasedbt')
        if code != 0:
            raise Exception(f"CM启动失败，错误码{code}, 错误信息{out}")

    def shutdown(self):  # 关停实例
        code, out = self.run_cmd(f'oncmsm -k {self.name}', username='gbasedbt')
        if code != 0:
            raise Exception(f"关停CM失败，错误码{code}, 错误信息{out}")
