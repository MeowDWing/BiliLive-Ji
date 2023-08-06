# import bilibili_api as bapi
import os
import iosetting as ios
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
    """
    直播间信息类，该类目前包含直播间的所有已经实现的操作，以后会细分成多个类

    Live Information class, now, the class include all of realized function, and the class will be split into
    other classes
    """

    def __init__(self, user_id: int = -1, room_id: int = -1,  # id zone
                 up_name: str = '资深小狐狸', crtl_name: str = '吾名喵喵之翼', auto_msg = '。',  # str zone
                 reply_flag: bool = False,  # flag zone
                 dot_limit: int = 100  # limit zone
                 ):
        """
        你可以输入房间号或者uid的任何一个，代码会自动获取另一个

        you can Enter any of these parameter or not all of them

        :param user_id: get in homepage(e.g. https://space.bilibili.com/3117538/ is 3117538)
        :param room_id: live room id which is got in live homepage(e.g. https://live.bilibili.com/34162 is 34162)
        :param up_name(str): up名，默认是资深小狐狸 / UP name, default is 资深小狐狸
        :param crtl_name: 控制用户的发言会设为亮青色，你可以设置成你的去高亮你的发言 / controller name, you can set to yourself to highlight your Danmaku
        :param auto_msg: 自定义回复内容 / customize your reply danmaku
        :param reply_flag: 回复标记，True的话开启自动回复功能，目前只适配资深小狐狸的，当然以后会有自定义方式来回复 / if the flag is True, auto reply will on
        :param dot_limit: 每dot_limit个中文句号，就自动回复一次 / every dot_limit CN full stop, reply once auto_msg
        """
        # parameter initial zone
        self.room_id = room_id
        self.user_id = user_id
        self.up_name = up_name
        self.ctrl_name = crtl_name
        self.dot_limit = dot_limit
        self.auto_msg = auto_msg

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
            self.room = live.LiveRoom(room_display_id=self.room_id)
            self.room_info = sync(self.room.get_room_info())
            self.user_id = self.room_info['room_info']['uid']
            if self.room_info['anchor_info']['medal_info'] is not None:
                self.fans_badge = self.room_info['anchor_info']['medal_info']['medal_name']
            else:
                self.fans_badge = 'NO FANS BADGE'
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
            print_flag = 'NORMAL'

            # main information processing Zone
            live_info = event['data']['info']  # list[Unknown, Msg, user_info, fans_info, Unknown:]
            danmaku_content = live_info[1]
            user_main_info = live_info[2]  # list[uid, Nickname, Unknown:]
            nickname = user_main_info[1]

            if danmaku_content == '。':
                self.dot_tmp += 1
                ios.print_set(f"【!】dot now is: {self.dot_tmp}", content='SYSTEM')
                if self.dot_tmp > self.dot_limit:
                    self.dot_tmp = 0
                    ios.print_set("dot reset", content='SYSTEM')
                    await self.auto_reply(self.auto_msg)

            user_fans_info = live_info[3]  # list[lvl, worn_badge, Unknown:]
            if len(user_fans_info) != 0:
                print_flag = 'FANS'
                if user_fans_info[1] == self.fans_badge:
                    user_fans_lvl = user_fans_info[0]
                    if user_fans_lvl > 20:
                        print_flag = 'CAPTAIN'
                    user_title = self.badge_dict[user_fans_lvl]

            match nickname:
                case self.ctrl_name: print_flag = 'CTRL'
                case self.up_name: print_flag = 'UP'

            # timestamp processing Zone
            send_timestamp = event['data']['send_time']/1000
            trans_time = self.timestamp_to_Beijing_time(send_timestamp)

            # print_content:
            #       [timestamp][lvl:badge]Nickname:Says
            ios.print_set(f'[{trans_time}][{user_fans_lvl}:{user_title}]{nickname}:{danmaku_content}',
                          content=print_flag)

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
            ios.print_set("[!]successfully reply", content='SUCCESS')
        except exceptions.ResponseCodeException:  # 登录信息有误也是这个错误，所以不一定是弹幕发送过快，以后会加以区分
            ios.print_set('[WARNING]弹幕发送过快', content='WARNING')
        finally:
            ios.print_set('auto_reply 结束', content='SYSTEM')


        # await self.sender.send_danmaku(bilibili_api.Danmaku(msg))
        # ios.print_set("[!]successfully reply", content='SUCCESS')



