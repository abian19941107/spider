import telnetlib
from threading import Thread

import redis
def test_proxy():
    reds = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        try:
            key,proxy = reds.brpop('spider:proxy')
        except:
            continue
        else:
            proxy = str(proxy)

            host = proxy.split(':')[1].strip("//'")
            port = proxy.split(':')[2].strip("//'")
            # print(proxy)
            print(host,port)
            try:
                telnetlib.Telnet(host=host,port=port,timeout=3)
            except:
                print('ip不可用')
            else:
                print('ip地址可用')
                reds.lpush('spider:proxy', proxy)
            # break
def thread_test(n):
    tasks = [Thread(target=test_proxy) for _ in range(n)]
    for task in tasks:
        task.start()

    for task in tasks:
        task.join()

if __name__ == '__main__':
    thread_test(8)