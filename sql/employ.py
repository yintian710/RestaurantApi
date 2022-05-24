#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-07-26
@file: employ.py
@Desc
"""
from re import findall
from time import time

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.dependencies import get_db
from sql.model import Food, Restaurant, History, Market
from tool.CONTANT import SQL_DICT
from tool.Error import SqlColumnError


def select_market(*args, **kwargs):
    like = kwargs.get('like', {})
    active = kwargs.get('active', None)
    _id = kwargs.get('id', None)
    db = get_db()
    base = Market
    res = db.query(base)
    if active:
        res = res.filter(base.active == active)
    if _id:
        res = res.filter(base.id == _id)
    if like:
        res = res.filter(base.name.like(f'%{like}%'))
    if not res:
        return None
    result = [_.get(*args) for _ in res]
    db.close()
    return result


def insert_market(user_id, name, foods, **kwargs):
    kwargs['user_id'] = user_id
    kwargs['name'] = name
    kwargs['foods'] = foods
    kwargs.setdefault('active', False)
    kwargs.setdefault('last_time', time())
    market_id = insert_base_id('market', **kwargs)
    return market_id


def update_market(market_id, **kwargs):
    kwargs['last_time'] = time()
    update_base_id('market', market_id, **kwargs)


# def select_market(market_id, **kwargs):
#     res = select_base_id('market', market_id, '*', **kwargs)
#     return res


def select_history(user_id, *args):
    """
    查询"history"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    db = get_db()
    base = History
    res = db.query(base).filter(base.user_id == user_id)
    if not res:
        return None
    result = [_.get(*args) for _ in res]
    db.close()
    return result


def insert_history(user_id, restaurant_id, food, food_id):
    """
    注册u表
    :param food_id:
    :param food:
    :param restaurant_id:
    :param user_id:
    :return:
    """
    db = get_db()
    base = History()
    base.user_id = user_id
    base.restaurant_id = restaurant_id
    base.last_time = int(time())
    base.food = food
    base.food_id = food_id
    db.add(base)
    db.commit()


def select_restaurant(user_id, *args, **kwargs):
    """
    查询"restaurant"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    db = get_db()
    base = Restaurant
    res = db.query(base).filter(base.user_id == user_id)
    if 'restaurant_id' in kwargs:
        res = res.filter(base.id == kwargs['restaurant_id'])
    if 'active' in kwargs:
        res = res.filter(base.active == kwargs['active'])
    if not res:
        return None
    result = [_.get(*args) for _ in res]
    db.close()
    return result


def update_restaurant(user_id, restaurant_id, **kwargs):
    """
    更新"restaurant"表中的数据,调用update_base接口
    :param restaurant_id:
    :param user_id:
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    db = get_db()
    base = Restaurant
    kwargs['last_time'] = time()
    db.query(base).filter(base.id == restaurant_id).filter(base.user_id == user_id).update(kwargs)
    db.commit()
    db.close()


def insert_restaurant(user_id, restaurant_name, **kwargs):
    """
    注册eat表
    :param restaurant_name:
    :param user_id:
    :return:
    """
    db = get_db()
    base = Restaurant(**kwargs)
    base.user_id = user_id
    base.name = restaurant_name
    base.last_time = int(time())
    base.active = True
    db.add(base)
    db.commit()
    return base.id


def select_restaurant_foods(restaurant_id, *args, **kwargs):
    """
    查询"food"表中的数据,调用select_base接口
    :param restaurant_id:
    :param args: 所有被查询的字段名
    :return:
    """
    db = get_db()
    base = Food
    res = db.query(base).filter(base.restaurant_id == restaurant_id)
    if 'active' in kwargs:
        res = res.filter(base.active == kwargs['active'])
    if not res:
        return None
    result = [_.get(*args) for _ in res]
    db.close()
    return result


def select_user_foods(user_id, *args, **kwargs):
    """
    查询"food"表中的数据,调用select_base接口
    :param user_id:
    :param args: 所有被查询的字段名
    :return:
    """
    db = get_db()
    base = Food
    res = db.query(base).filter(base.user_id == user_id)
    if 'active' in kwargs:
        res = res.filter(base.active == kwargs['active'])
    if not res:
        return None
    result = [_.get(*args) for _ in res]
    db.close()
    return result


def select_wx(user_id, *args):
    """
    查询"wx"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    return select_base('wx', user_id, *args)


def update_wx(user_id, kwargs):
    """
    更新"wx"表中的数据,调用update_base接口
    :param user_id:
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    update_base('wx', user_id, **kwargs)


def insert_wx(user_id):
    """
    注册wx表
    :param user_id:
    :return:
    """
    insert_base('wx', user_id)


def select_user_info(user_id, *args):
    """
    查询"user_info"表中的数据,调用select_base接口
    :param user_id: 被查询的用户id
    :param args: 所有被查询的字段名
    :return:
    """
    return select_base('user_info', user_id, *args)


