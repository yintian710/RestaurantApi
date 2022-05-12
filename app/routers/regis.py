#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-07-30
@file: regis.py
@Desc
"""
from fastapi import APIRouter

from Data.RegisData import isWxRegisData
from component.regis import get_login_openid, is_wx_regis

regis = APIRouter(
    prefix="/wx",
    tags=["wx"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@regis.post('/getOpenId')
async def _(params: dict):
    result = await get_login_openid(params)
    return result


@regis.post('/isWxRegis')
async def _(data: isWxRegisData):
    result = is_wx_regis(data.user_id)
    return result


if __name__ == '__main__':
    pass
