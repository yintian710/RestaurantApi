# -*- coding: utf-8 -*-
"""
@File  : CONTENT.py
@Author: yintian
@Date  : 2021/3/31 17:42
@Desc  : 各种常量
"""
import os
from sql.model import Wx, Restaurant, History, UserInfo, Food, Market

PA = '爬'

RUMOR_PRICE = 5

CARD_PRICE = 3

HOUSE_PRICE = 5

BOOM_TIME_INTERVAL = 60

BOOM_PRICE = 1

BOOM_SCORE = 5

USER_BOOM_PRICE = 70

USER_BOOM_TAX = 4

RE_PRICE = {'N': 1, 'R': 3, 'SR': 7}

PROJECT_PATH = os.getcwd()

BOT_PATH = PROJECT_PATH[:PROJECT_PATH.find('bot_http') + 8]

SQL_PATH = BOT_PATH + r'\ignore\sql.json'

SSL_KEY_PATH = BOT_PATH + r'\ignore\wx.key'

SSL_PEM_PATH = BOT_PATH + r'\ignore\wx.pem'


SQL_DICT = {
    'wx': Wx,
    'restaurant': Restaurant,
    'history': History,
    'user_info': UserInfo,
    'food': Food,
    'market': Market
}

GO_WEIGHT = 5
NEXT_WEIGHT = -2

RESTAURANT_LIST = [f'restaurant{_}' for _ in range(1, 10)]

pa = {"message": {"public": "爬", "private": ""}, "code": 1}

if __name__ == '__main__':
    print()
