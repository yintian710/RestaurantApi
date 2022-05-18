from Data.RestaurantData import NewMarketData, SearchData, OneData
from component.common import add_market_for_foods, get_market, add_restaurant_for_market_id
from sql import employ
from tool.common import is_regis, get_return


@is_regis
def update_market_for_restaurant_id(data: NewMarketData):
    restaurant_id = data.id
    user_id = data.user_id
    res1 = employ.select_restaurant(user_id, 'name', restaurant_id=restaurant_id)
    res2 = employ.select_restaurant_foods(restaurant_id, 'name', 'address')
    if not res1 or not res2:
        return get_return(f'您提交的食府错误或没有食物')
    name = data.name or res1[0][0]
    foods = '|'.join(['-'.join(_).replace('|', '') for _ in res2])
    market_id = add_market_for_foods(user_id, name, foods)
    return get_return(f'食府{name}添加到食府市场成功', market_id=market_id)


@is_regis
def get_market_for_search(data: SearchData):
    search_key = data.key
    res = get_market(search_key)
    if not res:
        return get_return(f'没有找到对应条件的食府', code=1)
    return get_return(f'查询成功', market=res)


@is_regis
def update_restaurant_for_market_id(data: OneData):
    user_id = data.user_id
    market_id = data.id
    res = add_restaurant_for_market_id(user_id, market_id)
    if not res:
        return get_return(f'添加失败', code=1)
    restaurant_id, foods = res
    return get_return(f'添加成功', restaurant_id=restaurant_id, foods=foods)


if __name__ == '__main__':
    pass
