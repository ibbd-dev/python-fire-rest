# -*- coding: utf-8 -*-
#
# 异常相关
# Author: alex
# Created Time: 2018年11月30日 星期五 09时47分38秒


class ErrCodeBase:
    """基础错误代码"""
    unknown = 1    # 未知错误
    err_param = 2  # 参数错误


class APIException(Exception):
    def __init__(self, messages, code=1):
        """
        Args:
            msg: 错误信息
            code: 错误代码
        """
        self._code = code
        super(Exception, self).__init__(messages)

    @property
    def code(self):
        return self._code
