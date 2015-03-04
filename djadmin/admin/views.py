# -*- coding: utf-8 -*-
import json
from bson.objectid import ObjectId
from .rest import Endpoint
from .rest import jsonify
from .rest import APIError

from django.conf import settings


import pymongo
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
connection = pymongo.Connection(MONGO_HOST, MONGO_PORT)
db = connection['crawl']
haha_col = db['blog']

evt_cat_col = connection['crawl']['blog_cat']


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

class PostApi(Endpoint):
    required_fields = {
        'title':'标题',
        'content':'内容',
        }
    
    def _validate(self, data):
        if_exists = {k:bool(data.get(k)) for k in self.required_fields.keys()}
        required = [ item[0] for item in if_exists.items() if not item[1]]
        fields = [self.required_fields[k] for k in required]
        fields.insert(0, '<strong>以下字段必填：</strong>')
        if required:
            raise APIError('<br>'.join(fields))
            
    def _get_one(self, post_id):
        post = haha_col.find_one({'_id':int(post_id)})
        marsh(post)
        return jsonify(post)

    def get_query_args(self, request):
        ''' '''
        query, offset, limit, sort_q = {}, 0, None, []
        try:
            offset =int(request.GET.get('offset', 0))
            limit =int(request.GET.get('limit', 0))
            sort_arg = request.GET.get('_sort', '')
            sort_dir = request.GET.get('_sortDir', '')
            source_cat = request.GET.get('source_cat', '')
            reg_q = request.GET.get('q', '')
            if reg_q:
                import re
                p = re.compile('%s'%reg_q)
                search_q = []
                search_fields = ['title','content','business']
                for f in search_fields:
                    search_q.append({f:p})
                query['$or'] = search_q
            if source_cat: query['source_cat'] = source_cat
            sort_q = []
            if sort_arg:
                sort_dir = 1 if sort_dir=='ASC' else -1
                sort_q.append((sort_arg, sort_dir))
        except:
            import traceback
            traceback.print_exc()
        return query, offset, limit, sort_q

    def _get_list(self, request):
        query, offset, limit, sort_q = self.get_query_args(request)
        posts = haha_col.find(query).skip(offset)
        if sort_q: posts = posts.sort(sort_q)
        if limit: posts = posts.limit(limit)
        posts = list(posts)
        for index, p in enumerate(posts):
            p['index'] = offset+index+1
            p['id'] = str(p['_id'])
            p['_id'] = str(p['_id'])
        total = haha_col.find(query).count()
        data = {'data':posts, 'total':total}
        return jsonify(data)

    def get(self, request, post_id=None):
        if post_id is None:
            return self._get_list(request)
        else:
            return self._get_one(post_id)

    def delete(self, request, post_id):
        result = haha_col.find_and_modify(
                {'_id':int(post_id)},
                {'$set':{'status':-1}},
                full_response=True, new=True
                )
        post = result['value']
        if not post:
            raise
        return jsonify(post)

    def post(self, request):
        data = request.data
        self._validate(data)
        #convert_int(data, 'cat')
        data['_id'] = get_next_seq('blog')+100
        haha_col.insert(
            data,
            safe=True
            )
        marsh(data)
        return jsonify(data)

    def put(self, request, post_id):
        data = request.data;
        print data
        self._validate(data)
        print type(data[u'id']), type(post_id)
        print data[u'id'], post_id
        print data[u'id']==post_id
        if data[u'id']!=post_id:
            raise
        convert_int(data, u'id')
        result = haha_col.find_and_modify(
                {'_id':int(post_id)},
                {'$set':data},
                full_response=True, new=True
                )
        post = result['value']
        if not post:
            raise
        marsh(post)
        return jsonify(post)

import re
regex_rn = ur'\n'
pattern_rn = re.compile(regex_rn, re.UNICODE | re.DOTALL | re.IGNORECASE)
def rn2br(text):
    return pattern_rn.sub('<br>', text)

def fix_item(item, key):
    if item.get(key):
        item[key] = rn2br(item[key])

def marsh(item):
    ''' no need return '''
    #fix_item(item, 'content')
    item['id'] = str(item.pop('_id'))

def convert_int(item, field):
    item[field] = int(item[field])

from django.http import HttpResponse
from django.utils import simplejson
def tag_list(request):
    tags = [{"id":1,"name":"室内","published":1},{"id":2,"name":"室外","published":False}]
    tags = list(evt_cat_col.find());
    filter(marsh, tags)
    data = {'data':tags,'total':2}
    return jsonify(data)


def tag_detail(request, tag_id):
    evt_cat = evt_cat_col.find_one({'_id': int(tag_id)})
    marsh(evt_cat)
    return jsonify(evt_cat)


from django.shortcuts import render
def index_view(request):
    ''' '''
    template_name = 'index.html'
    return render(request, template_name, {})
