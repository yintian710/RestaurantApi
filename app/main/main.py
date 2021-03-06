#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-07-26
@file: main.py
@Desc
"""
import os
import sys
from logging import INFO

import uvicorn as uvicorn
from fastapi import FastAPI

path = os.getcwd()
work_path = path.split('/main')[0]
sys.path.append(work_path)
sys.path.append(work_path + '/main')

from app.routers.wx import wx
from app.routers.restaurant import restaurants
from app.routers.history import history
from app.routers.market import market

app = FastAPI(docs_url='/yintian')
app.include_router(restaurants)
app.include_router(wx)
app.include_router(history)
app.include_router(market)


@app.get("/")
async def root(): return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=4399, log_level=INFO, )
