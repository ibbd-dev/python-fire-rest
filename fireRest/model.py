# -*- coding: utf-8 -*-
#
# 模型的基类
# Author: alex
# Created Time: 2018年05月09日 星期三 17时55分40秒
import pickle
from werkzeug.utils import secure_filename


class Model:
    """模型基类"""
    _model_default_path = "save_models"

    def set_save_model_path(self, path):
        self.path = "./%s/%s/" % (self._model_default_path, path)

    def save(self, model, model_name):
        """模型保存
        Args:
            model: 模型对象
            model_name: 模型保存的名字
        """
        if model_name != secure_filename:
            raise Exception("model_name is error!")
        if model_name == "":
            raise Exception("model_name cannot be empty!")
        path = self.path + model_name + ".model"
        with open(path, "wb+", encoding="utf8") as w:
            pickle.dump(model, w)

    def load(self, model_name):
        if model_name != secure_filename:
            raise Exception("model_name is error!")
        if model_name == "":
            raise Exception("model_name cannot be empty!")
        path = self.path + model_name + ".model"
        with open(path, "rb", encoding="utf8") as r:
            return pickle.load(r)
        raise Exception("Error when read from model_name")
