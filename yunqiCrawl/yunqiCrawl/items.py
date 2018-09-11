# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 小说的基本信息
class YunqiBookListItem(scrapy.Item):
    # 小说id
    novelId = scrapy.Field()
    # 小说名称
    novelName = scrapy.Field()
    # 小说链接
    novelLink = scrapy.Field()
    # 小说作者
    novelAuthor = scrapy.Field()
    # 小说类型
    novelType = scrapy.Field()
    # 小说状态
    novelStatus = scrapy.Field()
    # 小说更新时间
    novelUpdateTime = scrapy.Field()
    # 小说字数
    novelWords = scrapy.Field()
    # 小说封面
    novelImageUrl = scrapy.Field()


# 小说的热度
class YunqiBookDetailItem(scrapy.Item):
    # 小说id
    novelId = scrapy.Field()
    # 小说标签
    novelLabel = scrapy.Field()
    # 小说总点击量
    novelAllClick = scrapy.Field()
    # 小说月点击量
    novelMonthClick = scrapy.Field()
    # 小说周点击量
    novelWeekClick = scrapy.Field()
    # 小说总人气
    novelAllPopular = scrapy.Field()
    # 小说月人气
    novelMonthPopular = scrapy.Field()
    # 小说周人气
    novelWeekPopular = scrapy.Field()
    # 小说评论数
    novelCommentNum = scrapy.Field()
    # 小说总推荐
    novelAllComm = scrapy.Field()
    # 小说月推荐
    novelMonthComm = scrapy.Field()
    # 小说周推荐
    novelWeekComm = scrapy.Field()

        