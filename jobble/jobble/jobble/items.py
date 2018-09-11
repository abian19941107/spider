# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose,Join

from untils import handle_blank, handle_job_city


class JobbleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    link_hash = scrapy.Field()
    img_link = scrapy.Field()
    create_date = scrapy.Field()
    kind = scrapy.Field()
    content = scrapy.Field()

    def creat_insert(self):
        return 'insert into jobble value (0,%s,%s,%s,%s,%s,%s,%s)'

    def creat_values(self):
        value = (
            self.title,
            self.link,
            self.link_hash,
            self.img_link,
            self.create_date,
            self.kind,
            self.content
        )
        print(value)
        return value

class LagouItemLoader(ItemLoader):
    default_input_processor = MapCompose(handle_blank)
    default_output_processor = TakeFirst()

class LagouJob(scrapy.Item):
    '''
    拉勾的职位信息
    '''
    title = scrapy.Field()
    url= scrapy.Field()
    url_object_id= scrapy.Field()
    salary= scrapy.Field()
    job_city= scrapy.Field()
    work_years= scrapy.Field()
    degree_need= scrapy.Field()
    job_type= scrapy.Field()
    publish_time= scrapy.Field(
        input_processor = MapCompose(lambda x:x.split())
    )
    tags= scrapy.Field(
        output_processor = Join(',')
    )
    job_advantage= scrapy.Field()
    job_desc= scrapy.Field()
    job_addr= scrapy.Field(
        input_processor = MapCompose(handle_job_city)
    )
    company_url= scrapy.Field()
    company_name= scrapy.Field(
        output_processor = Join()
    )
    crawl_time= scrapy.Field()
    crawl_update_time= scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
            insert into lagou(
              url,url_object_id,title,salary,
              job_city,work_years,degree_need,job_type,
              publish_time,tags,job_advantage,job_desc,
              job_addr,company_url,company_name,crawl_time
            ) values(
                %s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s,%s,
                %s,%s,%s,%s
                ) 
            on DUPLIACTE key update crawl_update_time = values ()
        '''
        params = (
            self['url'],self['url_object_id'],self['title'],self['salary'],
            self['job_city'], self['work_years'], self['degree_need'], self['job_type'],
            self['publish_time'], self['tags'], self['job_advantage'], self['job_desc'],
            self['job_addr'], self['company_url'], self['company_name'], self['crawl_time'],
        )
