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
    get_all_restaurants, new_foods, change_this, change_restaurant_name, get_this, next_food, go_food, get_history, \
    get_ten_history

restaurants = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@restaurants.post('/newRestaurant')
async def new_restaurant_(data: NewRestaurantData):
    result = new_restaurant(data)
    return result


@restaurants.post('/newFoods')
async def new_foods_(data: NewFoodsData):
    result = new_foods(data)
    return result


@restaurants.post('/getOneRestaurant')
async def get_one_restaurant_(data: OneData):
    result = get_one_restaurant(data)
    return result


@restaurants.post('/all')
async def all_(data: UserData):
    result = get_all_restaurants(data)
    return result


@restaurants.post('/changeThis')
async def change_this_(data: OneData):
    result = change_this(data)
    return result


@restaurants.post('/this')
async def this_(data: UserData):
    result = get_this(data)
    return result


@restaurants.post('/changeRestaurantName')
async def change_restaurant_name_(data: RestaurantNameData):
    result = change_restaurant_name(data)
    return result


@restaurants.post('/next')
async def next_(data: UserData):
    result = next_food(data)
    return result


@restaurants.post('/go')
async def go_(data: UserData):
    result = go_food(data)
    return result


@restaurants.post('/getHistory')
async def get_history_(data: UserData):
    result = get_history(data)
    return result


@restaurants.post('/getTenHistory')
async def get_ten_history_(data: UserData):
    result = get_ten_history(data)
    return result


if __name__ == '__main__':
    pass
