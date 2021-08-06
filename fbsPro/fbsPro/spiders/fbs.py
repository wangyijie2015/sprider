import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapyRedisPro.items import ScrapyredisproItem
from scrapy_redis.spiders import RedisCrawlSpider
class FbsSpider(CrawlSpider):
    name = 'fbs'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']
    redis_key = 'sun'
    rules = (
        Rule(LinkExtractor(allow=r'type=4&page=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_list = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in li_list:
            title = li.xpath('./span[3]/a/text()').extract_first()
            state = li.xpath('./span[2]/text()').extract_first()
            state = state.strip()
            item = ScrapyredisproItem()
            item['title'] = title
            item['state'] = state
            print(item)
            yield item


