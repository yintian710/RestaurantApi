# -*- coding: utf-8 -*-
"""
@File  : common.py
@Author: yintian
@Date  : 2021/3/31 15:40
@Desc  : 公共方法模块
"""
import re

from sql.employ import select_wx, select_user_info
from tool.CONTANT import pa
from tool.util.Result import Result


def get_return(msg, need=None, code=0, **kwargs):
    """
    获取一个符合flask返回格式的dict
    :param need: 需要额外发送的数据
    :param msg: 返回给私聊的信息
    :param code: 状态码, 目前无使用,默认就好
    :return:
    """
    if need is None:
        need = {}
    if kwargs:
        need.update(kwargs)
    res = Result(message=msg, code=code, need=need)
    return res


def is_regis(func):
    """
    装饰器, 检查调用进入某方法的用户是否已注册
    需要装饰几乎所有被 Main 入口调用的方法
    :param func: 被装饰的方法,也就是用户进入的方法
    :return:
    """

    def inner(user_id, *args, **kwargs):
        """
        查询数据库中"wx"库,是否包含该用户信息,若无,则返回需要注册,有则代表已注册,执行被装饰的方法,返回其返回结果
        :param user_id:
        :param args:
        :param kwargs:
        :return:
        """
        if isinstance(user_id, str):
            key = user_id
        else:
            key = user_id.user_id
        if not select_wx(key, 'user_id'):
            return get_return('您还没有注册，请先注册', code=1)
        return func(user_id, *args, **kwargs)

    return inner


def is_admin(func):
    """
    检查进入方法的用户是否为管理员
    :param func:
    :return:
    """

    def inner(user_id, *args, **kwargs):
        """
        类似,检查"u"表中用户的"permission"字段,若为"admin"则放行,不然返回pa,
        :param user_id:
        :param args:
        :param kwargs:
        :return:
        """
        permission = select_user_info(user_id, 'permission')
        if not permission or permission != ('admin',):
            return pa
        return func(user_id, *args, **kwargs)

    return inner


def str_to_python_code(_str1):
    """
    将字符串转为python代码并执行
    :param _str1: 传入的字符串
    :return:
    """
    try:
        if 'time.sleep' in _str1:
            return 'sleep方法暂不支持。'
        _str1 = 'str1=""' + re.sub('print\(', 'str1 += f"\\\\n" + str(', _str1)
        print(_str1)
        write = '\nwith open("str.txt", "w", encoding="utf-8"' + ') as f:\n f.write(str(str1))'
        exec(_str1 + write)
        with open("str.txt", "r", encoding="utf-8") as f:
            str2 = f.read()
        # os.remove("str.txt")
        return str2
    except Exception as e:
        return e


def get_random_value_dict_for_dict_weight(list1: list, value: str, weight: str, ignore=None):
    res_dict = {'value': [], 'weight': []}
    for _ in list1:
        k = _[value]
        if ignore and k == ignore:
            continue
        v = _[weight]
        res_dict['value'].append(k)
        res_dict['weight'].append(v)
    return res_dict


if __name__ == '__main__':
    str1 = """print(136845)"""
    a = str_to_python_code(str1)
    print(a)
