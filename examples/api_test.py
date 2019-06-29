# -*- coding: utf-8 -*-
#
# 使用测试
# Author: alex
# Created Time: 2018年04月02日 星期一 14时53分50秒
from fireRest import API, app, APIException, ErrCodeBase


class Example:
    def hello(self, name='world'):
        if name == 'exception':
            # 可以简单的抛出异常（此时错误码为1）
            raise Exception('演示异常输出')
        return 'Hello {name} in Example!'.format(name=name)


class Example2:
    def hello(self, name='world'):
        if name == 'exception':
            # 可以使用自定义的错误码
            raise APIException('演示错误处理的使用方式', code=10)
        return 'Hello {name} in Example2!'.format(name=name)


def hello(name='world'):
    if name == 'exception':
        # 可以使用系统定义的错误码
        raise APIException('演示错误处理的使用方式',
                           code=ErrCodeBase.err_param)
    return 'Hello {name} in func!'.format(name=name)


if __name__ == '__main__':
    API(Example)
    print("==> curl -XPOST localhost:5000/Example/hello -d '{\"name\": \"IBBD\"}'")

    API(Example2)
    print("==> curl -XPOST localhost:5000/Example2/hello -d '{\"name\": \"IBBD\"}'")

    API(hello)
    print("==> curl -XPOST localhost:5000/hello -d '{\"name\": \"IBBD\"}'")

    app.run(debug=True)
