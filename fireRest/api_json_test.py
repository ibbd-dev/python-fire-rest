# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2018年04月02日 星期一 14时53分50秒
from api import API, run


class Example:
    def hello(self, name='world'):
        return 'Hello {name}!'.format(name=name)


if __name__ == '__main__':
    API(Example)
    run(debug=True)
