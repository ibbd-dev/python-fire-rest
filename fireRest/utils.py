# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2019年09月04日 星期三 09时31分18秒
import json
import numpy as np


class RestEncoder(json.JSONEncoder):
    """
    使用：json.dumps(data, cls=RestEncoder)
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj, np.bool_):
            return bool(obj)

        return json.JSONEncoder.default(self, obj)
