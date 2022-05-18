from Data.userData import UserData
from component.common import get_user_history, get_user_history_for_ten
from tool.common import is_regis, get_return


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
    pass
