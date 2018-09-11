# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline

class JobblePipeline(object):
    '''
    异步写入数据库
    '''
    @classmethod
    def from_settings(cls, settings):
        # settings = crawler.settings
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            cursorclass= pymysql.cursors.DictCursor
        )

        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        return cls(db_pool)

    def __init__(self, db_pool):
        self.db_pool = db_pool

    def process_item(self, item, spider):
        '''
        异步执行插入操作
        :param item:
        :param spider:
        '''
        query = self.db_pool.runInteraction(self.insert_item, item)
        query.addErrback(self.handler_error, item, spider)
        return item

    def handler_error(self, failure, item, spider):
        '''
        异常处理
        :param failure:
        :param item:
        :param spider:
        '''
        print(failure)

    def insert_item(self, cursor, item):
        sql = item.creat_insert()
        # 执行sql
        value = (
            item['title'],
            item['link'],
            item['link_hash'],
            item['img_link'],
            item['create_date'],
            item['kind'],
            item['content']
        )
        cursor.execute(sql, value)

    def spider_closed(self, spider):
        self.db_pool.close()


class JoboleImagePipeline(ImagesPipeline):
    '''
    继承内置批pipeline ，重写方法，将下载后的图片路径交给img——link
    '''
    def item_completed(self, results, item, info):
        for ok,value in results:
            img_path = value['path']
            item['img_link'] = img_path
        return item
