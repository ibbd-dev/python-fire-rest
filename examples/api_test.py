# -*- coding: utf-8 -*-
#
# 使用测试
# Author: alex
# Created Time: 2018年04月02日 星期一 14时53分50秒
from flask import request
from PIL import Image
from werkzeug import secure_filename
from fireRest import API, app, APIException, ErrCodeBase


class Example:
    def hello(self, name='world'):
        """这是函数的注释"""
        if name == 'exception':
            # 可以简单的抛出异常（此时错误码为1）
            raise Exception('演示异常输出')
        # 可以返回字典
        return {
            "msg": 'Hello {name} in Example!'.format(name=name)
        }


class Example2:
    def hello(self, name='world'):
        """这是函数的注释"""
        if name == 'exception':
            # 可以使用自定义的错误码
            raise APIException('演示错误处理的使用方式', code=10)
        # 可以返回列表
        return ['Hello {name} in Example2!'.format(name=name)]


def hello(name='world'):
    """这是函数的注释"""
    if name == 'exception':
        # 可以使用系统定义的错误码
        raise APIException('演示错误处理的使用方式',
                           code=ErrCodeBase.err_param)
    # 可以返回简单类型，如字符串等
    return 'Hello {name} in func!'.format(name=name)


def upload():
    """上传文件
    注意：上传文件时，不能在函数名upload增加参数，否则会报错
    测试：
    files = {'file': open('/path/to/filename', 'rb')}
    res = requests.post(url, files=files).json()
    """
    ufile = request.files.get('file')
    # 你的处理代码在这里。。。
    # ufile就是文件对象，对应表单域中的file
    # 如果需要可以同时传多个文件对象
    print(type(ufile))   # 对象类型：werkzeug.datastructures.FileStorage

    # ufile.stream 获取文件流对象
    img = Image.open(ufile.stream)

    # 保存文件
    ufile.save('/tmp/' + secure_filename('hello.png'))
    ufile.close()
    return {
        "file": ufile.filename,   # 这里只是一个样例返回
        "size": img.size,
        "mode": img.mode,
    }


if __name__ == '__main__':
    API(Example)
    print("==> curl -XPOST localhost:5000/Example/hello -d '{\"name\": \"IBBD\"}'")

    API(Example2)
    print("==> curl -XPOST localhost:5000/Example2/hello -d '{\"name\": \"IBBD\"}'")

    API(hello)
    print("==> curl -XPOST localhost:5000/hello -d '{\"name\": \"IBBD\"}'")

    API(upload)
    print("==> curl -XPOST localhost:5000/upload -F 'file=@README.md'")

    app.run(debug=True)
