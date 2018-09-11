# -*- coding: utf-8 -*-
import scrapy

from jobble.items import JobbleItem
from jobble.untils import handle_by_md5


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
        next_page = response.css(".next.page-numbers::attr(href)").extract_first()
        yield scrapy.Request(next_page)
        articles = response.css('.post.floated-thumb')
        for article in articles:
            # 获取需要的字段
            link = article.xpath('.//a[@class="archive-title"]/@href').extract_first()
            link_hash = handle_by_md5(link)
            title = article.xpath('.//a[@class="archive-title"]/text()').extract_first()
            img_link = article.xpath('.//img/@src').extract()
            create_date = ''.join(article.xpath('.//div[@class="post-meta"]/p/text()').extract()).strip().strip(' ·')
            kind = article.xpath('.//div[@class="post-meta"]//a[@rel]/text()').extract_first()
            # 插入item
            item = JobbleItem()
            item['link'] = link
            item['link_hash'] = link_hash
            item['title'] = title
            item['img_link'] = img_link
            item['create_date'] = create_date
            item['kind'] = kind
            yield scrapy.Request(link,callback=self.parse_content,meta={'item':item})

    def parse_content(self,response):
        '''
        解析文章内容页面
        :param response:
        '''
        item = response.meta['item']
        content = response.xpath('//div[@class="entry"]').extract_first()
        item['content'] = content
        yield item
