# -*- coding: utf-8 -*-
import scrapy
from telnetlib import Telnet

from proxy.items import ProxyItem


class XiciSpider(scrapy.Spider):
    name = 'xici'
    # allowed_domains = ['xici.com']
    start_urls = ['http://www.xicidaili.com/nn/1']

    def parse(self, response):
        # with open('xici.html','wb') as f:
        next_page = response.xpath('//a[@class="next_page"]/@href').extract_first()
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page)
        #     f.write(response.body)
        tr_list = response.xpath('//table[@id="ip_list"]//tr')
        # print(tr_list)
        # print(len(tr_list))
        for tr in tr_list[1:]:
            item = ProxyItem()
            td_list = tr.xpath('.//td/text()').extract()
            # host = td_list[0]
            # port = td_list[1]
            # print(host,port)
            proxy = td_list[5].lower()+'://' + td_list[0] + ':' + td_list[1]
            # print(proxy)
            # break
            item['proxy'] = proxy
            yield item


