# -*- coding: utf-8 -*-
#
# 使用测试
# Author: alex
# Created Time: 2018年04月02日 星期一 14时53分50秒
from fireRest import API, app, APIException


class Example:
    def hello(self, name='world'):
        return 'Hello {name} in Example!'.format(name=name)


class Example2:
    def hello(self, name='world'):
        return 'Hello {name} in Example2!'.format(name=name)


def hello(name='world'):
    if name == 'exception':
        raise APIException('演示错误处理的使用方式',
                           code=100)
    return 'Hello {name} in func!'.format(name=name)


if __name__ == '__main__':
    API(Example)
    API(Example2)
    API(hello)
    app.run(debug=True)
