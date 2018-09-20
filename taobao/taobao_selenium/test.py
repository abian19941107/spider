from selenium import webdriver
from selenium.webdriver.chrome import options
from scrapy.selector import Selector
import time

# browser = webdriver.Chrome()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://www.taobao.com/')
browser.implicitly_wait(10)
browser.find_element_by_xpath('//input[@id="q"]').send_keys('男装')
browser.find_element_by_xpath('//div[@class="search-button"]/button').click()

for i in range(10):
    time.sleep(3)
    # taobao_page = Selector(browser.page_source)
    # taobao_page.xpath('')
    browser.find_element_by_xpath('//div[@id="mainsrp-pager"]/div[contains(@class,"m-page")]//ul/li[contains(@class,"next")]/a').click()



browser.quit()
