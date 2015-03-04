# -*- coding: utf-8 -*-
import pymongo
import scrapy
import time
from sm.db import REDIS_SERVER
from sm.db import connection
from sm.utils import hash_item_fields


item_hash_key_set_name = 'duplicate_check_sign_set'

incr_id_col = connection['crawl']['blog_id']
def get_next_seq(name):
    result = incr_id_col.find_and_modify(
        {'_id':name},
        {'$inc':{'seq':1}},
        upsert=True,
        new=True,
        full_response=True
        )
    print result
    return result['value']['seq']

def get_id_query(item):
    ''' '''
    return {'link':item['link']}

class MongoDBPipeline(object):
    def __init__(self):
        self.db = connection['crawl']

    def save_or_update(self, collection, item, spider):
        try:
            current_time = int(time.time())
            source_cat = self.get_cat_name(item)
            item = dict(item)
            item_key = hash_item_fields(item)
            exists = REDIS_SERVER.sismember(item_hash_key_set_name, item_key)
            print exists
            if exists: raise scrapy.exceptions.DropItem()
            item['update_time'] = current_time
            item['duplicate_check_sign'] = item_key
            item['add_time'] = current_time
            item['status'] = -10
            item['source_cat'] = source_cat
            item['_id'] = get_next_seq('blog')+100
            id = collection.insert(item, safe=True)
            REDIS_SERVER.sadd(item_hash_key_set_name, item_key)
        except pymongo.errors.DuplicateKeyError as e:
            item.pop('_id', None)
            print 'dul'
            item.pop('create_time')
            item['has_update'] = 1
            collection.update(get_id_query(item), {'$set':{'has_update':1}}, safe=True)
            REDIS_SERVER.sadd(item_hash_key_set_name, item_key)

    def find_and_modify(self, col_name, query, item, upsert=True, full_response=True):
        ''' '''
        col = self.get_collection(col_name)
        col.find_and_modify(
            query,
            {'$set':item},
            upsert=upsert,
            full_response=full_response,
            new=True
            )
        
    def get_collection(self, name):
        return self.db[name]

    def get_cat_name(self, item):
        item_type = type(item)
        col_name = item_type._collection_name
        return col_name

    def process_item(self, item, spider):
        col = self.get_collection('blog')
        self.save_or_update(col, item, spider)
        return item
