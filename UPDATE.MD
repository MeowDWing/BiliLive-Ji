# 更新日志
## 2023.8.20 p1
**新增内容**
* 自动读弹幕，目前用的是百度的api，需要自己配置自己的api，具体方法为
  * ```python
    # livget.py
    # > def txt2audio(message, api_flag=False)
    #                                   ^^^^^^ 改为True
    # -->     if api_flag:
    #             SECRET_KEY = ''  改为自己对应的值
    #             API_KEY = ''
    ```
  * 目前该方法还没有优化，会生成大量冗余文件，并且很有可能浪费次数，所以在没看代码时尽量不要用
  * 默认情况下是不打开的，如需打开，要将LiveInfoGet类实例化时加入参数 read_flag = True
  * 设为True后，只要运行reader.py即可开启弹幕读取，默认只读目标直播间有粉丝牌的人


## 2023.8.16 p1
**新增内容**
* 抽奖函数实现

## 2023.8.14 p2
**更新标题更改**
* 由于#number会重定向到PR内容，所以之后的更新信息会改成Update to YYYY.MM.DD pN，pN代表第N次push


## 2023.8.14 #1
**新增内容**
* 完善了对进入直播间事件的监听

**Bug修复**
* 修复了辣条礼物接收时，会重复感谢的问题
* 取消了监听限制机制，现在，你可以自由的打开所有已实现的监听

## 2023.8.12 #1
**新增内容**
* 现在，SC与舰长购买可以开启了
* iosetting的输出新增了自定义颜色项

## 2023.8.11 #1
**特别注意**
* api已找到临时解决方案，在bilibili_api/live.py中，具体解决方案请等待包更新
  * ```
    --- a/bilibili_api/live.py
    +++ b/bilibili_api/live.py
    @@ -960,7 +960,7 @@ class LiveDanmaku(AsyncEvent):
             self.logger.info(f"正在尝试连接主机： {uri}")

             try:
    -                async with session.ws_connect(uri) as ws:
    +                async with session.ws_connect(uri, headers={"User-Agent": "Mozilla/5.0"}) as ws:

                         @self.on("VERIFICATION_SUCCESSFUL")
                         async def on_verification_successful(data):

    ```


## 2023.8.10 #2
**特别注意**
* 经确认，应该不是风控的问题，是api的问题（或者b站抽风），暂时未查明具体原因，下次更新将在抽风结束后稳步开始
* 详细信息见https://github.com/Nemo2011/bilibili-api/issues/419 

## 2023.8.10 #1
**特别注意**
* 为了防止并发请求过高，建议enter_flag不要打开
* 由于ip在测试时疑似被封禁，所以今天没有大更新，更新暂停到ip解禁

**新增内容**
* 为上次更新新家的所有世界输出配置了基本输出设置，由于测试时全部开启导致ip被封了，所以建议不要开的太多，默认开启上限为4
* 为新增输出设置了颜色tag，但还未确定颜色，所以目前新增内容颜色全部设置为默认色


## 2023.8.9 #1
**特别注意**
* 为了最好的使用体验，建议使用Windows Terminal而不是控制台主机，你可以再微软商城直接搜索下载Windows Terminal，如果你是win11，则最新版自带了WT，如果你是win8或更早的版本，则建议在初始化类时将cls_flag设为True


**新增内容**
* 新增弹幕流礼物板块，现在，可以选择打开礼物流了
  * 你可以通过参数gift_flag=True打开礼物流（默认关闭）
      ```python
        import liveget as lg
        x = lg.LiveInfoGet(rid=34162)
        x.living_on(gift_flag=True) 
      ```
  * 礼物的标记颜色默认为亮淡黄色
* 现在，可以通过设置参数来控制某个模块的开启、关闭
  * ```python
    import liveget as lg
    x = lg.LiveInfoGet(rid=34162)
    x.living_on( # 默认配置如下
        danmaku_flag=True, gift_flag=False,  # main
        sc_flag=False, guard_buy_flag=False,   # important
        gift_combo_flag=False, enter_flag=False,  # secondary
        sys_notice_flag=False,  # may need
        sc_jpn_flag=False  # never need  
    )
    ```
* 现在，输出设置自带的为一些特殊的tag配置来源前缀
* InfoText里增加了gift的event字典


**重构内容**
* 对LiveInfoGet类中的live_danmaku函数进行了重构
  * 现在，其所有功能由living_on函数代替
  * live_danmaku在以后将专门作为弹幕的处理函数使用，而living_on用以控制所有直播间信息的开启与否


