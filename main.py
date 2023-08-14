# import bilibili_api
from bilibili_api import live, sync, user
import asyncio
import liveget as lg
import multiprocessing as mp
import subprocess_init as smp


def main():
    x = lg.LiveInfoGet(rid=6136246, reply_flag=False)
    x.living_on(danmaku_flag=True, gift_flag=False, guard_buy_flag=True,
                gift_combo_flag=False, enter_flag=True, sys_notice_flag=False,
                sc_jpn_flag=True, sc_flag=True)
    # # initial zone
    # process_list = []
    # shared_danmaku_dict = mp.Manager.dict()
    # shared_danmaku_dict.update({'Name': 'Says'})
    #
    # sp_danmaku = smp.SubGetDanmaku('danmaku', room_id=34162)
    # sp_danmaku.start()
    # process_list.append(sp_danmaku)
    #
    # for i in range(5):
    #     p = smp.SubProcess(f"subprocess:{i}")
    #     p.start()
    #     process_list.append(p)
    #
    # for i in process_list:
    #     p.join()
    #
    # print(process_list)
    # print("test end")


if __name__ == '__main__':
    main()
