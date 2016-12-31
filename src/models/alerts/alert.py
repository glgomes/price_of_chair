import uuid

import datetime
import requests
import src.config as config

import src.models.alerts.constants as alert_constants
from src.common.database import Database
from src.models.items.item import Item

__author__ = 'glgs'


class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        super(Alert, self).__init__()
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self.active = active
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        return requests.post(
            alert_constants.URL,
            auth=("api", alert_constants.API_KEY),
            data={
                "from": alert_constants.FROM,
                "to": self.user_email,
                "subject": "The item {} has reached a good price!".format(self.item.name),
                "text": "Hi there!\n\nThe item {} has reached a price below ${}.\n\n{}\n\n"
                        "Alert page:\n\n{}".format(self.item.name,
                                                   self.price_limit,
                                                   self.item.url,
                                                   "http://{}/alerts/{}".format(config.DOMAIN, self._id))
            }
        )

    @classmethod
    def find_needing_update(cls, minutes_since_update=alert_constants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**item) for item in Database.find(alert_constants.COLLECTION,
                                                      {"last_checked": {"$lte": last_updated_limit},
                                                       "active": True})]

    def save_to_db(self):
        Database.insert("alerts", self.json())

    def update_to_db(self):
        Database.update(alert_constants.COLLECTION, {"_id": self._id}, self.json())

    def remove_from_db(self):
        Database.remove(alert_constants.COLLECTION, {"_id": self._id})

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "active" : self.active,
            "item_id": self.item._id
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.update_to_db()
        self.update_to_db()
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price <= self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(alert_constants.COLLECTION, {"user_email": user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(alert_constants.COLLECTION, {"_id": alert_id}))

    def deactivate(self):
        self.active = False
        self.update_to_db()

    def activate(self):
        self.active = True
        self.update_to_db()