# import bilibili_api
from bilibili_api import live, sync, user
import asyncio
import liveget as lg
import multiprocessing as mp


class SubProcess(mp.Process):
    def __init__(self, name):
        super(SubProcess, self).__init__()
        self.name = name

    def run(self) -> None:
        print(f"This is subprocess {self.name}")


class SubGetDanmaku(mp.Process):
    def __init__(self, name, room_id=-1, uid=-1):
        super(SubGetDanmaku, self).__init__()
        self.name = name
        self.room_id = room_id
        self.uid = uid

    def run(self) -> None:
        get_room = lg.LiveInfoGet(room_id=self.room_id, user_id=self.uid)
        get_room.live_danmaku()




if __name__ == '__main__':
    print("-----subprocess_init.py-----")
