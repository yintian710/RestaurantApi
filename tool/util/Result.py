#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021.11.03 11:19
@file: Result.py
@Desc：
"""
from json import dumps


class Result:
    code: int = 0
    message: str = ''

    def __init__(self, code=code, message=message, need=None):
        if need is None:
            need = {}
        self.message = message
        self.code = code
        self.set_need(need)

    def bad_result(self, message='', code=1, need=None):
        if need is None:
            need = {}
        self.code = code
        self.message = message
        self.set_need(need)
        return self.__dict__

    def good_result(self, message='', code=0, need=None):
        if need is None:
            need = {}
        self.code = code
        self.message = message
        self.set_need(need)
        return self.__dict__

    def set_need(self, need: dict):
        if need:
            for k, v in need.items():
                self.__setattr__(str(k), v)

    def dict(self):
        return self.__dict__

    @staticmethod
    def good(message='', code=0, need=None):
        if need is None:
            need = {}
        return {'message': message, 'code': code, **need}

    @staticmethod
    def bad(message='', code=1, need=None):
        if need is None:
            need = {}
        return {'message': message, 'code': code, **need}

    def __str__(self):
        return dumps(self.__dict__)

    __repr__ = __str__


if __name__ == '__main__':
    pass
