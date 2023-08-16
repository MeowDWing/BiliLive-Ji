import asyncio
import iosetting as ios


class DrawFunc:

    def __init__(self):
        self.DRAW_SET = set()
        self.len = len(self.DRAW_SET)

    def __str__(self):
        return self.len

    def __del__(self):
        del self.DRAW_SET
        del self.len

    def initial(self):
        pass

    async def open(self, participate_name: str):
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
