from random import choices

from sql import employ
from tool.common import get_random_value_dict_for_dict_weight


def get_market(search_key):
    res = employ.select_market('*', like=search_key)
    for _ in res:
        split = _['foods'].split('|')
        foods = [{'food': __.split('-')[0], 'address': __.split('-')[1]} for __ in split]
        _['foods'] = foods
    return res


def get_market_for_id(market_id):
    res = employ.select_market('*', id=market_id)
    if not res:
        return res
    res = res[0]
    split = res['foods'].split('|')
    foods = [{'food': __.split('-')[0], 'address': __.split('-')[1]} for __ in split]
    res['foods'] = foods
    return res


def add_market_for_foods(user_id, name, foods):
    market_id = employ.insert_market(user_id, name, foods)
    return market_id


def add_restaurant_for_market_id(user_id, market_id):
    market_data = get_market_for_id(market_id)
    if not market_data:
        return market_data
    name = market_data['name']
    foods = market_data['foods']
    restaurant_id = employ.insert_restaurant(user_id, name)
    food_id_list = [employ.insert_food(user_id, _['food'], restaurant_id, _['address']) for _ in foods]
    return restaurant_id, food_id_list


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
    random_food = choices(random_dict['value'], weights=random_dict['weight'])
    return random_food[0]


if __name__ == '__main__':
    res_ = get_market_for_id(17)
    print(res_)
