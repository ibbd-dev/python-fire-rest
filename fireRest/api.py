# -*- coding: utf-8 -*-
#
# 包装API
# Author: alex
# Created Time: 2018年04月02日 星期一 14时34分24秒
import logging
import types
from time import time
from flask import Flask, jsonify
from flask_restful import request
from traceback import format_exc
from jsonschema.exceptions import ValidationError
from .exception import ErrCodeBase, APIException

__all__ = ['API', 'set_app', 'app']

logger = logging.getLogger()
app = Flask(__name__)
app.logger.addHandler(logger)
app.config['JSON_AS_ASCII'] = False

# ctroller action list
action_list = {}
action_names = []  # 用于输出帮助信息

config = {
    "debug": False,
    "version": 'v1.0',
}


@app.errorhandler(APIException)
def err_handler_model(e):
    logger.exception(e)
    return _output_json(None, code=e.code, messages=str(e))


@app.errorhandler(ValidationError)
def err_handler_valid(e):
    logger.exception(e)
    return _output_json(None, code=ErrCodeBase.err_param, messages=str(e))


@app.errorhandler(Exception)
def err_handler_internal(e):
    logger.exception(e)
    msg = str(e) + "\n" + format_exc() if config['debug'] else str(e)
    return _output_json(None, code=ErrCodeBase.unknown, messages=msg)


def API(ctrl):
    """将函数或者类转化为添加Restful API
    Args:
        ctrl: function|class 需要转化的函数或者类
    """
    global action_list, action_names

    ctrl_name = ctrl.__name__
    if isinstance(ctrl, types.FunctionType):  # 函数
        key = (ctrl_name)
        action_list[key] = ctrl
        action_names.append(['/'+ctrl_name, _get_func_help(ctrl)])
        print('Add Function: ', ctrl_name)
        return

    obj = ctrl()
    logger.warning(ctrl_name)
    print('Add Class: ', ctrl_name)
    for func_name in ctrl.__dict__:
        if func_name[:1] == "_":
            continue

        key = (ctrl_name, func_name)
        action_list[key] = getattr(obj, func_name)
        action_names.append(['/'+ctrl_name+'/'+func_name, _get_func_help(action_list[key])])
        print('---> Method: ', func_name)


def set_app(debug: bool = False, version='v1.0'):
    """运行服务
    Args:
        debug: 当该值为True时，会增加异常信息输出，会自动计算接口耗时等
    """
    global config
    config["debug"] = debug
    config["version"] = version


def set_cors():
    global app
    from flask_cors import CORS
    CORS(app, supports_credentials=True)


def set_upload_size(size):
    """设置body大小
    如：1024*1024*2 = 2MB"""
    global app
    app.config['MAX_CONTENT_LENGTH'] = size


def set_param(key, val):
    """设置flask参数
    http://docs.jinkan.org/docs/flask/config.html
    """
    global app
    app.config[key] = val


def _output_json(data, code=0, messages=None, start=None):
    """以json结构返回数据"""
    res = {
        "code": code,
        "messages": messages,
        "data": data,
    }
    if start is not None:
        res['time'] = time() - start

    return jsonify(res)


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


@app.route('/<string:func_name>', methods=['POST'])
def restFunc(func_name):
    """函数API入口"""
    key = (func_name)
    if key not in action_list:
        return "not found!", 404

    start = None if config['debug'] is False else time()
    res = _parse_post(key)
    return _output_json(res, start=start)


@app.route('/<string:func_name>', methods=['GET'])
def getRestFunc(func_name):
    """帮助文档等"""
    key = (func_name)
    if key not in action_list:
        return "not found!", 404

    func = action_list[key]
    return _parse_get(func)


@app.route('/<string:ctrl>/<string:action>', methods=['POST'])
def restClass(ctrl, action):
    """类API入口"""
    key = (ctrl, action)
    if key not in action_list:
        return "not found!", 404

    start = None if config['debug'] is False else time()
    res = _parse_post(key)
    return _output_json(res, start=start)


@app.route('/<string:ctrl>/<string:action>', methods=['GET'])
def getRestClass(ctrl, action):
    """帮助文档等"""
    key = (ctrl, action)
    if key not in action_list:
        return "not found!", 404

    func = action_list[key]
    return _parse_get(func)


def _parse_post(key):
    """执行相应的函数"""
    func = action_list[key]
    params = request.get_json(force=True, silent=True)
    if config["debug"]:
        logger.warning("function: " + func.__name__)
        logger.warning(params)

    if params:
        res = func(**request.json)
    else:
        res = func()

    return res


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
