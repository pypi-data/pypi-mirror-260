# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 20:59

'''
onconfig实例,对应实例或CM
'''
from abc import ABCMeta, abstractmethod


class Onconfig(metaclass=ABCMeta):
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

    @abstractmethod
    def initialize(self):
        pass

    def get_variable(self, key):
        code, out = self.session.run_cmd(f"grep -E '^{key}(\s*|\s+.*)$' {self.path}")
        if code != 0:
            raise Exception(f"获取onconfig变量失败，错误码{code}, 错误信息{out}")
        return out.split(maxsplit=1)[1]

    def set_variable(self, key, value):
        if key in ['VPCLASS', 'BUFFERPOOL']:
            regx = '^' + key + '\s+' + value.split(',')[0] + '.*'
        else:
            regx = '^' + key + '(\s*|\s+.*)$'
        grepcmd = f"grep -E '{regx}' {self.path}"
        code, out = self.session.run_cmd(grepcmd)
        if out == "":  # 要修改的参数不存在
            code, out = self.session.run_cmd(f"echo '{key} {value}' >> {self.path}")
        else:
            code, out = self.session.run_cmd(f"sed -ri 's#{regx}#{key} {value}#g' {self.path}")
        if code != 0:
            raise Exception(f"修改onconfig参数失败，错误码{code}, 错误信息{out}")


class CMOnconfig(Onconfig):
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
        return f"{self.csdk.path}/etc/oncmsm.{self.name}"

    def initialize(self):
        code, out = self.session.run_cmd(f"rm -rf {self.path}; "
                                         f"touch {self.path}; chown gbasedbt:gbasedbt {self.path}")
        if code != 0:
            raise Exception(f"创建onconfig.{self.name}失败，错误码{code}, 错误信息{out}")
        self.set_variable('NAME', self.name)
        self.set_variable('LOGFILE', '${GBASEDBTDIR}/tmp/%s.log' % self.name)
        self.set_variable('CM_TIMEOUT', '30')
        self.set_variable('SECONDARY_EVENT_TIMEOUT', '15')
        self.set_variable('SQLHOSTS', 'LOCAL')
        self.set_variable('LOCAL_IP', self.session.ip)
        self.set_variable('EVENT_TIMEOUT', '30')
        self.set_variable('LOG', '1')
        self.set_variable('DEBUG', '0')
        self.set_variable('CLUSTER', 'cluster1')

    def add_cluster_info(self, cluster_info):
        code, out = self.session.run_cmd("echo '{\n%s\n}' >> %s" % (cluster_info, self.path))
        if code != 0:
            raise Exception(f"添加cluster信息到cmonconfig文件失败，错误码{code}, 错误信息{out}")


class ServerOnconfig(Onconfig):

    def __init__(self, ids, name):
        super().__init__()
        self._ids = ids
        self._name = name

    @property
    def ids(self):
        return self._ids

    @property
    def session(self):
        return self.ids.session

    @property
    def path(self):
        return f"{self.ids.path}/etc/onconfig.{self.name}"

    def initialize(self):
        code, out = self.session.run_cmd(f"cd {self.ids.path}/etc;cp -rf onconfig.std onconfig.{self.name};"
                                         f"chown gbasedbt:gbasedbt onconfig.{self.name}")
        if code != 0:
            raise Exception(f"复制onconfig.std失败，错误码{code}, 错误信息{out}")
        self.set_variable("ROOTPATH", "./rootdbs")
        self.set_variable("ROOTSIZE", "204800")
        self.set_variable("MSGPATH", "$GBASEDBTDIR/tmp/online_{}.log".format(self.name))
        self.set_variable("FULL_DISK_INIT", "-1")
        self.set_variable("TAPEDEV", "/dev/null")
        self.set_variable("LTAPEDEV", "/dev/null")
