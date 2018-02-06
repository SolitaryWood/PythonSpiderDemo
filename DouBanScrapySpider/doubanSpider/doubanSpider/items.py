# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanspiderItem(scrapy.Item):
    # 电影名
    movie_name = scrapy.Field()
    # 电影信息
    movie_info = scrapy.Field()
    # 电影评分
    movie_rating = scrapy.Field()
    # 电影经典语句
    movie_quote = scrapy.Field()
