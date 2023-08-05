# import bilibili_api as bapi
import os

import bilibili_api
from bilibili_api import live, sync, user, exceptions
import datetime


# Exception Zone
class UserInfoError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class LiveInfoGet:
    def __init__(self, user_id: int = -1, room_id: int = -1,  # id zone
                 up_name: str = '资深小狐狸', crtl_name: str = '吾名喵喵之翼',  # str zone
                 reply_flag: bool = False):   # flag zone
        """
        you can Enter any of these parameter or not all of them
        :param user_id: get in homepage(e.g. https://space.bilibili.com/3117538/ is 3117538)
        :param room_id: live room id which is got in live homepage(e.g. https://live.bilibili.com/34162 is 34162)
        """
        # parameter initial zone
        self.room_id = room_id
        self.user_id = user_id
        self.up_name = up_name
        self.ctrl_name = crtl_name

        self.SESSDATA = -1
        self.bili_jct = -1
        self.buvid3 = -1
        self.dedeuserid = -1

        self.reply_flag = reply_flag

        # dictionary & list initial zone
        #   badge_dict
        self.badge_dict = {0: 'Passer'}
        self.badge_dict.update({
            lvl: 'Fans' for lvl in range(1,21)
        })
        self.badge_dict.update({
            lvl: 'Captain' for lvl in range(21,50)
        })
        #   general_list
        # tmp zone
        self.dot_tmp = 0

        if self.user_id > 0:
            self.user_detail = user.User(uid=self.user_id)
            self.user_info = sync(self.user_detail.get_live_info())
            self.room_id = self.user_info['live_room']['roomid']
        if self.room_id > 0:
            self.room_id = room_id
            self.room = live.LiveRoom(room_display_id=self.room_id)
            self.room_info = sync(self.room.get_room_info())
            self.user_id = self.room_info['room_info']['uid']
            self.fans_badge = self.room_info['anchor_info']['medal_info']['medal_name']
        else:
            raise UserInfoError("User_id maybe wrong, please check again")

        # environment param. initial zone
        if self.reply_flag is True:
            address_file = open(r'.\address.txt', mode='r')
            address_file = address_file.readlines()
            address = address_file[0].strip()
            # address.txt
            # the address of environments parameters
            # bililive.param
            # SESSDATA=xxxx
            # bili_jct=xxxx
            # 如果只使用自动回复功能，只配置这两个即可
            # 详细用法见README.MD
            param_file = open(address, mode='r')
            file_lines = param_file.readlines()
            print(file_lines)
            lines_len = len(file_lines)
            for i in range(lines_len):
                file_line = file_lines[i].strip().split('=')
                print(file_line)
                match file_line[0]:
                    case 'SESSDATA': self.SESSDATA = file_line[1]
                    case 'bili_jct': self.bili_jct = file_line[1]
                    case 'buvid3': self.buvid3 = file_line[1]
                    case 'dedeuserid': self.dedeuserid = file_line[1]
                    case _: print('Undefined parameter(s)')
            self.credential = bilibili_api.Credential(sessdata=self.SESSDATA, bili_jct=self.bili_jct)
            self.sender = live.LiveRoom(self.room_id, credential=self.credential)
        else:
            pass

    def live_danmaku(self):
        self.room = live.LiveDanmaku(self.room_id)

        @self.room.on('DANMU_MSG')
        async def on_danmaku(event):  # event -> dictionary
            # initial Zone
            user_fans_lvl = 0
            user_title = 'Passer'

            # main information processing Zone
            live_info = event['data']['info']  # list[Unknown, Msg, user_info, fans_info, Unknown:]
            danmaku_content = live_info[1]
            user_main_info = live_info[2]  # list[space_id, Nickname, Unknown:]
            nickname = user_main_info[1]

            if nickname == self.ctrl_name or nickname == self.up_name:
                match danmaku_content:
                    case 'general choice' | 'gc' | '1':
                        pass
                    case _:
                        pass

            if danmaku_content == '。':
                self.dot_tmp += 1
                print(f"【!】dot now is: {self.dot_tmp}")
                if self.dot_tmp > 40:
                    self.dot_tmp = 0
                    print("dot reset")
                    await self.auto_reply('。')
                    print("successful reply")

            user_fans_info = live_info[3]  # list[lvl, worn_badge, Unknown:]
            if len(user_fans_info) != 0:
                if user_fans_info[1] == self.fans_badge:
                    user_fans_lvl = user_fans_info[0]
                    user_title = self.badge_dict[user_fans_lvl]
            # timestamp processing Zone
            send_timestamp = event['data']['send_time']/1000
            trans_time = self.timestamp_to_Beijing_time(send_timestamp)

            # print_content:
            #       [timestamp][lvl:badge]Nickname:Says
            print(f'[{trans_time}][{user_fans_lvl}:{user_title}]{nickname}:{danmaku_content}')

        @self.room.on('SEND_GIFT')
        async def on_gift(event):
            # 收到礼物
            pass

        sync(self.room.connect())

    def timestamp_to_Beijing_time(self, timestamp):

        utc_time = datetime.datetime.utcfromtimestamp(timestamp)

        beijing_timezone = datetime.timezone(datetime.timedelta(hours=16))  # 为啥这要是16时间才对呀，没搞懂
        beijing_time = utc_time.astimezone(beijing_timezone)

        formatted_time = beijing_time.strftime("%H:%M:%S")
        return formatted_time

    # def general_choice(self):
    #
    #     @self.room.on('DANMU_MSG')
    #     async def msg_get(event):

    async def auto_reply(self, msg: str):
        try:
            await self.sender.send_danmaku(bilibili_api.Danmaku(msg))
        except exceptions.ResponseCodeException:
            print('弹幕发送过快错误')
        finally:
            print('auto_reply 结束')



