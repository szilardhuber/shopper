""" Contains ProductHandler class """
from handlers.decorators import viewneeded
from handlers.basehandler import BaseHandler
from model import Product


class ProductHandler(BaseHandler):

    """ Handling requests for dealing with products """

    @viewneeded
    def get(self, api=None, product_id=None):
        """ GET request handler """
        self.response.headers['Content-Type'] = 'application/json'
        # TODO !!!!!! REMOVE ON RELEASE !!!!!!!!!!
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        # TODO !!!!!! REMOVE ON RELEASE !!!!!!!!!!

        if api is not None:
            return

        if product_id is None:
            query = self.request.get('q', '')
            product_list = Product.search(query)
            self.response.out.write(product_list)
        else:
            pass
