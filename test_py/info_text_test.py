from bilibili_api import user,live,sync

ri = 12162669
room = live.LiveRoom(room_display_id=ri)
rinfo = sync(room.get_room_info())
print(rinfo)