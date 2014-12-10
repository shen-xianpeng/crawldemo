# -*- coding: utf-8 -*-
import os

import json
from bson.objectid import ObjectId

from flask import Flask, request
from flask import jsonify
from flask import render_template
from flask import send_from_directory
SETTING_DIR = os.path.abspath(os.path.dirname(__file__))
import pymongo

import redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0


MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
connection = pymongo.Connection(MONGO_HOST, MONGO_PORT)

app = Flask(__name__)

db = connection['mmbspiders']
haha_col = db['events']

@app.route('/')
def index_view():
    ''' '''
    return render_template('index.html')

@app.route('/bootstrap-sass-official/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    print os.path.join(SETTING_DIR,'static', path)
    return send_from_directory(os.path.join(SETTING_DIR,'static'), path)

@app.route('/assets/<path:path>')
def assets_proxy(path):
    # send_static_file will guess the correct MIME type
    return send_from_directory(os.path.join(SETTING_DIR,'static/assets'), path)

from flask.views import MethodView

class PostApi(MethodView):

    def _get_one(self, post_id):
        post = haha_col.find_one({'_id':ObjectId(post_id)})
        post['id'] = str(post.pop('_id'))
        return json.dumps(post)
    
    def get_query_args(self):
        ''' '''
        query, offset, limit, sort_q = {}, 0, None, []
        try:
            offset =int(request.args.get('offset', 0))
            limit =int(request.args.get('limit', 0))
            sort_arg = request.args.get('_sort', '')
            sort_dir = request.args.get('_sortDir', '')
            source_cat = request.args.get('source_cat', '')
            reg_q = request.args.get('q', '')
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

    def _get_list(self):
        query, offset, limit, sort_q = self.get_query_args()
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
        return json.dumps(data)

    def get(self, post_id):
        if post_id is None:
            return self._get_list()
        else:
            return self._get_one(post_id)

    def delete(self, post_id):
        post = haha_col.find_one({'_id':ObjectId(post_id)})
        post['id'] = str(post.pop('_id'))
        return json.dumps(post)

    def post(self):
        data = request.get_json()
        haha_col.insert(
            data,
            safe=True
            )
        marsh(data)
        return json.dumps(data)

    def put(self, post_id):
        data = request.get_json()
        if data.pop('id')!=post_id:
            raise
        result = haha_col.find_and_modify(
                {'_id':ObjectId(post_id)},
                {'$set':data},
                full_response=True, new=True
                )
        post = result['value']
        if not post:
            raise
        marsh(post)
        return json.dumps(post)

post_view = PostApi.as_view('post_api')
app.add_url_rule(
    '/posts/',
    defaults={'post_id': None},
    view_func=post_view, methods=['GET',])
app.add_url_rule(
    '/posts',
    view_func=post_view, methods=['POST',])
app.add_url_rule(
    '/posts/<string:post_id>',
    view_func=post_view,
    methods=['GET', 'PUT', 'DELETE'])


def marsh(item):
    ''' no need return '''
    item['id'] = str(item.pop('_id'))

@app.route('/tags')
def tags():
    tags = [{"id":1,"name":"室内","published":1},{"id":2,"name":"室外","published":False}]
    data = {'data':tags,'total':2}
    return  json.dumps(data)


@app.route('/tags/<string:tag_id>')
def tag(tag_id):
    tags = [{"id":1,"name":"室内","published":1},{"id":2,"name":"室外","published":False}]
    data = {'data':tags,'total':2}
    return json.dumps(tags[int(tag_id)-1])
    return  json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
