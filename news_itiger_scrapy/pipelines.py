# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class MongoDBPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self,settings):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db_auth = connection.admin
        if db_auth.authenticate(settings['MONGODB_USER'], settings['MONGODB_PWD']):
            mydb = connection[settings['MONGODB_DB']]
            self.collection = mydb[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
        # valid = True
        # for data in item:
        #     if not data:
        #         valid = False
        # if valid:
        #     self.collection.insert(dict(item))
        #     print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        # return item