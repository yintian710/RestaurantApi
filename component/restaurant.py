# -*- coding: utf-8 -*-
"""
@File  : restaurant_.py
@Author: yintian
@Date  : 2021/6/11 23:43
@Desc  : 
"""
import json
import random
import time

from Data.RestaurantData import NewFoodsData, NewFoodData, OneData, RestaurantNameData, NewRestaurantData
from Data.userData import UserData
from sql import employ
from tool.CONTANT import SQL_DICT, NEXT_WEIGHT, GO_WEIGHT

from tool.common import is_regis, get_return, get_random_value_dict_for_dict_weight


def get_user_this(user_id):
    res = employ.select_user_info(user_id, 'this')
    return res[0]


def change_user_this(user_id, this):
    employ.update_user_info(user_id, this=this)


def change_food_weight(user_id, food, weight):
    food_id = food['id']
    weight = food['weight'] + weight
    employ.update_food(user_id, food_id, weight=weight)


def get_go(user_id):
    res = employ.select_user_info(user_id, 'go')
    return res[0]


def change_go(user_id, go):
    employ.update_user_info(user_id, go=go)


def get_user_history(user_id):
    res = employ.select_history(user_id, '*')
    if not res:
        return []
    res.sort(key=lambda x: x['last_time'], reverse=True)
    return res


def get_user_history_for_ten(user_id):
    return get_user_history(user_id)[:10]


def save_history(user_id, restaurant_id, food, food_id):
    employ.insert_history(user_id, restaurant_id, food, food_id)


def get_foods_for_restaurant_id(restaurant_id):
    res = employ.select_restaurant_foods(restaurant_id, '*', active=True)
    return res


def get_foods_for_user_id(restaurant_id):
    res = employ.select_user_foods(restaurant_id, '*', active=True)
    return res


def get_food_for_id(food_id):
    res = employ.select_food(food_id, '*')
    if not res:
        return None
    return res


def get_user_restaurant_for_restaurant_id(user_id, restaurant_id):
    res = employ.select_restaurant(user_id, '*', restaurant_id=restaurant_id)
    if not res:
        return res
    result = res[0]
    result['foods'] = get_foods_for_restaurant_id(restaurant_id)
    return result


def get_user_all_restaurants(user_id):
    """
    获取所有数据
    :param user_id:
    :return:
    """
    res = employ.select_restaurant(user_id, '*')
    for _ in res:
        _['foods'] = get_foods_for_restaurant_id(_['id'])
    return res


def get_user_all_restaurant_id(user_id):
    res = employ.select_restaurant(user_id, 'id')
    if res:
        res = [_[0] for _ in res]
    return res


def change_user_restaurant_name(user_id, restaurant_id, name):
    employ.update_restaurant(user_id, restaurant_id, name=name)


def get_random_food_id(foods: list, ignore=None) -> str:
    """
    获取随机产生的食物
    :param foods: 食府中的食物数据
    :param ignore: 需要被忽略的一个食物，往往是已经去了两次的
    :return:
    """
    food = foods.copy()
    random_dict = get_random_value_dict_for_dict_weight(food, value='id', weight='weight', ignore=ignore)
    random_food = random.choices(random_dict['value'], weights=random_dict['weight'])
    return random_food[0]


@is_regis
def new_restaurant(data: NewRestaurantData):
    """
    新建食府
    :param data:
    :return:
    """
    user_id, name = data.user_id, data.name
    restaurant_id = employ.insert_restaurant(user_id, name)
    employ.update_user_info(user_id, this=restaurant_id)
    result = get_return(f'新建食府{name}成功，食府id为：{restaurant_id}，当前选择食府已自动更换',
                        need={'restaurant_id': restaurant_id})
    return result


@is_regis
def new_foods(data: NewFoodsData):
    user_id = data.user_id
    food_list = data.food_list
    restaurant_id = data.restaurant_id
    if restaurant_id == 0:
        restaurant_id = get_user_this(user_id)
    restaurant = get_user_restaurant_for_restaurant_id(user_id, restaurant_id)
    if not restaurant:
        return get_return(f'请输入正确的食府id', code=1)
    food_id_list = [employ.insert_food(user_id, _.name, restaurant_id, _.address) for _ in food_list]
    return get_return(f'添加食物成功！', need={'food_id_list': food_id_list})


