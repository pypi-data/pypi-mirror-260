# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 15:56
import time
from abc import ABCMeta, abstractmethod

'''
IDS
'''


class Product(metaclass=ABCMeta):
    def __init__(self, path):
        self.path = path

    @abstractmethod
    def install(self, pkg_path):  # 执行产品安装
        pass

    @abstractmethod
    def set_machine(self, machine):  # 设置产品在哪个machine上
        pass

    @abstractmethod
    def get_machine(self):  # 获取产品所属的machine
        pass

    @abstractmethod
    def set_path(self, path):  # 设置产品的路径
        pass

    @abstractmethod
    def get_path(self):  # 获取产品的路径
        pass


class IDS(Product):

    def __init__(self, path, machine):
        super().__init__(path)
        self.machine = machine
        self.path = path

    @property
    def session(self):
        return self.machine.session

    def install(self, pkg_path):  # 执行ids安装
        target_path = "/tmp/ids_{}".format(time.time())  # 安装包解压目录
        code, out = self.session.run_cmd(f"rm -rf {self.path}; mkdir -p {target_path} {self.path}")
        if code != 0:
            raise Exception(f"创建ids安装包解压目录 {target_path} 或 安装目录 {self.path}失败, 错误码{code}， 错误信息{out}")
        else:
            code, out = self.machine.run_cmd(
                f"tar -xf {pkg_path} -C {target_path};cd {target_path};./ids_install -i silent -DLICENSE_ACCEPTED=TRUE -DUSER_INSTALL_DIR={self.path}")
            if code != 0:
                raise Exception(f"执行ids安装失败, 错误码{code}， 错误信息{out}")

    def set_machine(self, machine):  # 设置ids在哪个machine上
        self.machine = machine

    def get_machine(self):  # 获取ids所属的machine
        return self.machine

    def set_path(self, path):  # 设置ids的路径
        self.path = path

    def get_path(self):  # 获取ids的路径
        return self.path


class CSDK(Product):

    def __init__(self, path, machine):
        super().__init__(path)
        self.machine = machine
        self.path = path

    @property
    def session(self):
        return self.machine.session

    def install(self, pkg_path):  # 执行ids安装
        target_path = "/tmp/csdk_{}".format(time.time())  # 安装包解压目录
        code, out = self.session.run_cmd(f"mkdir -p {target_path} {self.path}")
        if code != 0:
            raise Exception(f"创建csdk安装包解压目录 {target_path} 或 安装目录 {self.path}失败, 错误码{code}， 错误信息{out}")
        else:
            code, out = self.machine.run_cmd(
                f"tar -xf {pkg_path} -C {target_path};cd {target_path};./installclientsdk -i silent -DLICENSE_ACCEPTED=TRUE -DUSER_INSTALL_DIR={self.path}")
            if code != 0:
                raise Exception(f"执行csdk安装失败, 错误码{code}， 错误信息{out}")

    def set_machine(self, machine):  # 设置ids在哪个machine上
        self.machine = machine

    def get_machine(self):  # 获取ids所属的machine
        return self.machine

    def set_path(self, path):  # 设置ids的路径
        self.path = path

    def get_path(self):  # 获取ids的路径
        return self.path
