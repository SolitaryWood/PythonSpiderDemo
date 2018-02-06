# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class DoubanspiderPipeline(object):
    def __init__(self):
        # 获取setting文件中设置的数据配置信息
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']
        table = settings['MONGODB_TABLE']

        # 连接数据库
        client = pymongo.MongoClient(host=host, port=port)
        # 指向指定的数据库
        mdb = client[dbname]
        # 指定表名
        self.post = mdb[table]

    def process_item(self, item, spider):
        data = dict(item)
        # 向表插入数据
        self.post.insert(data)

        return item


