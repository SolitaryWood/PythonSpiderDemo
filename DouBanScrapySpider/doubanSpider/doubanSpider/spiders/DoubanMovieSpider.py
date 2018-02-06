# -*- coding: utf-8 -*-
import scrapy
from doubanSpider.items import DoubanspiderItem
import re


class DoubanmoviespiderSpider(scrapy.Spider):
    name = 'DoubanMovieSpider'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250?start=0&filter=']

    def parse(self, response):
        print(response.url)
        movies = response.xpath('//div[@class="info"]')

        for movie in movies:
            movie_name = movie.xpath('./div[@class="hd"]/a/span[1]/text()').extract()[0]
            movie_info = movie.xpath('./div[@class="bd"]/p[1]/text()').extract()[0].strip() + ' / ' + movie.xpath('./div[@class="bd"]/p[1]/text()').extract()[1].strip()
            movie_rating = movie.xpath('./div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            movie_quote = movie.xpath('./div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if movie_quote:
                movie_quote = movie_quote[0]
            else:
                movie_quote = ''

            item = DoubanspiderItem()

            item['movie_name'] = movie_name
            item['movie_info'] = movie_info
            item['movie_rating'] = movie_rating
            item['movie_quote'] = movie_quote

            yield item
        page = int(re.search(r'top250\?(\D*)(\d+)', response.url).group(2))
        s = re.search(r'top250\?(\D*)(\d+)', response.url).group(1)
        if s == '':
            s = 'start='

        if page <= 225:
            url = re.sub(r'top250\?(\D*)(\d+)', 'top250?' + s + str(page + 25), response.url)
            yield scrapy.Request(url, callback=self.parse)
