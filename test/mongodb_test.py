#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/19 16:20
# @Author  : zhujinghui
# @File    : mongodb_test.py
# @Software: PyCharm
import pymongo
settings = {
'MONGODB_SERVER': 'dds-2ze641fbc7603b641871-pub.mongodb.rds.aliyuncs.com',
'MONGODB_PORT': 3717,
'MONGODB_USER': 'root',
'MONGODB_PWD': 'Ygkj@2017',
'MONGODB_DB': 'newsdb',
'MONGODB_COLLECTION': 'itiger_news',
}

connection = pymongo.MongoClient(
            host=settings['MONGODB_SERVER'],
            port=settings['MONGODB_PORT'],


        )
db_auth = connection.admin
tmp = db_auth.authenticate(settings['MONGODB_USER'],settings['MONGODB_PWD'])
print(tmp)
mydb = connection[settings['MONGODB_DB']]
# mydb.authenticate(settings['MONGODB_USER'],settings['MONGODB_PWD'])
collection = mydb[settings['MONGODB_COLLECTION']]

test = {'a':1,'b':2}

tm = collection.insert(test)
print(tm)