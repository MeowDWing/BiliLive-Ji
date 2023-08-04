# import bilibili_api
from bilibili_api import live, sync, user
import asyncio
import liveget as lg


def main():
    x = lg.LiveInfoGet(room_id=271744)
    x.live_danmaku()

    # room = live.LiveDanmaku(34162)
    #
    # @room.on('DANMU_MSG')
    # async def on_danmaku(event):  # event -> dictionary
    #     print(event)
    #
    # sync(room.connect())


if __name__ == '__main__':
    main()
