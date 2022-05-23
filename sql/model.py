#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-07-26
@file: model.py
@Desc
"""

from sqlalchemy import Column, BIGINT, VARCHAR, TEXT, BOOLEAN
from sqlalchemy.orm import registry

from sql.config import Base

mapper_registry = registry()

Map = mapper_registry.generate_base()


class dBase:

    def get(self, *args):
        if '*' in args:
            attr = self.__dict__.copy()
            attr.pop('_sa_instance_state')
            return attr
        return tuple(getattr(self, _) for _ in args)

    def set(self, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)


class Wx(Base, dBase, Map):
    __tablename__ = 'wx'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(255), primary_key=True)
    # open_id = Column(VARCHAR(255), primary_key=True)
    last_time = Column(BIGINT)


class UserInfo(Base, dBase, Map):
    __tablename__ = 'user_info'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(255), primary_key=True)
    name = Column(TEXT)
    this = Column(BIGINT)
    go = Column(BIGINT)
    permission = Column(VARCHAR(255))
    last_time = Column(BIGINT)


class Restaurant(Base, dBase, Map):
    __tablename__ = 'restaurant'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(255))
    name = Column(TEXT)
    last_time = Column(BIGINT)
    active = Column(BOOLEAN)


class Food(Base, dBase, Map):
    __tablename__ = 'food'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(255))
    restaurant_id = Column(BIGINT)
    weight = Column(BIGINT)
    name = Column(TEXT)
    address = Column(TEXT)
    active = Column(BOOLEAN)
    last_time = Column(BIGINT)


class History(Base, dBase, Map):
    __tablename__ = 'history'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(255))
    restaurant_id = Column(BIGINT)
    food = Column(TEXT)
    food_id = Column(BIGINT)
    last_time = Column(BIGINT)


class Market(Base, dBase, Map):
    __tablename__ = 'market'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(255))
    foods = Column(TEXT)
    name = Column(TEXT)
    last_time = Column(BIGINT)
    active = Column(BOOLEAN)


if __name__ == '__main__':
    pass