def update_user_info(user_id, **kwargs):
    """
    更新"user_info"表中的数据,调用update_base接口
    :param user_id:
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    kwargs['last_time'] = time()
    update_base('user_info', user_id, **kwargs)


def insert_user_info(user_id):
    """
    插入游戏用户信息
    :param user_id:
    :return:
    """
    insert_base('user_info', user_id)


def select_food(food_id, *args):
    """
    查询"food"表中的数据,调用select_base接口
    :param food_id:
    :param args: 所有被查询的字段名
    :return:
    """
    db = get_db()
    base = Food
    res = db.query(base).filter(base.id == food_id).first()
    if not res:
        return None
    result = res.get(*args)
    db.close()
    return result


def update_food(user_id, food_id, **kwargs):
    """
    更新"food"表中的数据,调用update_base接口
    :param food_id:
    :param user_id:
    :param kwargs: 需要更改的数据dict,{需要更改的字段名:更改之后的值,...}
    :return:
    """
    kwargs['last_time'] = time()
    # update_base_id('food', food_id, **kwargs)
    db = get_db()
    base = Food
    db.query(base).filter(base.id == food_id).filter(base.user_id == user_id).update(kwargs)
    db.commit()
    db.close()


def insert_food(user_id, food, restaurant_id, address=''):
    """
    注册food表信息
    :param restaurant_id:
    :param address:
    :param food:
    :param user_id:
    :return:
    """
    db = get_db()
    base = Food()
    base.user_id = user_id
    base.name = food
    base.restaurant_id = restaurant_id
    base.address = address
    base.weight = 100
    base.last_time = int(time())
    base.active = True
    db.add(base)
    db.commit()
    base_id = base.id
    db.close()
    return base_id


def select_id_in_wx(openid):
    """
    查询"wx"表中的数据,调用select_base接口, 不以user_id为查询
    :return:
    """
    db = get_db()
    base = SQL_DICT['wx']
    result = db.query(base.user_id).filter(base.user_id == openid).all()
    db.close()
    return result


def insert_base(base_name: str, user_id: int, **kwargs):
    db = get_db()
    base = SQL_DICT[base_name]()
    base.set(**kwargs)
    base.user_id = user_id
    db.add(base)
    db.commit()
    db.close()


def select_base(base_name: str, user_id: int, *args):
    db = get_db()
    base = SQL_DICT[base_name]
    result = db.query(base).filter(base.user_id == user_id)
    if not result:
        return None
    result = [_.get(*args) for _ in result]
    if not result:
        return None
    db.close()
    return result[0]


def update_base(base_name: str, user_id: int, **kwargs):
    db = get_db()
    base = SQL_DICT[base_name]
    db.query(base).filter(base.user_id == user_id).update(kwargs)
    db.commit()
    db.close()


def delete_base(base_name: str, user_id: int):
    db = get_db()
    base = SQL_DICT[base_name]
    db.query(base).filter(base.user_id == user_id).delete()
    db.commit()
    db.close()


def insert_base_id(base_name: str, **kwargs):
    db = get_db()
    base = SQL_DICT[base_name]()
    base.set(**kwargs)
    db.add(base)
    db.commit()
    base_id = base.id
    db.close()
    return base_id


def select_base_id(base_name: str, _id: int, *args, **kwargs):
    kwargs.get('user_id', '')
    db = get_db()
    base = SQL_DICT[base_name]
    result = db.query(base).filter(base.id == _id)
    if not result:
        return None
    result = [_.get(*args) for _ in result]
    db.close()
    if not result:
        return None
    return result[0]


def update_base_id(base_name: str, _id: int, **kwargs):
    db = get_db()
    base = SQL_DICT[base_name]
    db.query(base).filter(base.id == _id).update(kwargs)
    db.commit()
    db.close()


def delete_base_id(base_name: str, _id: int):
    db = get_db()
    base = SQL_DICT[base_name]
    db.query(base).filter(base.id == _id).delete()
    db.commit()
    db.close()


def select_base_any(base_name, *args, **kwargs):
    try:
        sql_list = []
        for k, v in kwargs.items():
            if isinstance(v, bool):
                sql_list.append(f'{k}={int(v)}')
            elif isinstance(v, int):
                sql_list.append(f'{k}={v}')
            elif isinstance(v, str):
                sql_list.append(f"{k}='{v}'")
        sql = ' and '.join(sql_list)
        print(sql)
        db = get_db()
        base = SQL_DICT[base_name]
        res = db.query(base).filter(text(sql)).all()
        if not res:
            return None
        result = [_.get(*args) for _ in res]
        db.close()
        return result
    except OperationalError as e:
        column = findall("column \'(.*?)\' ", str(e))[0]
        raise SqlColumnError(column)


if __name__ == '__main__':
    # res_ = select_base_any('food', 'name', 'id', user_id='string', active=True, name='米饭')
    res_ = select_market('*', like='1')
    print(res_)
