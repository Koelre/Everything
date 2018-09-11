# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import log
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cnblogs.items import CnblogsItem


class CnblogSpider(CrawlSpider):
    name = 'cnblog'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['https://www.cnblogs.com/']


    def parse(self,response):
        # 下一页//*[@id="paging_block"]/div/a[12]
        buildPaging = response.xpath('//*[@id="paging_block"]/div/a[last()-1]/text()').extract_first()
        try:
            self.pages = re.findall('\d+',buildPaging)[0]
        except Exception as e:
            self.pages = '0'
        for i in xrange(1,int(self.pages)+1):
            yield scrapy.Request(url='https://www.cnblogs.com/sitehome/p/%s'%str(i),callback=self.parse_t_l_list)

    # 日志
    def log(self,infos):
        log.msg(infos,level=log.INFO)


    # 文章列表
    def parse_t_l_list(self, response):
        articles = response.xpath('//*[@id="post_list"]/div/div[2]/h3/a')
        
        for ar in articles:
            curl = ar.xpath('@href').extract_first()
            title = ar.xpath('text()').extract_first()
            yield scrapy.Request(url=curl,meta={'title':title,'curl':curl},callback=self.parse_details)
        

    # 文章详情
    def parse_details(self,response):
        title = response.meta['title']
        curl = response.meta['curl']
        yield CnblogsItem(title = title,curl = curl,content = str(response.body))

