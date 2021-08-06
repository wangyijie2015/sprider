import scrapy
from imgsPro.items import ImgsproItem

class ImgSpider(scrapy.Spider):
    name = 'img'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://sc.chinaz.com/tupian/rentiyishu.html']

    def parse(self, response):
        div_list = response.xpath('//div[@id="container"]/div')
        for div in div_list:
            #在解析的时候使用伪属性
            src = div.xpath('./div/a/img/@src2').extract_first()

            item = ImgsproItem()
            item['src'] = src

            yield item

