# -*- coding: utf-8 -*-
#
# 包装API
# Author: alex
# Created Time: 2018年04月02日 星期一 14时34分24秒
import types
import logging
from flask import Flask, jsonify
from flask_restful import request
from .storage import storage

__all__ = ['API', 'run']

logger = logging.getLogger()
app = Flask(__name__)

# ctroller action list
action_list = {}
action_names = []  # 用于输出帮助信息

config = {
    "debug": False,
    "version": 'v1.0',
    "output_json": True,
}


def API(ctrl):
    """将函数或者类转化为添加Restful API
    Args:
        ctrl: function|class 需要转化的函数或者类
    """
    global action_list, action_names

    ctrl_name = ctrl.__name__
    if type(ctrl) is types.FunctionType:  # 函数
        key = (ctrl_name)
        action_list[key] = ctrl
        action_names.append(['/'+ctrl_name, _get_func_help(ctrl)])
        storage.init_func(ctrl_name)
        return

    logger.warning(ctrl_name)
    obj = ctrl()

    for func_name in ctrl.__dict__:
        if func_name[:1] == "_":
            continue

        key = (ctrl_name, func_name)
        storage.init_func(func_name, ctrl_name)
        action_list[key] = getattr(obj, func_name)
        action_names.append(['/'+ctrl_name+'/'+func_name, _get_func_help(action_list[key])])


def run(port=20920, save_path='/var/www/model', debug=False, version='v1.0'):
    """运行服务
    Args:
        port: 服务运行的端口号，不能跟系统其他服务的有冲突
        save_path: 模型在保存时的存储路径
        debug: 测试标识，测试状态下会输出更多的日志
        version: 服务的版本号，这个信息会在帮助信息输出
    """
    global config
    config["debug"] = debug
    config["version"] = version
    config["output_json"] = True
    app.run(port=port, debug=debug, host='0.0.0.0')
    app.logger.addHandler(logger)
    storage.init(save_path)


def _output_json(data, code=0, messages=None):
    """以json结构返回数据"""
    return jsonify({
        "code": code,
        "messages": messages,
        "data": data
    })


@app.route('/', methods=['GET'])
def getRootHelp():
    """帮助文档"""
    max_l = 0
    for a in action_names:
        if len(a[0]) > max_l:
            max_l = len(a[0])

    max_l += 4
    msg_help = "<pre>API Version " + config['version']
    msg_help += "\n\nSupport Functions:\n\t" + "\n\t".join([a[0]+(" "*(max_l-len(a[0])))+a[1] for a in action_names])
    msg_help += "\n\nThe help of functions:\n\t" + "\n\t".join([a[0]+'?help=true' for a in action_names])
    return msg_help


@app.route('/<string:func_name>/<string:model_action>', methods=['POST'])
def restFunc(func_name, model_action):
    """函数API入口"""
    if not _check_model_action(model_action):
        return 'error model action = %s' % model_action, 404

    key = (func_name)
    if key not in action_list:
        return "not found!", 404

    res = _parse_post(action_list[key])
    if config['output_json']:
        return _output_json(res)
    return res


@app.route('/<string:func_name>', methods=['GET'])
def getRestFunc(func_name):
    """帮助文档等"""
    key = (func_name)
    if key not in action_list:
        return "not found!", 404

    func = action_list[key]
    return _parse_get(func)


@app.route('/<string:ctrl>/<string:action>/<string:model_action>', methods=['POST'])
def restClass(ctrl, action, model_action):
    """类API入口"""
    if not _check_model_action(model_action):
        return 'error model action = %s' % model_action, 404

    key = (ctrl, action)
    if key not in action_list:
        return "not found!", 404

    res = _parse_post(action_list[key])
    if config['output_json']:
        return _output_json(res)
    return res


@app.route('/<string:ctrl>/<string:action>', methods=['GET'])
def getRestClass(ctrl, action):
    """帮助文档等"""
    key = (ctrl, action)
    if key not in action_list:
        return "not found!", 404

    func = action_list[key]
    return _parse_get(func)


def _check_model_action(action):
    if action in ['train', 'test', 'predict']:
        return True
    return False


def _parse_post(func):
    params = request.get_json(force=True, silent=True)
    if config["debug"]:
        logger.warning("function: " + func.__name__)
        logger.warning(params)

    if params:
        return func(**request.json)
    return func()


def _parse_get(func):
    p_help = request.args.get('help', '')
    p_help = p_help.lower()

    if p_help in ['true', '1']:
        return _print_func_help(func)

    return ""


def _print_func_help(func):
    """打印函数的帮助信息"""
    msg_help = '' if func.__doc__ is None else func.__doc__.strip()
    return "<pre>"+msg_help


def _get_func_help(func):
    """获取函数帮助信息的第一行"""
    if func.__doc__ is None:
        return ''
    msg = func.__doc__.split("\n")
    msg[0] = msg[0].strip()
    if len(msg[0]) > 0:
        return msg[0]
    if len(msg) > 1:
        return msg[1].strip()
    return ''
