#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-07-26
@file: restaurant_.py
@Desc
"""
from fastapi import APIRouter

from Data.RestaurantData import NewRestaurantData, NewFoodsData, OneData, RestaurantNameData
from Data.userData import UserData
from component.restaurant import new_restaurant, get_one_restaurant, \
    get_all_restaurants, new_foods, change_this, change_restaurant_name, get_this, next_food, go_food
restaurants = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@restaurants.post('/newRestaurant')
async def new_restaurant_(data: NewRestaurantData):
    """
    新建食府,传入新食府名及用户openid
    :param data:
    :return:
    """
    result = new_restaurant(data)
    return result


@restaurants.post('/newFoods')
async def new_foods_(data: NewFoodsData):
    """
    给食府添加食物,传入openid,restaurant_id,food_list：{name：food_name，address：food_address，address可为空}
    :param data:
    :return:
    """
    result = new_foods(data)
    return result


@restaurants.post('/getOneRestaurant')
async def get_one_restaurant_(data: OneData):
    """
    获取用户单个食府,传入restaurant_id,openid,传入restaurant_id为0则自动获取用户当前选择食府数据
    :param data:
    :return:
    """
    result = get_one_restaurant(data)
    return result


@restaurants.post('/all')
async def all_(data: UserData):
    """
    获取用户所有食府数据,传入用户openid
    :param data:
    :return:
    """
    result = get_all_restaurants(data)
    return result


@restaurants.post('/changeThis')
async def change_this_(data: OneData):
    """
    更改用户当前选择食府,传入用户open_id,新的食府restaurant_id
    :param data:
    :return:
    """
    result = change_this(data)
    return result


@restaurants.post('/this')
async def this_(data: UserData):
    """
    获取当前用户选择食府id,传入用户openid
    :param data:
    :return:
    """
    result = get_this(data)
    return result


@restaurants.post('/changeRestaurantName')
async def change_restaurant_name_(data: RestaurantNameData):
    """
    更改食府名,传入restaurant_id, openid, name, restaurant_id可不传,默认为用户当前选择食府
    :param data:
    :return:
    """
    result = change_restaurant_name(data)
    return result


@restaurants.post('/next')
async def next_(data: UserData):
    """
    获取下一个推荐食物,传入用户openid
    :param data:
    :return:
    """
    result = next_food(data)
    return result


@restaurants.post('/go')
async def go_(data: UserData):
    """
    选定当前食物,传入用户openid
    :param data:
    :return:
    """
    result = go_food(data)
    return result

if __name__ == '__main__':
    pass
