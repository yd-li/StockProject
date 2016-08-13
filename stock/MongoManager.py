import pymongo
from STAPI import STAPI

class MongoManager:

    def __init__(self):
        # self.client = pymongo.MongoClient()
        # self.db = self.client['StockProject']
        # self.collection = self.db['stocktwits']
        # self.documents = self.collection.find()
        self.client = pymongo.MongoClient('mongodb://StockProjectUser:stock@ds153715.mlab.com:53715/heroku_815qc0zx')
        self.db = self.client['heroku_815qc0zx']
        self.collection = self.db['stocktwits']
        self.documents = self.collection.find()

        self.api = STAPI()
        self.cache_size = 30
        self.cache_list = self.get_cache_list()

    def get_from_API(self):
        print 'Calling API: ', self.api.api
        json_obj = self.api.call_api()
        i = 0
        ret = {}
        for message in json_obj['messages']:
            i += 1
            if message['id'] in self.cache_list:
                print i, ' Message %d already exists.' % message['id']
                ret.update({message['id']: 'exists'})
            else:
                self.collection.insert_one(message)
                self.cache_list.append(message['id'])
                print i, ' Message %d inserted.' % message['id']
                ret.update({message['id']: 'inserted'})
        self.cut_cache_list()
        return ret

    def get_cache_list(self):
        latest = self.collection.find(projection={'id':1}).sort('id', pymongo.ASCENDING)
        if latest.count() > self.cache_size:
            latest = latest.skip(self.collection.count() - self.cache_size)
        cache_list = [message['id'] for message in latest]
        if cache_list is None:
            return []
        print len(cache_list)
        return cache_list

    def cut_cache_list(self):
        self.cache_list.sort()
        self.cache_list = self.cache_list[-self.cache_size:]
        print 'cache size', len(self.cache_list)

    def list_all_data(self):
        result = self.collection.find(projection={'_id':0}).sort('id', pymongo.ASCENDING)
        ret = [message for message in result]
        print 'Get %d results' % len(ret)
        return ret


if __name__ == "__main__":
    mongo_manager = MongoManager()
