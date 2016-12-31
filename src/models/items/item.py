import re
import uuid

import requests
from bs4 import BeautifulSoup

from src.common.database import Database
from src.models.stores.store import Store
import src.models.items.constants as item_constants

__author__ = 'glgs'


class Item(object):
    def __init__(self, name, url, price=None, _id=None):
        self.name = name
        self.url = url
        store = Store.get_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        soup = BeautifulSoup(request.content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+\.\d+)")
        match = pattern.search(string_price)
        self.price = float(match.group().replace(".", ""))

        return self.price

    def save_to_db(self):
        Database.insert("items", self.json())

    def update_to_db(self):
        Database.update(item_constants.COLLECTION, {"_id": self._id}, self.json())

    def remove_from_db(self):
        Database.remove(item_constants.COLLECTION, {"_id": self._id})

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(item_constants.COLLECTION, {"_id": item_id}))
