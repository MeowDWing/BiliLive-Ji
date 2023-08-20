import asyncio
import iosetting as ios
import time

"""
受保护的字符串：
__test
0x*
#*


> *代表任意16进制字符串
"""


class DrawFunc:

    def __init__(self):
        self.DRAW_SET = set()
        self.len = len(self.DRAW_SET)
        self.on_time = 0
        self.close_time = 0

    def __str__(self):
        return self.len

    def __del__(self):
        del self.DRAW_SET
        del self.len

    def initial(self):
        pass

    def on(self):  # 监听开启
        now = time.time()
        self.on_time = now

    def close(self):  # 监听关闭
        now = time.time()
        self.close_time = now

    def read(self):
        pass

    async def com_pipe(self, participate_name: str = '__test'):  # 进程通信
        pass

    def add_aud(self, participate_name: str):
        self.DRAW_SET.add(participate_name)
        self.len = len(self.DRAW_SET)

    def manifest_get(self):
        return self.DRAW_SET

    def manifest_print_debug(self):
        print(self.DRAW_SET)

    def manifest(self):
        ios.print_set('-----------------------------------------')
        tmp = 0
        for name in self.DRAW_SET:
            ios.print_set(name, end='\t')
            tmp += 1
            if tmp % 4 == 0:
                print()

    def draw(self):
        get = self.DRAW_SET.pop()
        self.len = len(self.DRAW_SET)
        return get

    def shuffle(self):
        shuffle_set = set()
        shuffle_set.update(self.DRAW_SET)
        self.DRAW_SET.clear()
        self.DRAW_SET = shuffle_set
        del shuffle_set

    def clear(self):
        self.DRAW_SET.clear()
