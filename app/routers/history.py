from fastapi import APIRouter

from Data.userData import UserData
from component.history import get_history, get_ten_history

history = APIRouter(
    prefix="/history",
    tags=["history"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@history.post('/getHistory')
async def get_history_(data: UserData):
    result = get_history(data)
    return result


@history.post('/getTenHistory')
async def get_ten_history_(data: UserData):
    result = get_ten_history(data)
    return result


if __name__ == '__main__':
    pass
