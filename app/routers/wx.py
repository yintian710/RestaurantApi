#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-07-30
@file: wx.py
@Desc
"""
from fastapi import APIRouter

from Data.RegisData import isWxRegisData
from component.wx import get_login_openid, is_wx_regis

wx = APIRouter(
    prefix="/wx",
    tags=["wx"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@wx.post('/getOpenId')
async def get_open_id_(params: dict):
    """
    获取用户openid
    :param params:
    :return:
    """
    result = await get_login_openid(params)
    return result


@wx.post('/isWxRegis')
async def is_wx_regis_(data: isWxRegisData):
    """
    验证用户是否登录,未注册则自动注册,传入用户openid
    :param data:
    :return:
    """
    result = is_wx_regis(data.user_id)
    return result


if __name__ == '__main__':
    pass
