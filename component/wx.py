# -*- coding: utf-8 -*-
"""
@File  : wx.py
@Author: yintian
@Date  : 2021/5/14 14:27
@Desc  : 
"""
import json

import aiohttp

from sql.employ import select_id_in_wx, select_base, insert_base
from tool.common import get_return
from tool.util import log_print


async def get_login_openid(data):
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = data['params']
    headers = {
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as s:
        async with s.get(url=url, params=params, headers=headers) as res:
            if res.status != 200:
                return get_return('获取失败', code=1)
            data_json = await res.text()
            data_json = json.loads(data_json)
            if data_json.get('openid'):
                return get_return('获取成功', need=data_json)
            else:
                return get_return('获取失败', code=1)


def regis(openid):
    bases = ['wx', 'user_info']
    for base in bases:
        res = select_base(base, openid, 'user_id')
        if not res:
            log_print(base, '-', openid)
            insert_base(base, openid)


def is_wx_regis(openid):
    """
    查询是否已经绑定小程序
    :param openid:
    :return:
    """
    res = select_id_in_wx(openid)
    if not res:
        regis(openid)
        return get_return('注册成功')
    return get_return('已注册')


if __name__ == '__main__':
    # a = get_verify_code(1327960105)
    # print(a)
    # a = is_wx_regis('123')
    regis('12345')
    pass
