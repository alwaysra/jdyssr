﻿# coding:utf-8
import sys
import requests
import re
import json

loginurl = 'https://jdycloud.xyz/auth/login'
userurl = 'https://jdycloud.xyz/user'
signurl = 'https://jdycloud.xyz/user/checkin'
userdata = {'email': '2507900291@qq.com',
            'passwd': '123456789abcd'}

def login_sign(loginurl,userurl,userdata,signurl,SCKEY):
    '''
    筋斗云登录并签到
    :param loginurl: 登录url
    :param userurl: 用户主界面
    :param userdata: 提交表单data
    :param signurl: 签到url
    :return:
    '''
    #登录
    r=requests.post(url=loginurl,data=userdata)
    if r.status_code==200:
        print(r.json())
        print(r.cookies)
        cookies=r.cookies
        #访问用户主界面
        r=requests.get(url=userurl,cookies=cookies)
        html=r.text
        #使用正则表达式搜索4个卡片标签
        counters=re.findall('<span class="counter">(.*?)</span>',html)
        #第二个是剩余流量
        shengyuliuliang=counters[1]
        print('剩余流量为:'+shengyuliuliang+'GB')
        r=requests.post(url=signurl,cookies=cookies)
        ujson=json.loads(r.text)
        print(ujson['msg'])
        sendtext='签到之前剩余流量为:'+shengyuliuliang+'GB\n'+ujson['msg']
        sendurl='https://sc.ftqq.com/' + SCKEY + '.send?text=' + sendtext
        requests.get(sendurl)

if __name__ == '__main__':
    print(requests.__version__)
    SCKEY = sys.argv[1]
    login_sign(loginurl,userurl,userdata,signurl,SCKEY)