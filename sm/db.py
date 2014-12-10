import pymongo

from sm.settings import *


connection = pymongo.Connection(MONGO_HOST, MONGO_PORT)

REDIS_SERVER = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
