# -*- coding: utf-8 -*-
# author: wangwei
# datetime: 2024/2/24 15:49
import paramiko
import warnings
from pygbase8s.ssh_session import SSHSession

'''
服务器
'''


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return self.username


class RemoteMachine:
    def __init__(self, ip, password, port=22, server_num_min=200, port_min=50000):
        self.ip = ip
        self.password = password
        self.ssh_port = port
        self.users = {
            'root': User('root', password),
            'gbasedbt': None,
            'general': []
        }
        self._server_num_min = server_num_min
        self._port_min = port_min
        self._general_user = None
        self._session: SSHSession = self.create_session(self.users.get('root'))
        try:
            self._sftp = paramiko.SFTPClient.from_transport(self._session.ssh.get_transport())
        except Exception as e:
            warnings.warn('SFTP启动失败，不支持文件上传/下载')


    @property
    def session(self):
        return self._session

    def reconnect(self, user_name='root'):
        self._session = self.create_session(self.users.get(user_name))
        try:
            self._sftp = paramiko.SFTPClient.from_transport(self._session.ssh.get_transport())
        except Exception as e:
            warnings.warn('SFTP启动失败，不支持文件上传/下载')

    def create_session(self, user: User):
        transport = paramiko.Transport((self.ip, self.ssh_port))
        transport.connect(username=user.username, password=user.password)
        ssh = paramiko.SSHClient()
        ssh._transport = transport
        return SSHSession(ssh=ssh)

    def run_cmd(self, cmd, **kwargs):
        return self.session.run_cmd(cmd, **kwargs)

    def get_ip(self):
        return self.ip

    def add_user(self, user: User):
        code, out = self.run_cmd(f"id -u {user.username}")
        if code != 0:
            code, out = self.run_cmd(f"useradd {user.username}")
            if code != 0:
                raise Exception(f"添加用户{user.username}失败")
        code, out = self.run_cmd(f"echo '{user.password}'|passwd --stdin {user.username}")
        if code != 0:
            raise Exception(f"修改用户{user.username}密码失败")
        else:
            if user.username in ('root', 'gbasedbt'):
                self.users[user.username] = user
            else:
                self.users['general'].append(user)

    def _gen_general_user(self):
        for user in self.users.get('general'):
            yield user

    def get_user(self, type):
        if type in ('root', 'gbasedbt'):
            return self.users.get(type)
        else:
            if self._general_user is None:
                self._general_user = self._gen_general_user()
            return next(self._general_user)

    def get_available_server_num(self):
        for check_num in range(self._server_num_min, 256):
            address = str(hex(0x5256 + check_num))
            code, out = self.session.run_cmd(f"ipcs -m|grep {address}")
            if out == "":
                self._server_num_min = check_num + 1
                return check_num
        raise Exception("无可用的SERVERNUM")

    def get_available_server_port(self):
        for check_port in range(self._port_min, 65535):
            code, out = self.session.run_cmd(f"netstat -an|grep {check_port}")
            if out == "":
                self._port_min = check_port + 1
                return check_port
        raise Exception("无可用的端口")

    @property
    def sftp(self):
        return self._sftp

    def upload(self, local_file, remote_file):
        self.sftp.put(local_file, remote_file)

    def download(self, remote_file, local_file):
        self.sftp.get(remote_file, local_file)

