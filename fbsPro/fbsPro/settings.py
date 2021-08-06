ROBOTSTXT_OBEY = False

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36'

DOWNLOAD_DELAY = 3

##### 增加 Scrapy-Redis 组件的配置

###### （必须）使用 Scrapy-Redis 的调度器，在 Redis 中分配请求
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

###### （必须）使用 Scrapy-Redis 的去重组件，在 Redis 数据库中做去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

###### （必须）允许爬虫出现暂停和暂停后恢复，也就是说不清理 Redis 队列
SCHEDULER_PERSIST = True

###### （必须）指定连接 Redis 数据库IP地址
REDIS_HOST = '10.35.2.24' # 这里需要换成你本地主机的IP

###### （必须）指定连接 Redis 数据库端口号
REDIS_PORT = 6379

###### (必须) 通过配置 RedisPipeline 将 Item 写入 key 为 sidper.name:items 的 Redis 的list 中，以便后面的分布式处理 Item，这个已经由 Scrapy-Redis 实现。
ITEM_PIPELINES = {
   'scrapy_redis.pipelines.RedisPipeline': 300
}
