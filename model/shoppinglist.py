""" Contains ShoppingList class """
from google.appengine.ext import db
from google.appengine.api import memcache

from model.listitem import ListItem
from model.product import Product

import logging
import json


class ShoppingList(db.Model):
    """ Model class for ShoppingList """
    name = db.StringProperty()
    items = db.StringProperty()

    NAMESPACE = 'ShoppingList'

    def to_dict(self):
        """ For JSON serialization """
        ret = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
        ret['id'] = self.key().id_or_name()
        ret['items'] = self.items
        return ret

    def add_item(self, description, key, quantity):
        """ Add an item to the list """
        if description is None or description == '':
            raise ValueError(" description not set")
        product = None
        if key is not None:
            product = Product.get_by_id(int(key))
        query = ListItem.all()
        query.ancestor(self)
        item = None
        if product is not None:
            query.filter('product_barcode = ', product.barcode)
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
            if product:
                item.product_barcode = product.barcode
            item.put()
        else:
            item.quantity += quantity
            item.put()
        memcache.delete(str(self.key().id_or_name()), namespace=ShoppingList.NAMESPACE)
        return item

    def get_items(self):
        """ Get all items """
        query = ListItem.all()
        query.ancestor(self)
        list_items = query.fetch(1000)
        ret = []
        if not self.items:
            return list_items
        else:
            ranked_items = json.loads(self.items)
            logging.info('Len: ' + str(len(ranked_items)))
            for ranked_item in ranked_items:
                logging.info('Item: ' + str(ranked_item['id']))
                for real_item in list_items:
                    if ranked_item['id'] == real_item.key().id_or_name():
                        ret.append(real_item)
            for real_item in list_items:
                for ranked_item in ranked_items:
                    if ranked_item['id'] == real_item.key().id_or_name():
                        break
                else:
                    ret.append(real_item)

        return ret

    def delete_item(self, item_id):
        """ Delete given item """
        item = ListItem.get_by_id(int(item_id), self)
        item.delete()
        memcache.delete(str(self.key().id_or_name()), namespace=ShoppingList.NAMESPACE)


    @staticmethod
    def create_list(user, list_name):
        """ Create a new list """
        if list_name is None or list_name == "":
            raise  ValueError("list_name must not be empty error")
        query = ShoppingList.all()
        query.ancestor(user)
        query.filter('name = ', list_name)
        count = query.count()
        if count > 0:
            raise ValueError("a list with the same name already exists: " + str(list_name))
        new_list = ShoppingList(parent=user)
        new_list.name = list_name
        new_list.put()
        return new_list
