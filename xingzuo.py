#!/usr/bin/python
#-*- coding:utf-8 -*-

import os
import re
import time
import json
import itchat
import requests
from lxml import etree
from urllib.parse import urljoin
from apscheduler.schedulers.blocking import BlockingScheduler


headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
}
class SendWXInfos(object):
    def __init__(self):
        self.lists = [] # 放链接
        self.xingzuoInfos = [] # 放星座信息
        self.wxFriendsname = ["测试用户1","测试用户2"] #微信好友昵称
    
    # 获取星座链接
    def getInfos(self):
        url = 'http://www.xzw.com/fortune/'#'https://www.d1xz.net/yunshi/today/Pisces/'
        res = requests.get(url,headers=headers,timeout=30).text
        etr = etree.HTML(res)
        lis = etr.xpath('//div[@id="list"]//div[@class="alb"]//dl//dt//a')#('//ul[@id="btn_left"]//li//a')
        for li in lis:
            # href = urljoin("https://www.d1xz.net" , li.xpath('@href')[0])
            href = urljoin("http://www.xzw.com" , li.xpath('@href')[0])
            self.lists.append(href)

    # 获取星座名称
    def getXZDet(self,url):
        res = requests.get(url,headers=headers,timeout=30).text
        etr = etree.HTML(res)
        title = etr.xpath('//div[@class="c_main"]//h4')[0].xpath('string(.)').strip()#('//p[@class="title fb"]')[0].xpath('string(.)').strip()#.encode('GBK')
        txt = etr.xpath('//div[@class="c_cont"]//p[1]//span')[0].xpath('string(.)').strip()#('//div[@class="txt"]')[0].xpath('string(.)').replace('','')#.strip().encode('GBK')
        self.xingzuoInfos.append(title+"：\n"+txt+"\n")
        aa = title+"：\n"+txt+"\n"
        if '双鱼座今日运势' in aa:
            print(aa)

    # 获取新闻信息
    def getNews(self):
        url = 'https://feed.sina.com.cn/api/roll/get'
        params = {
            "_":round(int(time.time())*1000),
            "callback":"feedCardJsonpCallback",
            "encode":"utf-8",
            "lid":"1356",
            "num":"20",
            "page":"1",
            "pageid":"121",
            "versionNumber":"1.2.4"
        }
        res = requests.get(url,headers=headers,params=params,timeout=30).text
        infos = re.findall('feedCardJsonpCallback\((.*)\);\}catch',res)[0].replace('█','')
        infos = json.loads(infos)['result']['data']
        self.news = ["新闻早报："] #保存新闻信息
        for i,info in enumerate(infos):
            self.news.append(str(i+1)+'、'+info['title'])
        self.newsmessage = '\n'.join(self.news) #新闻信息
        print(self.newsmessage)

    # 微信发信息
    def send_news(self):
        for wxn in self.wxFriendsname:
            try:
                # 发送给朋友
                my_friend = itchat.search_friends(name=wxn)
                name = my_friend[0]['UserName'] # 0 第一个
            except Exception as e:
                # 发送给群聊
                myroom = itchat.search_chatrooms(name=wxn)
                name = myroom[0]['UserName']
            if '测试用户1' == wxn:
                message = ''.join([m for m in self.xingzuoInfos if '巨蟹座今日运势' in m])
            elif wxn == '测试用户2':
                message = ''.join([m for m in self.xingzuoInfos if '天蝎座今日运势' in m])
            else:
                print(message)

            itchat.send(self.newsmessage,toUserName=name) # 发送新闻信息
            itchat.send(message,toUserName=name) # 发送星座信息

    # 主程序
    def wmain(self):
        # 爬取星座信息
        self.getInfos()
        print(len(self.lists))
        # print(self.lists)
        list(map(self.getXZDet,self.lists))
        print(len(self.xingzuoInfos))
        # print(self.xingzuoInfos)
        # 爬取新闻信息
        self.getNews()

        # 微信登录
        itchat.auto_login(hotReload=True)
        sche = BlockingScheduler()
        time.sleep(2)
        sche.add_job(self.send_news,'date',run_date=time.strftime("%Y-%m-%d %H:%M:%S"))
        sche.start()


def main():
    # 爬取信息
    wx = SendWXInfos()
    wx.wmain()

if __name__ == '__main__':
    main()

