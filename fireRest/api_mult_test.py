# -*- coding: utf-8 -*-
#
# 多个对象
# Author: alex
# Created Time: 2018年04月02日 星期一 14时53分50秒
from api import API, run, output_json


class Example:
    def hello(self, name='world'):
        """这是Example的hello帮助文档"""
        return output_json('Hello {name} in Example!'.format(name=name))


class Example2:
    def hello(self, name='world'):
        """
        这是Example2的hello帮助文档
        """
        return output_json('Hello {name} in Example2!'.format(name=name))


if __name__ == '__main__':
    API(Example)
    API(Example2)
    run(debug=True)
