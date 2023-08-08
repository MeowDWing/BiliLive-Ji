import liveget as lg
import bilibili_api
from bilibili_api import live, sync, exceptions
import iosetting as ios
import os

class SenderCMD:
    def __init__(self, rid: int = 34162, uid: int = -1,
                 cls_flag=False,
                 place=None):
        self.rid = rid
        self.uid = uid
        if cls_flag:
            os.system("cls")

        self.SESSDATA = -1
        self.bili_jct = -1
        self.buvid3 = -1
        self.dedeuserid = -1
        address_file = open(r'.\address.txt', mode='r')
        address_file = address_file.readlines()
        address = address_file[0].strip()
        param_file = open(address, mode='r')
        file_lines = param_file.readlines()
        print(file_lines)
        lines_len = len(file_lines)
        for i in range(lines_len):
            file_line = file_lines[i].strip().split('=')
            print(file_line)
            match file_line[0]:
                case 'SESSDATA':
                    self.SESSDATA = file_line[1]
                case 'bili_jct':
                    self.bili_jct = file_line[1]
                case 'buvid3':
                    self.buvid3 = file_line[1]
                case 'dedeuserid':
                    self.dedeuserid = file_line[1]
                case _:
                    ios.print_set('Undefined parameter(s)', tag='SYSTEM')
        self.credential = bilibili_api.Credential(sessdata=self.SESSDATA, bili_jct=self.bili_jct)

    def sender(self):
        self.send_room = live.LiveRoom(room_display_id=self.rid, credential=self.credential)
        while True:
            send_msg = input(">>>")
            if len(send_msg) > 20:
                ios.print_set("[WARNING]长度超过20个字符，需重新输入", tag="WARNING")
            elif send_msg.strip() == 'cls':
                os.system("cls")
            else:
                try:
                    sync(self.send_room.send_danmaku(bilibili_api.Danmaku(send_msg)))
                    ios.print_set("[!]successfully reply", tag='SUCCESS')
                except exceptions.ResponseCodeException:  # 登录信息有误也是这个错误，所以不一定是弹幕发送过快，以后会加以区分
                    ios.print_set('[WARNING]弹幕发送过快', tag='WARNING')
                finally:
                    ios.print_set('auto_reply 结束', tag='SYSTEM')


def main():
    x = SenderCMD(cls_flag=True)
    x.sender()


if __name__ == "__main__":
    main()
