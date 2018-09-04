#!/usr/bin/python
#-*- coding:utf-8 -*-

__author__  = 'lixxue'
__version__ = '1.0.0'

import re,os,sys
import requests
import json
import csv
from lxml import etree


reload(sys)
sys.setdefaultencoding('utf-8')

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}

path = os.path.abspath(os.path.dirname(__file__))
filepath = os.path.join(path,'YSLMouthred')


class YSLBrand(object):
    def __init__(self):
        self.filepath = filepath
        
    '''文件夹列表'''
    def mkimgdir(self):
        self.imgpath = os.path.join(self.filepath,self.pname)
        if not os.path.exists(self.imgpath):
            os.makedirs(self.imgpath)

    '''保存CSV'''
    def saveCSV(self,infoes):
        for info in infoes:
            with open('YSLMouthred.csv','ab') as f:
                writer = csv.writer(f)
                writer.writerow(info)


    '''产品列表'''
    def getlist_product(self):
        url = 'https://www.yslbeautycn.com/makeup-lips-and-nails?ni=15&s=category_order_14_desc%2Cdefault_sort_asc&pn=2&pageSize=8'
        res = requests.get(url,headers=headers,timeout=30).text
        etr = etree.HTML(res)
        divs = etr.xpath('//*[@id="wrapper"]/section/article/div/div[2]/div/div[2]/div[1]/div/div')
        productlist = []
        for div in divs:
            ahref = 'https://www.yslbeautycn.com' + str(div.xpath('div[1]/a/@href')[0])
            title = div.xpath('div[2]/p[2]/a/text()')[0]
            price = div.xpath('div[2]/div[2]/div[2]/span/text()')[0].replace('¥','')
            productlist.append((ahref,title,price))
            # print ahref,title,price
        return productlist


    '''每种色号'''
    def ysldetails(self):
        res = requests.get(self.durl,headers=headers,timeout=30).text
        itemDetail = re.findall('itemDetail = (\{.*\})',res)[0]
        colorSwatches = json.loads(itemDetail)['colorSwatches']
        colors = []
        for color in colorSwatches:
            colorimg = 'https://res.yslbeautycn.com/resources/' + str(color['image'])
            imgname = color['propertyValue']+'.jpg'
            img = requests.get(colorimg,headers=headers,timeout=30).content
            with open(os.path.join(self.imgpath,imgname),'wb') as file:
                file.write(img)
            colors.append((self.pname,str(color['propertyValue']),self.price,self.durl))

        self.saveCSV(colors)


    def test(self):
        productlist = self.getlist_product()
        for pro in productlist:
            # print pro[0],pro[1],pro[2]
            self.durl = pro[0]
            self.pname = pro[1]
            self.price = pro[2]
            self.mkimgdir()
            self.ysldetails()

def main():
    ysl = YSLBrand()
    ysl.test()

if __name__ == '__main__':
    main()
