# import bilibili_api
from bilibili_api import live, sync, user
import asyncio

def main():
    user_id = 3117538
    user_info = user.User(user_id)
    x = sync(user_info.get_live_info())
    # print(sync(user_info.get_user_medal()))
    y = x['live_room']['roomid']
    z = x['fans_badge']
    print(x)
    print(y)
    print(z)


if __name__ == '__main__':
    main()
