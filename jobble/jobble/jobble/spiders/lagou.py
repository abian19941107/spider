# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.shell import inspect_response
from scrapy.spiders import CrawlSpider, Rule

from items import LagouItemLoader, LagouJob
from untils import handle_by_md5


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']


    rules = (
        Rule(LinkExtractor(allow=r'zhaopin/.*'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/j\d+.html'),follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):

        item_loader = LagouItemLoader(item=LagouJob(),response=response)
        item_loader.add_xpath('title','//div[@class="job-name"]/@title')
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',handle_by_md5(response.url))
        item_loader.add_xpath('salary','//span[@class="salary"]/text()')
        item_loader.add_xpath('job_city','//*[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath('work_years','//*[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath('degree_need','//*[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath('job_type','//*[@class="job_request"]/p/span[5]/text()')
        item_loader.add_xpath('publish_time','//p[@class="publish_time"]/text()')
        item_loader.add_xpath('tags','//ul[contains(@class,"position-label")]/li/text()')
        item_loader.add_xpath('job_advantage','//dd[@class="job-advantage"]/p/text()')
        item_loader.add_xpath('job_desc','string(//dd[@class="job_bt"]/div)')
        item_loader.add_xpath('job_addr','string(//div[@class="work_addr"])')
        item_loader.add_xpath('company_url','//dl[@class="job_company"]/dt/a/@href')
        item_loader.add_xpath('company_name','//dl[@class="job_company"]/dt/a/div/h2/text()')
        item_loader.add_value('crawl_time',datetime.datetime.now())

        item = item_loader.load_item()
        yield item()
