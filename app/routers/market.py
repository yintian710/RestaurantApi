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
    result = update_market_for_restaurant_id(data)
    return result


@market.post('/GetMarketForSearch')
async def get_market_for_search_(data: SearchData):
    result = get_market_for_search(data)
    return result


@market.post('/UpdateRestaurantFroMarketId')
async def update_restaurant_for_market_id_(data: OneData):
    result = update_restaurant_for_market_id(data)
    return result


if __name__ == '__main__':
    pass
