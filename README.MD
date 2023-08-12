# BiliLive-Ji
本文件每周末更新，若未发布最新版，请移步UPDATE.MD查看更新内容

Update date：2023.8.12
## zh-CN
这是一个学习用项目（练手的，没啥实际使用价值），如果您有什么问题或任何针对代码的建议与问题，欢迎在issue里提问。

要求： 你需要bilibili-api-python 与 python 3.9+

你可以安装bilibili-api-python:

    pip install bilibili-api-python


### 目前的功能
**目前，本项目仍然只是一个库的形式，未来会拓展成一个应用**

* 根据直播间号或uid连接直播间,监听直播间大部分信息
* 在资深小狐狸直播间自动参与将军抽奖*
* 发送弹幕*
> 注意：带*号的功能需要配置cookie并手动更新

### 更新计划

* 在alpha版本到来时，形成一个基于cmd的弹幕姬应用
* 在beta版到来时，完成弹幕姬所有功能
* 在第一个正式版本到来时，做到一个可以供个人使用的项目
* 2.0版本到来时，完成基于web的可视化
* 3.0版本到来时，完成完整的可视化界面

-----

### 例子

#### 连接直播间

```python
import liveget as lg
x = lg.LiveInfoGet(rid=34162, reply_flag=False)
x.living_on(danmaku_flag=True, gift_flag=False, guard_buy_flag=True,
             sc_flag=True,gift_combo_flag=False, enter_flag=False, sys_notice_flag=False,
                sc_jpn_flag=False)
```

#### 在上述功能实现的前提下增加自动回复‘。’参加抽奖

```python
# 讲上段代码中live_room改为
live_room = lg.LiveInfoGet(room_id=34162, reply_flag=True)
# 如果你不想看代码，则：
# 在项目文件夹新建bililive.txt内容参考bililive.txt
# 目前，bililive.txt里的内容需要自己更新，获取方法见下方链接
# 设置完成后，在项目文件夹新建address。txt文件，输入 .\bililive.txt
# 如果你愿意看代码，则根据自己需要配置
# 位置在liveget.py的environment param. zone代码段
#
# 之后，打开直播流
live_room.living_on() # 不加参数时默认只打开弹幕监听
# 即可自动开启回复功能，每当接收到其他人输入的100个句号，则发送一个句号
```
#### 手动发送弹幕
```
python sender.py
REM 需要在sender.py中配置rid
REM 内置cls与exit功能
>>> cls   REM 清屏
>>> exit  REM 退出sender.py
```

其中，得到bililive.txt中参数信息的方式见：

https://nemo2011.github.io/bilibili-api/#/get-credential

-------


## en

Updated date: 2023/8/4

**If updated date is far away from today, please read zh-CN README**

This is a private repo based on bilibili-api-python by python 3.11.4

This repo is just used for private study

If you have any Question or Advise, please propose an issue to make me know
, I'm very pleasant to see it.

#### requirements:

python 3.9+ | bilibili-api-python

you can get the later by 

    pip install bilibili-api-python

### examples

Up to now, there is only one function which is get danmuku
 from anyone living room.

```python
import liveget as lg

live_room = lg.LiveInfoGet(rid=34162)  # creat an instance
live_room.living_on()  # open danmaku streaming
```
-------
I will finish more functions in the future