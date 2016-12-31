import uuid

from src.common.database import Database
import src.models.stores.errors as store_errors
import src.models.stores.constants as store_constants

__author__ = 'glgs'


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def save_to_db(self):
        Database.insert("stores", self.json())

    def update_to_db(self):
        Database.update(store_constants.COLLECTION, {"_id": self._id}, self.json())

    def remove_from_db(self):
        Database.remove(store_constants.COLLECTION, {"_id": self._id})

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one("stores", {"_id": id}))

    @classmethod
    def get_by_name(cls, name):
        return cls(**Database.find_one("stores", {"name": name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return cls(**Database.find_one("stores", {"url_prefix": url_prefix}))

    @classmethod
    def get_by_url(cls, url):
        for i in range(len(url)):
            try:
                store = cls.get_by_url_prefix(url[:-i])
                return store
            except:
                continue
        raise store_errors.StoreNotFoundException("URL prefix returned nothing")

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(store_constants.COLLECTION, {})]
