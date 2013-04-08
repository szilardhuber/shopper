""" Contains ShoppingList class """
from google.appengine.ext import db
from google.appengine.api import memcache

from model.listitem import ListItem
from model.product import Product

import logging


class ShoppingList(db.Model):
    """ Model class for ShoppingList """
    name = db.StringProperty()

    NAMESPACE = 'ShoppingList'

    def to_dict(self):
        """ For JSON serialization """
        ret = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
        ret['id'] = self.key().id_or_name()
        return ret

    def add_item(self, description, quantity):
        """ Add an item to the list """
        query = Product.all()
        query.filter('name = ', description)
        product = query.get()
        query = ListItem.all()
        query.ancestor(self)
        item = None
        if product is not None:
            query.filter('product = ', product)
            item = query.get()
            logging.info('Product: ' + str(product))
            logging.info('Item: ' + str(item))
        else:
            query.filter('description = ', description)
            item = query.get()

        if item is None:
            item = ListItem(parent=self)
            item.description = description
            item.quantity = quantity
            item.product = product
            item.put()
        else:
            item.quantity += quantity
            item.put()
        memcache.delete(str(self.key().id_or_name()), namespace=ShoppingList.NAMESPACE)

    def get_items(self):
        """ Get all items """
        list_items = memcache.get(str(self.key().id_or_name()), namespace=ShoppingList.NAMESPACE)
        if list_items is not None:
            return list_items
        query = ListItem.all()
        query.ancestor(self)
        list_items = query.fetch(1000)
        memcache.add(str(self.key().id_or_name()), list_items, namespace=ShoppingList.NAMESPACE)
        return list_items

    @staticmethod
    def create_list(user, list_name):
        """ Create a new list """
        query = ShoppingList.all()
        query.ancestor(user)
        query.filter('name = ', list_name)
        count = query.count()
        if count > 0:
            return None
        new_list = ShoppingList(parent=user)
        new_list.name = list_name
        new_list.put()
        return new_list
