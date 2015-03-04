# -*- coding: utf-8 -*-
import scrapy


class BaseItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    add_time = scrapy.Field()
    status = scrapy.Field()
    cat = scrapy.Field() 
    body = scrapy.Field()#抓取描述div内容 方便编辑复制
#     images = scrapy.Field()
#     image_urls = scrapy.Field()
    link = scrapy.Field()


class BlogItem(BaseItem):
    _collection_name = 'js'
    title = scrapy.Field()
    link = scrapy.Field()
