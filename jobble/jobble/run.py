from scrapy.cmdline import execute

import sys
import os
# print(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute('scrapy crawl jobble_article'.split())
