# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2018年04月02日 星期一 14时53分50秒
from api import API, run, output_json


def hello(name='world'):
    return output_json('Hello {name} in func!'.format(name=name))


if __name__ == '__main__':
    API(hello)
    run(debug=True)
