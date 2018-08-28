import time

from redis import Redis

from tools.get_proxy import GetProxies

getproxies = GetProxies()
red = Redis(host='localhost',port=6379)

def get_urls_for_proxies():

    for i in range(101,1000):
        url = 'https://www.kuaidaili.com/free/inha/' + str(i)
        red.lpush('spider:urls',url)
        # break
# getproxies.get_proxies(url)


def main():
    get_urls_for_proxies()
    while True:
        key,url = red.blpop('spider:urls')
        getproxies.get_proxies(url)
        time.sleep(3)

if __name__ == '__main__':
    main()