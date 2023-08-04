# import bilibili_api as bapi
from bilibili_api import live, sync, user
import datetime


# Exception Zone
class UserInfoError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class LiveInfoGet:
    def __init__(self, user_id: int = -1, room_id: int = -1):
        """
        you can Enter any of these parameter or not all of them
        :param user_id: get in homepage(e.g. https://space.bilibili.com/3117538/ is 3117538)
        :param room_id: live room id which is got in live homepage(e.g. https://live.bilibili.com/34162 is 34162)
        """
        self.room_id = room_id
        self.user_id = user_id
        self.badge_dict = {0: 'Passer'}
        self.badge_dict.update({
            lvl: 'Fans' for lvl in range(1,21)
        })
        self.badge_dict.update({
            lvl: 'Captain' for lvl in range(21,50)
        })
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

    def live_danmaku(self):
        room = live.LiveDanmaku(self.room_id)

        @room.on('DANMU_MSG')
        async def on_danmaku(event): # event -> dictionary
            # initial Zone
            user_fans_lvl = 0
            user_title = 'Passer'

            # main information processing Zone
            live_info = event['data']['info']  # list[Unknown, Msg, user_info, fans_info, Unknown:]
            danmaku_content = live_info[1]
            user_main_info = live_info[2]  # list[space_id, Nickname, Unknown:]
            nickname = user_main_info[1]
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

        @room.on('SEND_GIFT')
        async def on_gift(event):
            # 收到礼物
            pass

        sync(room.connect())

    def timestamp_to_Beijing_time(self, timestamp):

        utc_time = datetime.datetime.utcfromtimestamp(timestamp)

        beijing_timezone = datetime.timezone(datetime.timedelta(hours=16))  # 为啥这要是16时间才对呀，没搞懂
        beijing_time = utc_time.astimezone(beijing_timezone)

        formatted_time = beijing_time.strftime("%H:%M:%S")
        return formatted_time

