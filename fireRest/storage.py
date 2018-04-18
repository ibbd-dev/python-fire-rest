# -*- coding: utf-8 -*-
#
# 存储
# Author: alex
# Created Time: 2018年04月18日 星期三 09时50分31秒

class Storage:

    def __init__(self, obj):
        self.obj = obj

    def save(self, name, model, desc=""):
        """模型保存
        Args:
            name: 模型名字
            model: 模型实际参数
            desc: 模型描述
        """

    def get(self, name):
        """获取模型"""
