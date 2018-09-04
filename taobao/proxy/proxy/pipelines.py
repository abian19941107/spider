# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis

class ProxyPipeline(object):
    def process_item(self, item, spider):
        reds = redis.Redis(host='localhost',port=6379,db=0)
        print(item['proxy'])
        reds.lpush('spider:proxy', item['proxy'])
        return item
