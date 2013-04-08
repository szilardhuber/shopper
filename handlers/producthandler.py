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
            json_reponse = to_JSON(product_list)
            self.response.out.write(json_reponse)
        else:
            pass

    @authenticate
    def put(self, api=None, product_id=None):
        """ PUT request handler """
        if api is not None:
            self.response.out.write('API!<br>')

        if product_id is None:
            self.set_error(constants.STATUS_BAD_REQUEST)
            return
        else:
            pass

    @authenticate
    def post(self, api=None, product_id=None):
        """ POST request handler """
        if api is not None:
            self.response.out.write('API!<br>')

        if product_id is None:
            return
        else:
            pass

    @authenticate
    def delete(self, api=None, product_id=None):
        """ DELETE request handler """
        if api is not None:
            self.response.out.write('API!<br>')

        if product_id is None:
            self.response.out.write("Not supported here.")
            return
        else:
            self.response.out.write("Delete the addressed member of the collection. #")
