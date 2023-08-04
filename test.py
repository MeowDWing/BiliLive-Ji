import bilibili_api
from bilibili_api import live, sync
import liveget as lg

class Main:
    def __init__(self):
        self.i = 0
        self.flag = 0
        self.gdict = {}

    def main(self):
        room = live.LiveDanmaku(34162)

        @room.on('DANMU_MSG')
        async def on_danmaku(event):

            getttt = event['data']['info']
            gettt = getttt[1]
            match gettt:
                case '-1':
                    self.flag = 0
                    self.i=0
                    self.gdict={}
                case '-2':
                    self.flag = 1
            name = getttt[2][1]
            print(getttt, name)
            if self.flag == 1:
                if gettt == '。':
                    self.gdict.update({name: self.i})
                    self.i += 1


        @room.on('DANMU_MSG')
        async def on_general(event):
            print('-----------')

        sync(room.connect())

if __name__ == '__main__':
    x = Main()
    x.main()
