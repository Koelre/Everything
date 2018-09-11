#!/usr/bin/python
#-*- coding:utf-8 -*-

import os,sys
import MySQLdb as db
import pandas as pd
from sqlalchemy import create_engine  # 报错安装  pip install flask-SQLAlchemy
from pymongo import MongoClient

reload(sys)
sys.setdefaultencoding('utf-8')

class ReaptDBInfos(object):
    """ 对mysql 数据库数据表进行去重 """
    def __init__(self):
        self.MYSQL_HOST = "localhost"
        self.MYSQL_DBNAME = "cnblogs"
        self.MYSQL_USER = "root"
        self.MYSQL_PASSWD = "123456"

    def reaptInfos(self):
        dbs = db.connect(
            host = self.MYSQL_HOST,
            user = self.MYSQL_USER,
            passwd=self.MYSQL_PASSWD,
            db = self.MYSQL_DBNAME,
            charset = 'utf8',
            use_unicode = True
            )
        sql = 'select title,curl from cnblogs'
        df = pd.read_sql(sql,dbs)
        dr = df.drop_duplicates()
        yot = create_engine("mysql+mysqldb://root:123456@localhost:3306/cnblogs?charset=utf8")
        pd.io.sql.to_sql(dr,'reapts',yot,if_exists='replace',index=False)
        dr.to_csv('cnblogs.csv',index=False)
        yot.close()


""" 对mongo 数据库数据表进行去重 """
class ReaptMogoInfos(object):
    """ 对mysql 数据库数据表进行去重 """
    def __init__(self):
        self.host = 'localhost'
        self.port = 27017
        self.username = None
        self.password = None
        self.db = 'cnblogs'
        self.collection = 'cnbloginfos'

    def _con_mongo(self):
        if self.username and self.password:
            # mongodb://username:password@host:port/db
            mongo_uri = 'mongodb://%s:%s@%s:%s/%s'%(self.username,self.password,self.host,self.port,self.db)
            conn = MongoClient(mongo_uri)
        else:
            conn = MongoClient(self.host,self.port)
        return conn[self.db]


    def read_mongo(self,query={}):
        db = self._con_mongo()
        cursor = db[self.collection].find(query)
        df = pd.DataFrame(list(cursor))
        print df
        df.to_csv('infos.csv',index=False)
        
        
if __name__ == '__main__':
    redb = ReaptDBInfos()
    redb.reaptInfos()

    mogo = ReaptMogoInfos()
    mogo.read_mongo()

