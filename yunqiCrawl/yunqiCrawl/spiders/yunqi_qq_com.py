# -*- coding: utf-8 -*-
import scrapy
import logging
from yunqiCrawl.items import YunqiBookListItem
from yunqiCrawl.items import YunqiBookDetailItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class YunqiQqComSpider(CrawlSpider):
    name = 'yunqibooks'
    allowed_domains = ['yunqi.qq.com']
    start_urls = ['http://yunqi.qq.com/bk/so2/n10p1']

    rules = (
        Rule(LinkExtractor(allow=r'/bk/so2/n10p\d+'), callback='parse_book_list', follow=True),
    )

    # 图书列表
    def parse_book_list(self,response):
        books = response.xpath('.//div[@class="book"]')
        for book in books:
            novelImageUrl = book.xpath('./a/img/@src').extract_first()
            novelId = book.xpath('div[@class="book_info"]/h3/em/a[2]/@bid').extract_first()
            novelName = book.xpath('div[@class="book_info"]/h3/a/text()').extract_first()
            print novelId,novelName

            novelLink = book.xpath('a/@href').extract_first()
            novelInfos = book.xpath('./div[@class="book_info"]/dl/dd[@class="w_auth"]')
            logging.info("novelInfos lenth:%s"%len(novelInfos))
            if len(novelInfos)>4:
                novelAuthor = novelInfos[0].xpath('./a/text()').extract_first()
                novelType = novelInfos[1].xpath('./a/text()').extract_first()
                novelStatus = novelInfos[2].xpath('./text()').extract_first()
                novelUpdateTime = novelInfos[3].xpath('./text()').extract_first()
                novelWords = novelInfos[4].xpath('./text()').extract_first()
            else:
                novelAuthor = ""
                novelType = ""
                novelStatus = ""
                novelUpdateTime = ""
                novelWords = ""
            booklistItem = YunqiBookListItem(novelId=novelId, novelName = novelName, novelLink = novelLink, novelAuthor = novelAuthor, novelType = novelType, novelStatus = novelStatus, novelUpdateTime = novelUpdateTime, novelWords = novelWords, novelImageUrl = novelImageUrl)
            yield booklistItem
            yield scrapy.Request(url=novelLink,meta={'novelId':novelId},callback=self.parse_book_detail)


    # 小说点击及其人气数据
    def parse_book_detail(self,response):
        novelId = meta["novelId"]
        novelLabel = response.xpath('//div[class="tags"]/text()').extract_first()
        novelAllClick = response.xpath('//*[@id="novelInfo"]/table/tr[2]/td[1]/text()').extract_first()
        novelMonthClick = response.xpath('//*[@id="novelInfo"]/table/tr[3]/td[1]/text()').extract_first()
        novelWeekClick = response.xpath('//*[@id="novelInfo"]/table/tr[4]/td[1]/text()').extract_first()
        novelAllPopular = response.xpath('//*[@id="novelInfo"]/table/tr[2]/td[2]/text()').extract_first()
        novelMonthPopular = response.xpath('//*[@id="novelInfo"]/table/tr[3]/td[2]/text()').extract_first()
        novelWeekPopular = response.xpath('//*[@id="novelInfo"]/table/tr[4]/td[2]/text()').extract_first()
        novelCommentNum = response.xpath('//*[@id="novelInfo_commentCount"]/text()').extract_first()
        novelAllComm = response.xpath('//*[@id="novelInfo"]/table/tr[2]/td[3]/text()').extract_first()
        novelMonthComm = response.xpath('//*[@id="novelInfo"]/table/tr[3]/td[3]/text()').extract_first()
        novelWeekComm = response.xpath('//*[@id="novelInfo"]/table/tr[4]/td[3]/text()').extract_first()
        print novelAllClick,novelAllComm
        logging.info("novelAllClick,novelAllComm: %s"%(novelAllClick,novelAllComm))
        bookdetailItem = YunqiBookDetailItem(novelId = novelId, novelLabel = novelLabel, novelAllClick = novelAllClick, novelMonthClick = novelMonthClick, novelWeekClick = novelWeekClick, novelAllPopular = novelAllPopular, novelMonthPopular = novelMonthPopular, novelWeekPopular = novelWeekPopular, novelCommentNum = novelCommentNum, novelAllComm = novelAllComm, novelMonthComm = novelMonthComm, novelWeekComm = novelWeekComm)
        yield bookdetailItem


