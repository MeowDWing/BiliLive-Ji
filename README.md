# BiliLive-Ji
## zh-CN
这是一个学习用项目（练手的，没啥实际使用价值），如果您有什么问题或任何针对代码的建议与问题，欢迎再issue里提问。

要求： 你需要bilibili-api-python 与 python 3.9+

你可以安装bilibili-api-python:

    pip install bilibili-api-python


### 目前的功能

**！！！目前，main函数还没完成，所以需要自己去写main或者直接用命令行！！！**

1,根据直播间号或空间号连接直播间,并显示弹幕（见例子）

2,在资深小狐狸的直播间自动参加将军抽奖（需要配置环境变量）

### 后续可能的功能
1：弹幕抽奖

2：自动参与抽奖

3：...

### 目前的实现思路
目前是有几个思路来实现之后的功能，

一个是多进程，通过Pipe来实现进程间通信，分为
弹幕子进程和抽奖子进程，然后当抽奖进程由主进程控制，中断传入（就是用await）指令
开启抽奖模式，开启后弹幕子进程每收到一个弹幕便判断一次牌子/等级或者内容，然后将符合条件的人的名字
以字典或者列表的形式传回抽奖子进程，子进程再收到下一次主进程给出的end指令后返回字典/列表，之后再写一个抽奖代码完成抽奖

第二个就是干脆直接用多个程序，主程序只负责用os.startfile打开子程序，子程序间通过UDP实现本机通信，剩余思路就跟上面一样了。

最后一个就是完全由一个程序来跑，完全靠异步实现，这个我不知道是简单还是难，得写写试试才知道。

-----

### 例子

#### 连接直播间

```python
import liveget as lg

live_room = lg.LiveInfoGet(room_id=34162)  # 实例化直播资料获取对象
live_room.live_danmaku()  # 开启直播流
#   格式：
#   [时间戳][等级:名号]昵称:内容
#   其中，
#   时间戳： 时:分:秒
#   等级： 佩戴当前直播间牌子时，即牌子等级，否则为0
#   名号： 当等级为0时，是passer；小于21时，为Fans；大于21为Captain
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
live_room.live_danmaku()
# 即可自动开启回复功能，每当接收到其他人输入的100个句号，则发送一个句号
```

其中，得到bililive.txt中参数信息的方式见：

https://nemo2011.github.io/bilibili-api/#/get-credential

-------


## en
This is a private repo based on bilibili-api-python by python 3.11.4

This repo is just used for private study

If you have any Question or advise, please propose an issue to make me know
, I'm very pleasant to see it.

#### requirements:

python 3.9+ | bilibili-api-python

you can get it by 

    pip install bilibili-api-python

### examples

Up to now, there is only one function which is get danmuku
 from anyone living room.

```python
import liveget as lg

live_room = lg.LiveInfoGet(room_id=34162)  # creat an instance
live_room.live_danmaku()  # open danmaku streaming
```
-------
I will finish more functions in the future