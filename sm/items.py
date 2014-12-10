# -*- coding: utf-8 -*-
import scrapy


class BaseItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    brief = scrapy.Field()
    content = scrapy.Field()
    age_range = scrapy.Field()
    can_join = scrapy.Field() #int 0 1
    apply_start = scrapy.Field()
    apply_end = scrapy.Field()
    activity_start = scrapy.Field()
    activity_end = scrapy.Field()
    address = scrapy.Field()
    tel = scrapy.Field()
    update_time = scrapy.Field()
    add_time = scrapy.Field()
    status = scrapy.Field()
    cat = scrapy.Field() #景区id
    act_time_desc = scrapy.Field()
    #-----extra
    body = scrapy.Field()#抓取描述div内容 方便编辑复制
    orig_pic = scrapy.Field()
    orig_previews = scrapy.Field()
    orig_thumb_list = scrapy.Field()
    orig_apply_time = scrapy.Field()
    orig_apply_time_str = scrapy.Field()
    orig_activity_time_str = scrapy.Field()
#     images = scrapy.Field()
#     image_urls = scrapy.Field()
    link = scrapy.Field()


class HahaItem(BaseItem):
    _collection_name = 'haha'


class IzaojiaoItem(BaseItem):
    _collection_name = 'izaojiao'
    title = scrapy.Field()
    host = scrapy.Field()
    attend_time = scrapy.Field()
    link = scrapy.Field()

class FumubangItem(BaseItem):
    _collection_name = 'fumubang'
    title = scrapy.Field()
    business = scrapy.Field()
    price = scrapy.Field()
    sold_count = scrapy.Field()
    attend_time = scrapy.Field()
    link = scrapy.Field()

class BbedenItem(BaseItem):
    _collection_name = 'bbeden'
    title = scrapy.Field()
    link = scrapy.Field()


class QinzizxItem(BaseItem):
    _collection_name = 'qinzizx'
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
