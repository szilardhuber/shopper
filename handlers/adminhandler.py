""" Contains AdminHandler class """
from basehandler import BaseHandler
from utilities import constants
from model import Product
from utilities import to_JSON
from google.appengine.api import taskqueue

from model import Category

class AdminHandler(BaseHandler):

    """ Handling requests for dealing with products """

    def get(self):
        """ GET request handler """
        template = self.jinja2_env.get_template('admin.html')
        self.response.out.write(template.render({}))

    def post(self):
        product_raw_data = self.request.get('productlist')
        if product_raw_data is None:
            return
        count = 0
        raw_data_string = unicode(product_raw_data, 'iso-8859-1')
        rows = raw_data_string.split("\n")

        for row in rows:
            try:
                count += 1
                items = row.split("|")
                outer_id = items[0]
                name = items[1]
                barcode = items[2]
                category_name = items[3]

                taskqueue.add(url='/admin/worker', params={'outer_id': outer_id, 'name': name, 'barcode': barcode, 'category_name':category_name})
                #if count > 15:
                #    break
            except IndexError:
                pass
        self.response.out.write(count)


class AdminWorkerHandler(BaseHandler):
    def post(self):
        outer_id = self.request.get('outer_id')
        name = self.request.get('name')
        barcode = self.request.get('barcode')
        category_name = self.request.get('category_name')
        category = AdminWorkerHandler.create_category(category_name)
        AdminWorkerHandler.create_product(name, outer_id, barcode, category)

    @staticmethod
    def create_category(category_name):
        query = Category.all()
        query.filter('description =', category_name)
        ret = query.get()
        if ret is None:
            ret = Category()
            ret.description = category_name
            ret.put()
        return ret

    @staticmethod
    def create_product(name, outer_id, barcode, category):
        query = Product.all()
        query.filter('name=', name)
        ret = query.get()
        if ret is None:
            ret = Product()
            ret.barcode = barcode
            ret.set_name(name)
            ret.category = category
            ret.outer_id = outer_id
            ret.put()
        return ret


