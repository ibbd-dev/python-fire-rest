# -*- coding: utf-8 -*-
#
# 需要训练的模型测试
# Author: alex
# Created Time: 2018年05月09日 星期三 18时29分59秒
from fireRest import Model
from sklearn.linear_model import LogisticRegression


class linear(Model):
    """线性模型"""

    def train(self, X, y, model_name, penalty='l2'):
        """LogisticRegression: logistic回归模型
        logistic回归是一种广义的线性回归分析模型，常用于数据挖掘，疾病自动诊断，经济预测等领域。例如，探讨引发疾病的危险因素，并根据危险因素预测疾病发生的概率等。

        Args:
            X: list, 自变量，值如：[[0, 0], [1, 1], [2, 2]]
            y: list, 因变量，值如：[0, 1, 2]
            penalty: str, 惩罚项，默认为l2，支持取值：l1, l2

        Returns:
            coef: list, 线性模型的系数

        Examples:
            curl -XPOST localhost:20920/linear/logistic -d '{"X": [[0, 0], [1, 1], [2, 2]], "y": [0, 1, 2]}'
            注意：这里localhost需要换成实际的host
        """
        lr = LogisticRegression(penalty=penalty)
        lr.fit(X, y)
        self.save(lr, model_name)
        return {
            'coef': lr.coef_.tolist(),
        }

    def test(self, X, y, model_name):
        """模型测试"""
        model = self.load(model_name)
        predict_y = model.predict(X)
        return {
            "predict_y": predict_y
        }

    def predict(self, X, model_name):
        """模型预测"""
        model = self.load(model_name)
        predict_y = model.predict(X)
        return {
            "predict_y": predict_y
        }


if __name__ == "__main__":
    l = linear()
    print(l.train([[0, 0], [1, 1], [2, 2]], [0, 1, 2]))
