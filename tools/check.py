import requests
from redis import Redis
from threading import Thread

from tools.get_user_agent import UserAgent

red = Redis(host='localhost',port=6379)

def check_proxies():
    while True:
        key,proxy = red.blpop('spider:proxies')
        user_agent = UserAgent().get_pc_user_agent()
        header = {
            'User-Agent':user_agent
        }
        try:
            res = requests.get('https://www.baidu.com/',timeout=3,proxies={'http':proxy},headers=header)
        except:
            continue
        else:
            # print(type(res.status_code))
            if res.status_code == 200:
                red.lpush('spider:used_proxies',proxy)
                print(proxy)

def main():
    tasks = [Thread(target=check_proxies) for _ in range(8)]
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()

if __name__ == '__main__':
    main()
