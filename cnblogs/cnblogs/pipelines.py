# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from cnblogs.items import CnblogsItem
import sys
import MySQLdb as db
import settings

# save mongo
class CnblogsPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get("MONGO_URI"),
            mongo_db = crawler.settings.get("MONGO_DATABASE","cnblogs")
            )

    def open_spider(self,spider):
        self.con = pymongo.MongoClient(self.mongo_uri)
        self.db = self.con[self.mongo_db]

    def close_spider(self,spider):
        self.con.close()

    def _process_info(self,item):
        self.db.cnbloginfos.insert(dict(item))


    def process_item(self, item, spider):
        self._process_info(item) # save mongo
        return item


# # save MySQL
# class CnblogsPipeline(object):
#     def __init__(self):
#         self.con = db.connect(
#             host = settings.MYSQL_HOST,
#             db=settings.MYSQL_DBNAME,
#             user=settings.MYSQL_USER,
#             passwd=settings.MYSQL_PASSWD,
#             charset='utf8',
#             use_unicode=True
#             )
#         self.cur = self.con.cursor()

#     def addInfos(self,item):
#         try:
#             ssql = '''select curl from cnblogs where curl = %s'''
#             vas = item['curl']
#             self.cur.execute(ssql,vas)
#             reptition = self.cur.fetchone()
#             if reptition:
#                 pass
#             else:
#                 values = (
#                     item['title'],
#                     item['curl'],
#                     item['content']
#                     )
#                 sql = '''insert into cnblogs(title,curl,content) values(%s,%s,%s)'''
#                 self.cur.execute(sql,values)
#             self.con.commit()
#         except Exception as e:
#             print e

#     def process_item(self, item, spider):
#         self.addInfos(item)
#         return item
