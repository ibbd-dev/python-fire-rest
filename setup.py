# -*- coding: utf-8 -*-
#
# 安装程序
# Author: alex
# Created Time: 2018年04月02日 星期一 17时29分45秒
#from setuptools import setup
from distutils.core import setup


LONG_DESCRIPTION = """
Python fireRest is a library for automatically generating restful api interfaces
(APIs) with a single line of code.
It will turn any Python class or function into a API.

快速将函数或者对象包装成Restful接口。

This idea comes from: https://github.com/google/python-fire
""".strip()

SHORT_DESCRIPTION = """
A library for automatically generating restful api interfaces.""".strip()

DEPENDENCIES = [
    'flask',
    'jsonschema',
    'flask_restful',
    'json-tricks',
]

VERSION = '0.3.3'
URL = 'https://github.com/ibbd-dev/python-fire-rest'

setup(
    name='fireRest',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Alex Cai',
    author_email='cyy0523xc@gmail.com',
    license='Apache Software License',

    keywords='restful api interface for python',

    packages=['fireRest'],
)
