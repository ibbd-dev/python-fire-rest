# -*- coding: utf-8 -*-
#
# 存储
# Author: alex
# Created Time: 2018年04月18日 星期三 09时50分31秒
import os
import pickle


class FileStorage:
    path = ""

    def init(self, path):
        if path[-1] != "/":
            path += "/"
        self.path = path
        if not os.path.exists(path):
            raise Exception("%s is not exists!" % path)

    def get_path(self, func_name, cls_name):
        path = self.path
        if len(cls_name) > 0:
            path += cls_name + '/'
        return path + func_name + '/'

    def init_func(self, func_name, cls_name=""):
        """初始化路径
        Args:
            func_name: 函数名
            cls_name: 类名，可能为空
        """
        path = self.get_path(func_name, cls_name)
        if not os.path.exists(path):
            os.mkdir(path, mode=0o644)

    def save(self, name, model, func_name, cls_name="", desc=""):
        """模型保存
        Args:
            name: 模型名字
            model: 模型对象
            func_name: 函数名
            cls_name: 类名，可能为空
            desc: 模型描述
        """
        fname = self.get_path(func_name, cls_name) + name + '.model'
        with open(fname, 'w', encoding='utf8') as f:
            pickle.dump(model, f)
        return True

    def load(self, name, func_name, cls_name=""):
        """获取模型"""
        fname = self.get_path(func_name, cls_name) + name + '.model'
        with open(fname, encoding='utf8') as f:
            return pickle.load(f)


storage = FileStorage()
