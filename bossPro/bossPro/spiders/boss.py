import scrapy
from bossPro.items import BossproItem

class BossSpider(scrapy.Spider):
    name = 'boss'
    # allowed_domains = ['www.xxx.com']
    # https://www.zhipin.com/c100010000-p100101/?page=2&ka=page-2
    start_urls = ['https://www.zhipin.com/c100010000-p100101/']

    def parse_detail(self,response):
        item = response.meta['item']
        job_desc = response.xpath('.//span[@class="job-name"]a/text()').extract()
        job_desc = ''.join(job_desc)
        print(job_desc)
        item['job_desc'] = job_desc

        yield item
    def parse(self, response):
        li_list = response.xpath('//*[@id="main"]/div/div[2]/ul/li')
        item = BossproItem()
        for li in li_list:
            job_name = li.xpath('.//span[@class="job-name"]a/text()').extract_first()
            item['job_name'] = job_name
            # print(job_name)
            detail_url = li.xpath('.//span[@class="job-name"]a/text()').extract_first()
            #对详情页发请求获取详情页源码数据
            #手动请求的发送
            #请求传参：meta={},可以将meta字典传递给请求对应的回调函数
            yield scrapy.Request(detail_url,callback=self.parse_detail,meta={'item':item})
