import time

import requests
from tools.get_user_agent import UserAgent
from bs4 import BeautifulSoup
from redis import Redis
from threading import Thread
class GetProxies():
    def __init__(self):
        self.redis = Redis(host='localhost',port=6379)
        self.redis_key = 'spider:proxies'


    def get_html(self,url):
        '''
        获取得页面的url,存储到redis中
        :param url: 统一资源定位符
        :return byte html
        '''
        print(url)
        user_agent = UserAgent().get_pc_user_agent()
        # print(user_agent)
        headers = {
            'User-Agent':user_agent
        }
        res = requests.get(url=url,headers=headers)
        # print(res)
        return res.content


    def parse_html(self,html):
        '''
        解析页面,获得对因的host 和 port
        :param html: str html or byte html
        :return 包含字典的列表
        '''
        contents = []
        soup = BeautifulSoup(html,'lxml')
        proxies = soup.find(name='table').find_all(name='tr')
        for proxie in proxies[1:]:
            td = proxie.find_all(name='td')
            host = td[0].text
            port = td[1].text
            contents.append({'host':host,'port':port})
            proxie_str = 'http://'+host+':'+port
            # self.redis.rpush(self.redis_key,proxie_str)
        return contents


    def save_content(self,contents):
        '''
        将数据保存到redis中
        :param contents:
        '''
        for content in contents:
            host = content['host']
            port = content['port']
            proxie_str = 'http://' + host + ':' + port
            self.redis.rpush(self.redis_key, proxie_str)
            print(proxie_str)


    def get_proxies(self,url):
        html = self.get_html(url)
        contents = self.parse_html(html)
        self.save_content(contents)





# red = Redis(host='localhost', port=6379)
# getproxies = GetProxies()
# for i in range(1,1001):
#     url = 'http://www.xicidaili.com/nn/' + str(i)
#
#     red.lpush('spider:urls',url)
# getproxies.get_all_proxies('http://www.xicidaili.com/nn/1')

# def main():
#     red = Redis(host='localhost', port=6379)
#     while True:
#         key,url = red.brpop('spider:urls')
#         getproxies = GetProxies()
#         getproxies.get_all_proxies(url)
#
# def go(n):
#     tasks = [Thread(target=main) for _ in range(n)]
#     for task in tasks:
#         task.start()
#
#     for task in tasks:
#         task.join()
#     time.sleep(2)
# #
# if __name__ == '__main__':
#     go(8)


