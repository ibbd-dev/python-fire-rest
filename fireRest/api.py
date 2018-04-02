# -*- coding: utf-8 -*-
#
# 包装API
# Author: alex
# Created Time: 2018年04月02日 星期一 14时34分24秒
import logging
from flask import Flask, jsonify
from flask_restful import request

logger = logging.getLogger()
app = Flask(__name__)

# ctroller action list
action_list = {}

config = {
    "debug": False
}


def API(ctrl):
    """添加API"""
    global action_list
    ctrl_name = ctrl.__name__
    logger.warning(ctrl_name)
    obj = ctrl()

    for func in ctrl.__dict__:
        if func[:1] == "_":
            continue

        key = (ctrl_name, func)
        action_list[key] = getattr(obj, func)


def run(port=20920, debug=False):
    """运行服务"""
    global config
    config["debug"] = debug
    app.run(port=port, debug=debug)
    app.logger.addHandler(logger)


def output_json(data, code=0, messages=None):
    """以json结构返回数据"""
    return jsonify({
        "code": code,
        "messages": messages,
        "data": data
    })


@app.route('/<string:ctrl>/<string:action>', methods=['POST'])
def rest(ctrl, action):
    """API入口"""
    params = request.get_json(force=True, silent=True)
    if config["debug"]:
        logger.warning("ctroller: " + ctrl + "  action:" + action)
        logger.warning(len(action_list))
        logger.warning(params)

    key = (ctrl, action)
    if key in action_list:
        if params:
            return action_list[key](**request.json)
        return action_list[key]()

    return "not found!", 404
