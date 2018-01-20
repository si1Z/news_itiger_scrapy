# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class NewsArticleItem(scrapy.Item):
    #股票号
    symbol = scrapy.Field()
    #股票名
    symbol_name = scrapy.Field()
    #出版时间
    pub_time = scrapy.Field()
    # 出版时间戳
    pub_time_stamp = scrapy.Field()
    # 标题
    article_title = scrapy.Field()
    # 内容摘录
    article_summary = scrapy.Field()
    # 内容
    article_detail = scrapy.Field()
    #关键字
    keywords = scrapy.Field()
    # 网址
    itiger_url = scrapy.Field()
    #源网址
    source_url = scrapy.Field()
    # 来源
    source_media = scrapy.Field()
    #是否为英语
    is_english = scrapy.Field()
    #相关股票
    related_stocks = scrapy.Field()