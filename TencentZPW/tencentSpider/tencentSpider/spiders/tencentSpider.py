# coding:utf-8
import scrapy
from tencentSpider.items import TencentItem
import re

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0']

    def parse(self, response):
        # 获取总页面，312页
        pages = response.xpath('//div[@class="pagenav"]/a[last()-1]/text()').extract()[0]
        url = 'https://hr.tencent.com/position.php?&start='
        # 提取页面数据
        for res in response.xpath('//tr[@class="even"]|//tr[@class="odd"]'):
            item = TencentItem()
            positionName = res.xpath('./td[1]/a/text()').extract()[0]
            detailLink = res.xpath('./td[1]/a/@href').extract()[0]
            positionType = res.xpath('./td[2]/text()').extract()
            # 因为有的职位没有类别，所以这里做一下判断
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
        # 当一页数据提取完毕后，发送下一页请求
        page = int(re.search('\d+', response.url).group(0))
        if page <= int(pages) * 10:
            yield scrapy.Request(url + str(page + 10), callback = self.parse)
