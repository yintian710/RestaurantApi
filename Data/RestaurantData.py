# -*- coding: utf-8 -*-
"""
@File  : RestaurantData.py
@Author: yintian
@Date  : 2021/7/30 21:51
@Desc  : 
"""
from typing import List

from pydantic import BaseModel

from Data.userData import UserData


class RestaurantData(UserData):
    new_this_num: str = ''
    new_restaurant_name: str = ''
    add_str: str = ''


class NewRestaurantData(UserData):
    name: str


class RestaurantNameData(NewRestaurantData):
    id: int


class NewFoodData(BaseModel):
    address: str = ''
    name: str


class NewFoodsData(UserData):
    restaurant_id: int
    food_list: List[NewFoodData]


class OneData(UserData):
    id: int = 0


if __name__ == '__main__':
    pass
