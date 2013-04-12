""" Contains ProductHandler class """
from decorators import viewneeded, authenticate
from basehandler import BaseHandler
from utilities import constants
from model import Product
from utilities import to_JSON


class ProductHandler(BaseHandler):

    """ Handling requests for dealing with products """

    @viewneeded
    def get(self, api=None, product_id=None):
        """ GET request handler """
        self.response.headers['Content-Type'] = 'application/json'

        if api is not None:
            self.response.headers['Content-Type'] = 'application/json'

        if product_id is None:
            query = self.request.get('q', '')
            product_list = Product.search(query)
            #json_reponse = to_JSON(product_list)
            self.response.out.write(product_list)
        else:
            pass
