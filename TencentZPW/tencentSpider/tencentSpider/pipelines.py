# -*- coding: utf-8 -*-
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TencentspiderPipeline(object):
    def __init__(self):
        self.file = open('tencent.json', 'w')

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii = False) + '\n'
        self.file.write(data)
        return item

    def close_spider(self, spider):
        self.file.close()
