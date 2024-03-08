# coding: utf-8
# @Time    : 2024/3/5 10:01
# @Author  : wangwei
from abc import ABCMeta, abstractmethod


class Cluster(metaclass=ABCMeta):

    def __init__(self, primary_node, bak_node):
        self._primary_node = primary_node
        self._bak_node = bak_node

    @abstractmethod
    def initialize(self):  # 初始化实例
        pass

    @property
    def primary_node(self):
        return self.primary_node


    @property
    def bak_node(self):
        return self.bak_node

    def release(self):
        self.primary_node.release()
        self.bak_node.release()


class SDSCluster(Cluster):
    type = 'SDS'

    def initialize(self):
        self.bak_node.onconfig.set_variable('SDS_ENABLE', '1')
        self.bak_node.run_cmd('cd {0}; touch sdstmp1 sdstmp2;chown gbasedbt:gbasedbt sdstmp1 sdstmp2; chmod 660 '
                              'sdstmp1 sdstmp2'.format(self.bak_node.path))
        self.bak_node.onconfig.set_variable('SDS_PAGING', '{0}/sdstmp1,{0}/sdstmp2'.format(self.bak_node.path))
        self.bak_node.run_cmd(
            f'cd {self.bak_node.path}; touch sdstmpdbs1;chown gbasedbt:gbasedbt sdstmpdbs1; chmod 660 sdstmpdbs1')
        self.bak_node.onconfig.set_variable('SDS_TEMPDBS',
                                            f'sdstmpdbs1, {self.bak_node.path}/sdstmpdbs1,2,0,16000')
        self.primary_node.initialize()
        self.primary_node.run_cmd(f'onmode -d set SDS primary {self.primary_node.name}')
        self.bak_node.path = self.primary_node.path
        self.bak_node.startup()


class HDRCluster(Cluster):
    type = 'HDR'

    def initialize(self):
        for node in [self.primary_node, self.bak_node]:
            node.onconfig.set_variable('DRAUTO', '3')
            node.onconfig.set_variable('DRINTERVAL', '30')
            node.onconfig.set_variable('DRTIMEOUT', '30')
            node.onconfig.set_variable('HA_FOC_ORDER', 'HDR')
            node.onconfig.set_variable('UPDATABLE_SECONDARY', '0')
            node.onconfig.set_variable('DRLOSTFOUND', '$GBASEDBTDIR/etc/dr.lostfound')
        self.primary_node.initialize()
        self.primary_node.run_cmd(f'onmode -d primary {self.bak_node.name}')
        # 主做0及备份
        self.primary_node.run_cmd(f'ontape -s -L 0 -t STDIO > tape_L0', cwd=self.primary_node.path)
        # 备做备份恢复
        self.bak_node.run_cmd(f'cat {self.primary_node.path}/tape_L0|ontape -p -t STDIO', cwd=self.bak_node.path)
        self.bak_node.run_cmd(f'onmode -d secondary {self.primary_node.name}')


class RSSCluster(Cluster):
    type='RSS'

    def initialize(self):
        self.primary_node.onconfig.set_variable('LOG_INDEX_BUILDS', '1')
        self.primary_node.initialize()
        self.primary_node.run_cmd(f'onmode -d add RSS {self.bak_node.name}')
        # 主做0及备份
        self.primary_node.run_cmd(f'ontape -s -L 0 -t STDIO > tape_L0', cwd=self.primary_node.path)
        # 备做备份恢复
        self.bak_node.run_cmd(f'cat {self.primary_node.path}/tape_L0|ontape -p -t STDIO', cwd=self.bak_node.path)
        self.bak_node.run_cmd(f'onmode -d RSS {self.primary_node.name}')



