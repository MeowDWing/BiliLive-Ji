# import bilibili_api as bapi
import os
import sys
import iosetting as ios
import bilibili_api
from bilibili_api import live, sync, user, exceptions
import datetime
import get_from_web as gfw


# Exception Zone
class UserInfoError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class LiveInfoGet:
    """
    直播间信息类，该类目前包含直播间的所有已经实现的操作，以后会细分成多个类/函数

    Live Information class, now, the class include all of realized function, and the class will be split into
    other classes/functions
    """

    def __init__(self, uid: int = -1, rid: int = -1,  # id zone
                 up_name: str = '资深小狐狸', crtl_name: str = '吾名喵喵之翼', auto_msg='。',  # str zone
                 reply_flag: bool = False, cls_flag: bool = False, debug_flag: bool = False,  # flag zone
                 dot_limit: int = 100  # limit zone
                 ):
        """
        你可以输入房间号或者uid的任何一个，代码会自动获取另一个

        you can Enter any of these parameter or not all of them

        :param uid: get in homepage(e.g. https://space.bilibili.com/3117538/ is 3117538)
        :param rid: live room id which is got in live homepage(e.g. https://live.bilibili.com/34162 is 34162)
        :param up_name(str): up名，默认是资深小狐狸 / UP name, default is 资深小狐狸
        :param crtl_name: 控制用户的发言会设为亮青色，你可以设置成你的去高亮你的发言 /
                            controller name, you can set to yourself to highlight your Danmaku
        :param auto_msg: 自定义回复内容 / customize your reply danmaku
        :param reply_flag: 回复标记，True的话开启自动回复功能，目前只适配资深小狐狸的，当然以后会有自定义方式来回复 /
                            if the flag is True, auto reply will on
        :param cls_flag: 清屏标记，该标记用于处理win10中cmd转义字符错误的临时标记，为True时启用
        :param dot_limit: 每dot_limit个中文句号，就自动回复一次 / every dot_limit CN full stop, reply once auto_msg
        """
        # parameter initial zone
        self.room_id = rid
        self.user_id = uid
        self.up_name = up_name
        self.ctrl_name = crtl_name
        self.dot_limit = dot_limit
        self.auto_msg = auto_msg
        self.debug_flag = debug_flag
        self.debug_limit = 1000
        self.shared_counter = 0
        self.shared_dict = {
            'latiao_gift': {'nickname_str': set()}
        }

        self.reply_flag = reply_flag
        if cls_flag:  # 临时解决win10中cmd和powershell可能是转义字符输出错误，解决后本代码将去除
            os.system("cls")

        # dictionary & list initial zone
        #   badge_dict
        self.badge_dict = {0: 'Passer'}
        self.badge_dict.update({
            lvl: 'Fans' for lvl in range(1, 21)
        })
        self.badge_dict.update({
            lvl: 'Captain' for lvl in range(21, 50)
        })
        #   general_list
        # tmp zone
        self.dot_tmp = 0
        self.debug_limit_tmp = 0

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

        # living room cover get
        # gfw.get_dl_files(url=self.room_info['room_info']['cover'])


        # environment param. initial zone
        if self.reply_flag:  # reply_flag = True 时，需要配置文件
            self.sender = self.reply_initial()
            self.auto_reply('test')

        self.room_event_stream = live.LiveDanmaku(self.room_id)

    def living_on(self, danmaku_flag=True, gift_flag=False,  # main
                  sc_flag=False, guard_buy_flag=False,   # important
                  gift_combo_flag=False, enter_flag=False,  # secondary
                  sys_notice_flag=False,  # may need
                  sc_jpn_flag=False  # never need
                  ):
        """

        :param danmaku_flag: 弹幕（开启）标记
        :param gift_flag: 礼物信息开启标记
        :param sc_flag: SC标记
        :param guard_buy_flag: 大航海购买标记
        :param gift_combo_flag: 礼物连击标记
        :param enter_flag: 进场标记
        :param sys_notice_flag: 系统提示标记
        :param sc_jpn_flag: sc日语版标记

        """

        # MAIN zone
        if danmaku_flag:
            @self.room_event_stream.on('DANMU_MSG')
            async def on_danmaku(event):  # event -> dictionary
                await self.live_danmaku(event)
            ios.print_set('弹幕开启', tag='SYSTEM')

        if gift_flag:
            @self.room_event_stream.on('SEND_GIFT')
            async def on_gift(event):
                self.live_gift(event)
            ios.print_set('礼物开启', tag='SYSTEM')
        # Important zone
        if sc_flag:
            pass
        if guard_buy_flag:
            pass
        if gift_flag:
            pass

        # secondary zone
        if gift_combo_flag:
            pass
        if enter_flag:
            pass

        # may n. zone
        if sys_notice_flag:
            pass

        # n.n. zone
        if sc_jpn_flag:
            pass

        sync(self.room_event_stream.connect())

    async def live_danmaku(self, event: dict = None):

        user_fans_lvl = 0
        user_title = 'Passer'
        print_flag = 'NORMAL'

        # main information processing Zone
        live_info = event['data']['info']  # list[Unknown, Msg, user_info, fans_info, Unknown:]
        danmaku_content = live_info[1]
        user_main_info = live_info[2]  # list[uid, Nickname, Unknown:]
        nickname = user_main_info[1]

        if self.reply_flag:
            if danmaku_content == '。':
                self.dot_tmp += 1
                ios.print_set(f"dot now is: {self.dot_tmp}", tag='SYSTEM')
                if self.dot_tmp > self.dot_limit:
                    self.dot_tmp = 0
                    ios.print_set("dot reset", tag='SYSTEM')
                    await self.auto_reply(self.auto_msg)

        if self.debug_flag:
            self.debug_limit_tmp += 1
            if self.debug_limit_tmp % (self.debug_limit / 10) == 0:
                ios.print_set(f"[SYSTEM][DEBUG_TMP]{self.debug_limit_tmp}", tag="SYSTEM")
            if self.debug_limit_tmp > self.debug_limit:
                # self.room_danmaku.remove_event_listener(name="DANMU_MSG", handler=)
                # sync(self.room_danmaku.disconnect())
                ios.print_set("exit", tag="SYSTEM")
                sys.exit()

        user_fans_info = live_info[3]  # list[lvl, worn_badge, Unknown:]
        if len(user_fans_info) != 0:
            if user_fans_info[1] == self.fans_badge:
                print_flag = 'FANS'
                user_fans_lvl = user_fans_info[0]
                if user_fans_lvl > 20:
                    print_flag = 'CAPTAIN'
                user_title = self.badge_dict[user_fans_lvl]

        match nickname:
            case self.ctrl_name:
                print_flag = 'CTRL'
            case self.up_name:
                print_flag = 'UP'

        # timestamp processing Zone
        send_timestamp = event['data']['send_time'] / 1000
        trans_time = self.timestamp_to_Beijing_time(send_timestamp)

        # print_content:
        #       [timestamp][lvl:badge]Nickname:Says
        ios.print_set(f'[{trans_time}][{user_fans_lvl}:{user_title}]{nickname}:{danmaku_content}',
                      tag=print_flag)

    def live_gift(self, event: dict):
        print(event)
        combo_num = 0
        gift_data = event['data']['data']
        action = gift_data['action']
        gift_name = gift_data['giftName']
        nickname = gift_data['uname']
        send_time = event['data']['send_time']
        batch_combo_send = gift_data['batch_combo_send']
        if batch_combo_send is not None:
            combo_num = batch_combo_send['batch_combo_num']

        if gift_name == '辣条':
            self.shared_dict['latiao_gift']['nickname_str'].add(nickname)
            self.shared_counter += 1
            if self.shared_counter > 10:
                self.shared_counter = 0
                name_str = ''
                for i in self.shared_dict['latiao_gift']['nickname_str']:
                    name_str += i + '、'
                nickname = name_str
            else:
                return

        trans_time = self.timestamp_to_Beijing_time(send_time/1000)

        end = ''
        if combo_num > 0:
            end = f"* {combo_num}\n"
        # gift standard print format:
        # [timestamp][Nickname]投喂一个 " GiftName " * combos
        ios.print_set(f"[{trans_time}][{nickname}]{action}一个 \" {gift_name} \" "+end, tag='GIFT')
        #
        #

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

    def reply_initial(self):
        SESSDATA = -1
        bili_jct = -1

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
                case 'SESSDATA': SESSDATA = file_line[1]
                case 'bili_jct': bili_jct = file_line[1]
                case _:
                    ios.print_set('[REPLY MODULE]Undefined or Unused parameter(s)', tag='SYSTEM')
        credential = bilibili_api.Credential(sessdata=SESSDATA, bili_jct=bili_jct)
        sender = live.LiveRoom(self.room_id, credential=credential)
        return sender

    async def auto_reply(self, msg: str):
        try:
            await self.sender.send_danmaku(bilibili_api.Danmaku(msg))
            ios.print_set("successfully reply", tag='SUCCESS')
        except exceptions.ResponseCodeException:  # 登录信息有误也是这个错误，所以不一定是弹幕发送过快，以后会加以区分
            ios.print_set('弹幕发送过快', tag='WARNING')
        finally:
            ios.print_set('auto_reply 结束', tag='SYSTEM')
        # await self.sender.send_danmaku(bilibili_api.Danmaku(msg))
        # ios.print_set("[!]successfully reply", content='SUCCESS')
