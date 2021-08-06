# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FbsproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    no = scrapy.Field()  # 编号
    title = scrapy.Field()  # 标题
    content = scrapy.Field()  # 内容
    pass
