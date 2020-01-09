# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2020年01月09日 星期四 18时13分54秒
import requests


res = requests.post('http://localhost:5000/upload',
                    files={
                        'file': open('/tmp/test.png', 'rb')
                    }).json()

print(res)
