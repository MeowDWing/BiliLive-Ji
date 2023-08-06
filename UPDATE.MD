# 更新日志
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

* 现在，你可以自定义出发回复所需要的中文句号的数量以及自动回复的内容了
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