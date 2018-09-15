import requests
from scrapy.selector import Selector
class CrawlXici():

    def crawl_xici(self):
        '''
        获取代理ip
        条件： speed <  0.5s
        来源 ： 西刺高匿代理
        :return: 代理ip
        '''
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
        }
        re = requests.get('http://www.xicidaili.com/nn/',headers=headers)
        selector_xici = Selector(text=re.text)
        all_trs = selector_xici.css('#ip_list tr')
        for tr in all_trs[1:]:
            speed_str = tr.css('.bar::attr(title)').extract_first()
            if speed_str:
                speed = float(speed_str.strip('秒'))
                if speed > 0.5:
                    continue
            all_text = tr.css('td::text').extract()
            ip = all_text[0]
            port = all_text[1]
            http_type = all_text[5].lower()
            print(ip,port,http_type)
            break
if __name__ == '__main__':
    pass