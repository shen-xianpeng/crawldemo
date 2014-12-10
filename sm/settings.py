# -*- coding: utf-8 -*-

# Scrapy settings for sm project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sm'

SPIDER_MODULES = ['sm.spiders']
NEWSPIDER_MODULE = 'sm.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sm (+http://www.yourdomain.com)'
import os
SETTING_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(SETTING_DIR, '../')

ITEM_PIPELINES = {
    'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    'sm.pipelines.MongoDBPipeline': 300,
}

IMAGES_STORE = PROJECT_ROOT + 'images/'


import redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0


MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
