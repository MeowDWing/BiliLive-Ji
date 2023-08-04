# import bilibili_api as bapi
from bilibili_api import live, sync, user

class LiveInfoGet:
    def __init__(self, user_id, room_id=None, flag=False):
        self.user_id = user_id
        self.badge_dict = {0: 'Passer'}
        self.badge_dict.update({
            lvl: 'Fans' for lvl in range(1,21)
        })
        self.badge_dict.update({
            lvl: 'Captain' for lvl in range(21,50)
        })
        if room_id is not None:
            self.room_id = room_id
        if flag is True:
            pass
        else:
            self.user_info = user.User(uid=self.user_id)
            self.user_live_info_details = sync(self.user_info.get_live_info())
            self.fans_badge = self.user_live_info_details['fans_medal']['medal']['medal_name']
            self.room_id = self.user_live_info_details['live_room']['roomid']

    def live_danmaku(self):
        room = live.LiveDanmaku(self.room_id)

        @room.on('DANMU_MSG')
        async def on_danmaku(event): # event -> dictionary
            live_info = event['data']['info']
            danmaku_content = live_info[1]
            user_main_info = live_info[2]
            user_fans_info = live_info[3]
            if user_fans_info[1] != self.fans_badge:
                user_fans_info[0] = 0
            print(f'the {self.badge_dict[user_fans_info[0]]} {user_main_info[1]}(uid:{user_main_info[0]}),say:{danmaku_content}')
            """
            {
                'room_display_id': 34162,
                'room_real_id': 34162,
                'type': 'DANMU_MSG',
                'data': {
                    'cmd': 'DANMU_MSG',
                    'dm_v2':'CiIxM2I3NzFjODgyNzM3M2U0NDRhNjdhZmE3YTU4ZWQ2OTIzEAQYGSD//4wHKggzMzk3MjA2ZjIBMTiWlYHdmzFItdmupgZiIQgFEh0jMTQ1M0JBRkYsIzRDMjI2M0EyLCMzMzUzQkFGRooBAJoBEAoIMjM0QTlFMTIQp9yupgaiAa4BCOKU/QwSEuWQvuWQjeWWteWWteS5+e/vBoHIzAwRDFGMSJKaHR0cHM6Ly9pMi5oZHNsYi5jb20vYmZzL2ZhY2UvOGVmZTE0ZWI1Y2EyMTdlYTJmMjFiYTc3OWI5M2ViYmFjZDViMGE2Yi5qcGc4kE5AAVogCBUSBuiQjOeLkCDLqGkw/9GfAzjLqGlAkrvKAkgDUAFiDwgHEJat2gQaBj41MDAwMGoAcgB6AggJqgEaCOKjvgESD+i1hOa3seWwj+eLkOeLuBjyigI=',
                    'info': [
                    0           [
                                    0, 4, 25, 14893055, 1691069991574, 1691069621, 0, '3397206f', 0, 0, 5, '#1453BAFF,#4C2263A2,#3353BAFF', 0, '{}', '{}',
                                    {'extra': '{"send_from_me":false,"mode":0,"color":14893055,"dm_type":0,"font_size":25,"player_mode":4,"show_player_type":0,"content":"1","user_hash":"865542255","emoticon_unique":"","bulge_display":0,"recommend_score":6,"main_state_dm_color":"","objective_state_dm_color":"","direction":0,"pk_direction":0,"quartet_direction":0,"anniversary_crowd":0,"yeah_space_type":"","yeah_space_url":"","jump_to_url":"","space_type":"","space_url":"","animation":{},"emots":null,"is_audited":false,"id_str":"13b771c8827373e444a67afa7a58ed6923","icon":null}',
                                    'mode': 0,
                                    'show_player_type': 0},
                                    {'activity_identity': '',
                                    'activity_source': 0,
                                    'not_show': 0},
                                    0
                                ],
                    1           '1',    // 弹幕内容
                    2           [27216482, '吾名喵喵之翼', 0, 0, 0, 10000, 1, '#00D1F1'], //用户主要信息戳
                    3           [21, '萌狐', '资深小狐狸', 34162, 1725515, '', 0, 6809855, 1725515, 5414290, 3, 1, 3117538], //用户铭牌信息戳
                    4           [7, 0, 9868950, '>50000', 0],
                    5           ['', ''],   //未知
                    6:9         0, 3, None, //未知
                    9           {'ct': '234A9E12', 'ts': 1691069991},//未知
                    10:          , 0, None, None, 0, 105, [9] //未知
                            ],          // 弹幕主要信息戳
                    'is_report': False,
                    'msg_id': '1319167094968832',
                    'send_time': 1691069991555
                    }
            }
            """

        @room.on('SEND_GIFT')
        async def on_gift(event):
            # 收到礼物
            print(event)

        sync(room.connect())



