# -*- coding: utf-8 -*-
import scrapy


class JobbleArticleSpider(scrapy.Spider):
    name = 'jobble_article'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://python.jobbole.com/all-posts/']

    def parse(self, response):
        '''
        横向获得下一页链接：加入请求队列
        纵向请求文章链接，解析文章内容
        :param response:
        '''
        pass

    def parse_content(self,response):
        '''
        解析文章内容页面
        :param response:
        '''
        pass
