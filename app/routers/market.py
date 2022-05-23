from fastapi import APIRouter

from Data.RestaurantData import NewMarketData, SearchData, OneData
from component.market import update_market_for_restaurant_id, get_market_for_search, update_restaurant_for_market_id

market = APIRouter(
    prefix="/market",
    tags=["market"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@market.post('/AddMarketForRestaurantId')
async def add_market_for_restaurant_id_(data: NewMarketData):
    """
    通过restaurant_id将食府数据添加到食府市场,传入user_id=openid,id=restaurant_id,name为食府市场食府名,可不传,默认用户食府名
    :param data:
    :return:
    """
    result = update_market_for_restaurant_id(data)
    return result


@market.post('/GetMarketForSearch')
async def get_market_for_search_(data: SearchData):
    """
    查询食府市场食府,传入查询关键词,可不传,默认返回全部
    :param data:
    :return:
    """
    result = get_market_for_search(data)
    return result


@market.post('/UpdateRestaurantFroMarketId')
async def update_restaurant_for_market_id_(data: OneData):
    """
    通过market_id添加食府及食物,传入id=market_id,user_id=openid
    :param data:
    :return:
    """
    result = update_restaurant_for_market_id(data)
    return result


if __name__ == '__main__':
    pass
