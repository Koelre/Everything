#-*- coding:utf-8 -*-

#author:Koelre

# 黑板课爬虫闯关
# url: http://www.heibanke.com/lesson/crawler_ex00/

import os,sys
import re
import random
import requests
from lxml import etree
import pytesseract
from PIL import Image,ImageEnhance

reload(sys)
sys.setdefaultencoding('utf-8')

# 登录 
# 3,4,5都需要登录
# url: http://www.heibanke.com/accounts/login
def login():
    website1 = 'http://www.heibanke.com/accounts/login'
    se = requests.Session()
    se.get(website1)
    token1 = se.cookies['csrftoken']# 保存csrftoken  
    # 登录参数
    dataWebsite1 = {
        'username': 'Koelre',  
        'password': 'lixue961314',  
        'csrfmiddlewaretoken': token1  
    }
    res = se.post(website1, data=dataWebsite1)#登录
    print res.status_code
    return se


# 第一关 猜数字
# 此次的数字是下一次请求的数字
# url: http://www.heibanke.com/lesson/crawler_ex00/
def ex01():
    # 匹配数字
    def findNum(url):
        res = requests.get(url).content
        num = re.findall('数字[^\d]*(\d+)[\.<]',res)
        return num
    # 首先获得数字
    url = "http://www.heibanke.com/lesson/crawler_ex00/"
    num = findNum(url)
    # 循环直至出来结果
    while num:
        url2 = url+num[0]
        num = findNum(url2)
        print u'访问网页：%s'%url2
    else:
        print u'第二关网页：%s'%url2


# 第二关 猜密码
# 密码是30以内，所以我就没把30放在考虑范围内，就是0-29
# url: http://www.heibanke.com/lesson/crawler_ex01/
def ex02():
    url = 'http://www.heibanke.com/lesson/crawler_ex01/'
    data = {
    "csrfmiddlewaretoken": "8BiM322tV4hbOEO90cSHJXjFw5HDFXEq",
    "username": "a",
    "password": "1"
    }
    for x in xrange(30):
        data["password"] = x
        res = requests.post(url,data=data).content
        if u"错误" not in res:
            print u"密码：%s"%x
            break


# 第三关 猜密码
# 这个相对第二关就需要登录了
# 密码是30以内，所以我就没把30放在考虑范围内，就是0-29
# url: http://www.heibanke.com/lesson/crawler_ex02/
def ex03():
    website2 = 'http://www.heibanke.com/lesson/crawler_ex02/'
    s = login()# 登录
    for x in xrange(30):
        # 以下步骤原理和上面一样
        token2 = s.cookies['csrftoken']
        dataWebsite2 = {
        'username': 'a',  
        'password': x,  
        'csrfmiddlewaretoken': token2
        }
        result = s.post(website2, data=dataWebsite2).content
        if u"错误" not in result: 
            print u"3--密码：%s"%x
            break



# 第四关 猜密码
# 同样需要登录
# 这一关，我看了好几遍才清楚它的密码逻辑
# “密码的位置”最大的是100，所以，密码长度应该是100个
# 如果只是遍历完一遍显示的页数，数字也不能达到100个
# 所以需要循环几遍才能得到所有的
# url: http://www.heibanke.com/lesson/crawler_ex03/
def guesspass(se,password):
    website2 = 'http://www.heibanke.com/lesson/crawler_ex03/'
    dataweb2 = {
    "csrfmiddlewaretoken": "JUwPvezXy54mqH5MrklkBSiecn1ZZnqv",
    "username": "a",
    "password": password
    }
    req = se.post(website2,data=dataweb2).content
    return req

# 收集密码的值
passes = ['' for x in range(101)]
def ex04():
    global passes
    se = login()# 登录
    # for i in range(1,14):
    passwebsite = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page=1'#+str(i)
    # 密码
    res = se.get(passwebsite).content
    etr = etree.HTML(res)
    # 第一个是标题
    trs = etr.xpath('/html/body/div/div/div/table/tr')[1:]
    for tr in trs:
        pa1 = tr.xpath('td[1]/text()')[0].strip()#密码位置
        pa1 = int(re.findall('\d+',pa1)[0])
        pas = tr.xpath('td[2]/text()')[0].strip()#密码的值
        passes[pa1] = pas
    password = ''.join(passes)#把密码拼接字符串
    if len(password)==100:
        # 猜密码
        result = guesspass(se,password)
        # 判断密码是否猜对
        if u"错误" not in result: 
            print u"4--密码：%s"%password
    else:
        ex04()





# 第五关
# 同样需要登录
# 密码同样是数字 - 就从0开始,数字增加
# 途中 弄错了字段，默默的抓狂了好久的哦，最后发现是 captcha_0 字段错了，巨坑啊
# 多了一个验证码，有时候验证码也会识别错误，所以说，同一个数字就多几次识别验证码
# 答案是11
# url: http://www.heibanke.com/lesson/crawler_ex04/
def VerificationCode(imgurl):
    # 保存验证码
    imgs = requests.get(imgurl).content
    with open('1.jpg','wb') as f:
        f.write(imgs)
        
    # 验证码识别，这个不好用，得重新找一个
    image = Image.open('1.jpg')
    imgry = image.convert('L')#图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)#对比度增强
    sharp_img = sharpness.enhance(2.0)
    sharp_img.save('1.jpg')

    text = pytesseract.image_to_string(image)
    return text

def ex05(a=1,passd=0):
    website = 'http://www.heibanke.com/lesson/crawler_ex04/'
    se = login()# 登录
    res1 = se.get(website)
    # print res1.status_code
    etr = etree.HTML(res1.content)
    token2 = etr.xpath('/html/body/div/div/div[2]/form/input/@value')[0].strip()
    imgsrc = etr.xpath('/html/body/div/div/div[2]/form/div[3]/img/@src')[0].strip()
    #验证码链接
    imgurl = 'http://www.heibanke.com'+str(imgsrc)
    #图片code
    capcodes = etr.xpath('//*[@id="id_captcha_0"]/@value')[0]
    # 保存验证码图片且识别验证码
    text = VerificationCode(imgurl)
    # print capcodes,text,passd
    web2data = {
        "csrfmiddlewaretoken":token2,
        "username":"a",
        "password":passd,
        "captcha_0":capcodes,
        "captcha_1":text
    }
    # 提交信息 - 开始猜测
    # 尝试每个数字多猜几次，验证码有时候会识别错误
    res2 = se.post(website,data=web2data,timeout=30).content
    if u"验证码输入错误" not in res2:
        if u"密码错误" not in res2:
            with open('pass.txt','ab') as f:
                f.write(u"密码是：%s"%passd)
        else:
            ex05(a,passd+1)
    else:
        # 多输入几次验证码，预防验证码错误
        if a<=3:
            ex05(a+1,passd)
        else:
            a=1
            ex05(a,passd+1)


def main():
    ex01()# 第一关
    ex02()# 第二关
    ex03()# 第三关
    ex04()# 第四关
    ex05()# 第五关

if __name__ == '__main__':
    main()

