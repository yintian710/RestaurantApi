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

from Data.RestaurantData import NewFoodsData, OneData, RestaurantNameData, NewRestaurantData
from Data.userData import UserData
from component.common import get_user_this, get_user_restaurant_for_restaurant_id, get_user_all_restaurants, \
    get_user_all_restaurant_id, change_user_this, change_user_restaurant_name, get_go, get_foods_for_user_id, \
    get_foods_for_restaurant_id, get_user_history_for_ten, change_food_weight, get_random_food_id, change_go, \
    get_food_for_id, save_history
from sql import employ
from tool.CONTANT import NEXT_WEIGHT, GO_WEIGHT

from tool.common import is_regis, get_return


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


if __name__ == '__main__':
    res_ = get_user_all_restaurant_id('string')
    # res_ = next_food(UserData(user_id='string'))
    # res_ = change_this(OneData(user_id='string', id=11))
    # update_market_for_restaurant_id(NewMarketData(user_id='string', id=11, name=''))
    print(res_)
