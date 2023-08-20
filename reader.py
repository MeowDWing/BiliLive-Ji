import os

import pygame

import live_function.audioplay as player
import time
from collections import deque

class Reader:

    def __init__(self):
        self.danmaku_queue = deque()
        self.danmaku_len = 0
        player.initial()

    def reader(self):
        print('[read]wait initial')
        time.sleep(1)
        while True:
            with open('./files/danmaku.txt', mode='r', encoding='utf-8') as f:
                lines = f.readlines()
            with open('./files/danmaku.txt', mode='w', encoding='utf-8'):
                pass
            if len(lines) != 0:
                for line in lines:
                    line = line.strip()
                    self.danmaku_queue.append(line)
                    self.danmaku_len += 1
                    print(self.danmaku_queue)
            if self.danmaku_len != 0:
                now = self.danmaku_queue.popleft()
                print(now)
                self.danmaku_len -= 1
                try:
                    player.play('./audio/'+now+'.mp3')
                except pygame.error:
                    print('bad stream')
                player.delete('./audio/'+now+'.mp3')
            else:
                time.sleep(3)


def main():
    read = Reader()
    read.reader()

if __name__ == '__main__':
    main()