@is_regis
def get_one_restaurant(data: OneData):
    user_id, restaurant_id = data.user_id, data.id
    if not restaurant_id:
        restaurant_id = get_user_this(user_id)
    res = get_user_restaurant_for_restaurant_id(user_id, restaurant_id)
    if not res:
        return get_return(f'用户无默认食府或传入食府id错误', code=1)
    return get_return(f'获取食府：{res["name"]}成功', need={'data': res})


@is_regis
def get_all_restaurants(data: UserData):
    res = get_user_all_restaurants(data.user_id)
    if not res:
        return get_return(f'获取失败', code=1)
    return get_return(f'获取成功', need={'data': res})


@is_regis
def change_this(data: OneData):
    if data.id not in get_user_all_restaurant_id(data.user_id):
        return get_return(f'请确认输入食府id是否正确', code=1)
    change_user_this(data.user_id, data.id)
    if data.id != get_user_this(user_id=data.user_id):
        return get_return(f'更改当前食府出错', code=1)
    return get_return(f'更改食府成功!')


@is_regis
def get_this(data: UserData):
    this = get_user_this(data.user_id)
    return get_return(f'获取用户当前选定食府id成功！', this=this)


@is_regis
def change_restaurant_name(data: RestaurantNameData):
    this = data.id if data.id else get_user_this(data.user_id)
    change_user_restaurant_name(data.user_id, this, data.name)
    if data.name != get_user_restaurant_for_restaurant_id(data.user_id, this)['name']:
        return get_return(f'更改食府名出错', code=1)
    return get_return(f'更改食府名成功!')


@is_regis
def next_food(data: UserData):
    user_id = data.user_id
    this = get_user_this(user_id)
    go = get_go(user_id)
    user_foods = get_foods_for_user_id(user_id)
    foods = get_foods_for_restaurant_id(this)
    now = time.time()
    history = get_user_history_for_ten(user_id)
    if len(foods) < 2:
        return get_return(f'请确保食府中食物数量大于2', code=1)
    if go:
        food = next(filter(lambda x: x['id'] == go, user_foods))
        change_food_weight(user_id, food, NEXT_WEIGHT)
    if len(history) > 2 and \
            history[0]['food'] == history[1]['food'] == go and \
            history[0]['last_time'] - history[1]['last_time'] < 24 * 60 * 60 and \
            now - history[0]['last_time'] < 24 * 60 * 60:
        ignore = go
    else:
        ignore = None
    food_id = get_random_food_id(foods, ignore)
    change_go(user_id, food_id)
    food = next(filter(lambda x: x['id'] == food_id, foods))
    food_name = food['name']
    return get_return(f'当前食物为：{food_name}', food=food)


@is_regis
def go_food(data: UserData):
    user_id = data.user_id
    this = get_user_this(user_id)
    go = get_go(user_id)
    if not go:
        return get_return(f'还没有选择的食物，请先摇一下~')
    food = get_food_for_id(go)
    change_food_weight(user_id, food, GO_WEIGHT)
    food_name = food['name']
    change_go(user_id, 0)
    save_history(user_id, this, food_name, go)
    return get_return(f'你选择了{food_name}， 冲鸭！', food=food)


@is_regis
def get_history(data: UserData):
    user_id = data.user_id
    history = get_user_history(user_id)
    return get_return(f'获取成功', history=history)


@is_regis
def get_ten_history(data: UserData):
    user_id = data.user_id
    history = get_user_history_for_ten(user_id)
    return get_return(f'获取成功', history=history)


if __name__ == '__main__':
    res_ = get_user_all_restaurant_id('string')
    # res_ = next_food(UserData(user_id='string'))
    # res_ = change_this(OneData(user_id='string', id=11))
    print(res_)
