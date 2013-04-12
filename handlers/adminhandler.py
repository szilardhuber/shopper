""" Contains AdminHandler class """
from basehandler import BaseHandler
from utilities import constants
from model import Product
from model import SearchHelper
from utilities import to_JSON
from google.appengine.api import taskqueue
from model import Category
import json
import unicodedata

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

        queue = taskqueue.Queue()
        tasks = []
        for row in rows:
            try:
                count += 1
                items = row.split("|")
                outer_id = items[0]
                name = items[1]
                barcode = items[2]
                category_name = items[3]

                task = taskqueue.Task(url='/admin/worker', params={'outer_id': outer_id, 'name': name, 'barcode': barcode, 'category_name': category_name})
                tasks.append(task)
                if len(tasks) > 99:
                    queue.add(tasks)
                    tasks = []

                #if count > 15:
                #    break
            except IndexError:
                pass
        if len(tasks) > 0:
            queue.add(tasks)
        self.response.out.write(count)


class AdminWorkerHandler(BaseHandler):
    def post(self):
        outer_id = self.request.get('outer_id')
        name = self.request.get('name')
        barcode = self.request.get('barcode')
        category_name = self.request.get('category_name')
        #category = AdminWorkerHandler.create_category(category_name)
        AdminWorkerHandler.create_product(name, outer_id, barcode, category_name)

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
        query.filter('barcode =', barcode)
        ret = query.get()
        if ret is None:
            ret = Product()
            ret.barcode = barcode
            ret.set_name(name)
            ret.category = category
            ret.put()
            AdminWorkerHandler.update_search_table(ret)
        return ret

    @staticmethod
    def update_search_table(product):
        for word in product.name.lower().split(' '):
            #word = unicodedata.normalize('NFKD', unicode(word, 'utf-8')).encode('ASCII', 'ignore')
            word = unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore')
            term = ''
            for char in word:
                term = term + char
                if len(term) < 3:
                    continue
                helper = SearchHelper.get_by_key_name(term)
                ret = []
                if helper is not None:
                    ret = json.loads(helper.items)
                else:
                    helper = SearchHelper(key_name=term)
                ret.append({'id': product.key().id_or_name(), 'name': product.name})
                helper.items = json.dumps(ret)
                helper.put()