**Bug修复**
* 纠正了注释文件中的说明错误


## 2023.8.8 #1

**新增内容**
* get_from_web module
  * 本模块支持从web下载图片，目前只用于直播封面获取
  * 本模块之后会在完善后启用，暂时只作为一个拓展模块
* Windows Terminal 设置文档settings.json
  * 字典的参考文档

**重构内容**
* liveget模块
  * initial参数重构，现在可以更方便的输入参数了
  * 回复初始化现在单独成为一个函数以让模块的__init__方法更清晰

**Bug修复**
* 纠正了Update日志中的一个拼写错误
* .gitignore新增无用文档

**Bug查明**
* cmd的问题应该是控制台主机的bug，建议win10+通过下载Windows Terminal解决


## 2023.8.7 #1
**特别注意**
* 发现了一个cmd的bug，该bug会导致：
    * 在win10的cmd中，用于调整颜色的逃逸字符\033颜色会错误的输出为乱码
    * 目前的解决方案是在使用\033前加入os.system("cls")
    * 在没找到具体解决方案前，将暂时使用上述方式解决，如果你不想清理，请将LiveInfoGet的初始化中加入参数（cls_flag=True）

**新增内容**
* 新增sender.py，允许直接在cmd窗口发送弹幕。（需要配置credential,方式见README）
  * 你可以通过如下方式配置
    ```python
    import sender
    x = sender.SenderCMD(rid=room_id, uid=uid, 
                        cls_flag=False  # 为解决特别注意里的bug设置
                        )
    x.send_room()
    # sender.py也配置了main函数，可以直接在里面改           
    ```
  * 你也可以在sender.py里直接配置main函数，然后直接：
    ```commandline
    python sender.py
    ```
* 为liveGetInfo类初始化新增debug参数，现在可以进行简单的debug，以后会进一步增加debug内容

**Bug修复**
* 修复了当粉丝牌不是本直播间的牌子时，也会被认为是FANS并设置错误的弹幕颜色的bug
* 修复了即便没有设置reply_flag，也会在满足条件时尝试reply的bug
* 在.gitignore 增加了一些无用的测试用文件

**目前发现的其他还未处理的bug**
* 有时弹幕会反向显示（直播间是正常的）
* 有时弹幕会在中间突然出现颜色显示问题
* 以上这些问题还未能复现，正在追踪


## 2023.8.6 #2
* 更改 .gitignore 来忽略一些不必要的文件

## 2023.8.6 #1
**1.现在，会根据发话人显示对应颜色了**
```python
content: str = 'NORMAL' #默认为NORMAL
match content:
    case 'SYSTEM': begin_str = '\033[91m'  # Red bright
    case 'ERROR': begin_str = '\033[41m'  # Red bottom
    case 'WARNING': begin_str = '\033[43m'  # Yellow bottom
    case 'SUCCESS': begin_str = '\033[42m'  # Green bottom
    case 'UP': begin_str = '\033[92m'  # Green bright
    case 'CTRL': begin_str = '\033[96m'  # Sky blue bright
    case 'FANS': end_str = ''  # Normal
    case 'CAPTAIN': begin_str = '\033[94m'  # Blue bright
    case 'NORMAL': begin_str = '\033[90m'  # Gray
```
**2.其他新增**

* 现在，你可以自定义触发回复所需要的中文句号的数量以及自动回复的内容了
* 新增了test_py文件夹，里面有一些用于测试的文件
* 新增了UPDATE.MD，现在，每次更新都会有更新日志了


**3.一些关于cookies的更正**

* 我发现cookie貌似会更新，网上说一个月会更新一次，所以可能需要按时自己更新下cookie，
目前还没发现具体怎么自动爬取所需要的cookie

**4.Bug修订**

* 现在，没有自己牌子的直播间也能被正确的处理了
* 删除了LiveInfoGet类初始化时没有必要的赋值
* 修复了一些其他bug

**5.一些勘误**

* 一些正文中注释的更新，具体参考提交日志

**之后的打算**

* 下次会着重解决cookie的问题，尽可能实现自动获取
* 之后，会有更多将目前没有自定义功能的内容逐步实现自定义
* 之后，会对LiveInfoGet类进行重构，设置更多的类来实现更细分的功能，让代码更整洁
* main文件暂时不会更改了，在相当长的时间内，重心会在增加功能上，等主要功能实现的差不多了才会写main

-----

## from repo established to 2023.8.6

缺失
