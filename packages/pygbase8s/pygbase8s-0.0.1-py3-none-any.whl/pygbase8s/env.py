# coding: utf-8
# @Time    : 2024/3/6 9:38
# @Author  : wangwei
'''
环境变量
'''


class ENV:

    def __init__(self):
        self._variables = {}

    def set_variable(self, key, value):
        self._variables[key] = value

    def unset_variable(self, key):
        self._variables[key] = None

    def get_variable(self, key):
        return self._variables.get(key, '')

    def get_variables(self):
        return self._variables

    def update(self, env):
        self._variables.update(env.get_variables())

    def __str__(self):
        return '\n'.join([f"export {k}={v}" if v else f'unset {k}'for k, v in self.get_variables().items()])


if __name__ == '__main__':

    env = ENV()
    env.set_variable('DB_LOCALE', 'zh_CN.utf8')
    env.set_variable('CLIENT_LOCALE', 'zh_CN.utf8')
    env.set_variable('GBASEDBTDIR', '/data/wangwei/gbase8s')
    print(env)
