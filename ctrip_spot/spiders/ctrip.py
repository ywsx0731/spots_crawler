# -*- coding: utf-8 -*-
import sys;sys.path.append('..')
import scrapy
# from items import CtripSpotItem
from ctrip_spot.items import CtripSpotItem
from scrapy.crawler import CrawlerProcess # 方法一导入

from scrapy.utils.project import get_project_settings # 方法二新增

city_id = {'changsha': 148, 'yueyang': 287, 'zhuzhou': 1174}
city = 'zhuzhou'

class CtripSpider(scrapy.Spider):
    name = 'ctrip'
    allowed_domains = ['ctrip.com']
    start_urls = ['https://m.ctrip.com/webapp/ticket/dest/dt-长沙-{}/s-tickets/?from=https%3A%2F%2Fm.ctrip.com\
            %2Fwebapp%2Fvacations%2Ftour%2Faround%3Fsecondwakeup%3Dtrue%26dpclickjump%3Dtrue%26from%3D\
            https%3A%2F%2Fm.ctrip.com%2Fhtml5%2F&urltype=dt&name=长沙'.format(city_id[city])]

    def parse(self, response):
        spots = response.xpath('//li/div/div[2]')
        # print(spots);input()
        for spot in spots:
            item = CtripSpotItem()
            name = spot.xpath('./h3/a/text()').extract_first()
            score = spot.xpath(".//span[@class='list-tkt-score']/text()").extract_first()
            rec = spot.xpath(".//span[@class='score-star']/text()").extract_first()
            num = spot.xpath("string(.//span[@class='pro-sale-text'])").extract_first()
            address = spot.xpath("string(.//span[contains(@class, 'pro-tkt-distance')])").extract_first()
            price = spot.xpath("string(.//span[contains(@class, 'pro-tkt-price-info')])").extract_first()
            item['name'] = name
            item['score'] = score
            item['rec'] = rec
            item['num'] = num
            item['address'] = address
            item['price'] = price
            yield item

if __name__ == '__main__':
    settings = get_project_settings()
    settings.set('FEED_URI', 'export_data/%(name)s_%(time)s.csv')
    settings.set('MONGO_DB_NAME', city)
    process = CrawlerProcess(settings)
    process.crawl('ctrip')
    process.start()
