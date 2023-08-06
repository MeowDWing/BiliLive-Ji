# from urllib import request
# from http import cookiejar
#
# cookie = cookiejar.CookieJar()
# handler = request.HTTPCookieProcessor(cookie)
# opener = request.build_opener(handler)
# response = opener.open('https://www.baidu.com')
# print(cookie)

import requests

# 登录地址
url = 'https://passport.bilibili.com/web/login/v2'

# 构造登录的 POST 数据，其中 username 和 password 是账号密码
login_data = {
    'username': '15090192527',
    'password': 'hzf123156'
}

# 发送登录请求
response = requests.post(url, data=login_data)

# 检查是否登录成功
if response.status_code == 200 and response.json()['code'] == 0:
    print('登录成功！')
else:
    print('登录失败！')
