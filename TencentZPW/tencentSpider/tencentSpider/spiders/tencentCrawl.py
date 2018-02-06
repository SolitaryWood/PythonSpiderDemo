# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencentSpider.items import TencentItem

'''
	通过scrapy genspider -t crawl tencentcrawl "tencent.com"命令，
	可以创建CrawlSpider模板的爬虫文件
'''

# 编写的爬虫类继承CrawlSpider类，这个类是Spider类派生出来的类
# 这个类定义了一些规则rules来提供跟进link的
class TencentcrawlSpider(CrawlSpider):
    name = 'tencentcrawl'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0']

    rules = (
    	# LinkExtractor方法创建一个对象，规定要提取的链接
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # 提取页面数据
        for res in response.xpath('//tr[@class="even"]|//tr[@class="odd"]'):
            item = TencentItem()
            positionName = res.xpath('./td[1]/a/text()').extract()[0]
            detailLink = res.xpath('./td[1]/a/@href').extract()[0]
            positionType = res.xpath('./td[2]/text()').extract()
            if positionType:
                positionType = positionType[0]
            else:
                positionType = ''
            positionNum = res.xpath('./td[3]/text()').extract()[0]
            workplace = res.xpath('./td[4]/text()').extract()[0]
            publishTime = res.xpath('./td[5]/text()').extract()[0]

            item['positionName'] = positionName
            item['detailLink'] = detailLink
            item['positionType'] = positionType
            item['positionNum'] = positionNum
            item['workplace'] = workplace
            item['publishTime'] = publishTime
            yield item 
        
