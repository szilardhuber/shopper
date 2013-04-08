""" Contains ListHandler Class """
import logging

from handlers.basehandler import BaseHandler
from model import ShoppingList, User
from utilities import constants, to_JSON
from handlers.decorators import authenticate, viewneeded
from google.net.proto.ProtocolBuffer import ProtocolBufferEncodeError
from google.appengine.api.datastore_errors import BadKeyError
from google.appengine.ext.db import BadValueError

class ListHandler(BaseHandler):
    """ Handling requests for dealing with shopping lists """
#Public methods
    @viewneeded
    @authenticate
    def get(self, api=None, list_id=None):
        """ get request handler """
        if list_id is None:
            self._list_lists(api)
        else:
            self._display_list(list_id, api)

    @viewneeded
    @authenticate
    def post(self, api=None, list_id=None):
        """ POST request handler """
        current_user = User.getUser(self.user_email)
        if api is not None:
            if list_id is None:
                list_name = self.request.get('name', None)
                if list_name is None or list_name == '':
                    self.set_error(constants.STATUS_BAD_REQUEST)
                    return
                new_list = ShoppingList.create_list(current_user, list_name)
                if new_list is None:
                    self.set_error(constants.STATUS_BAD_REQUEST)
                    return
                self._api_display_list_(new_list)

        if list_id is not None:
            # Add item to list
            try:
                current_list = ShoppingList.get_by_id(
                    int(list_id), current_user)
                if current_list is None:
                    raise ValueError

                current_list.add_item(self.request.get('description', None), int(self.request.get('quantity', 1)))
                self.ok('/Lists/'+str(list_id))

            except (TypeError, ValueError, BadKeyError, BadValueError) as exc:
                logging.error('Exception: ' + str(exc))
                self.set_error(constants.STATUS_BAD_REQUEST, message=self.gettext("There's not such list, sorry."), url="/")

#Private methods
    def _create_list_(self, list_name):
        """ Creates a new list with the given name """
        current_user = User.getUser(self.user_email)
        new_list = ShoppingList(parent=current_user)
        new_list.name = list_name
        new_list.put()
        return new_list

    def _list_lists(self, api):
        """ Lists all shopping lists of current user """
        current_user = User.getUser(self.user_email)
        query = ShoppingList.all()
        query.ancestor(current_user)

        if api is not None:
            all_lists = query.run()
            self._api_list_lists_(all_lists)
        else:
            # get first list
            first_list = query.get()
            if first_list is None:
                first_list = self._create_list_('Shopping list')

            # navigate to it
            newurl = '/Lists/' + str(first_list.key().id_or_name())
            self.redirect(newurl)

    def _api_list_lists_(self, all_lists):
        """ Lists all shopping lists as JSON """
        self.response.headers['Content-Type'] = 'application/json'
        response_json = to_JSON(all_lists)
        self.response.out.write(response_json)

    def _display_list(self, list_id, api):
        """ Displays the list with the given id if it belongs to the current user """
        try:
            current_user = User.getUser(self.user_email)
            current_list = ShoppingList.get_by_id(int(list_id), current_user)
            if current_list is None:
                raise ValueError

            if api is not None:
                self._api_display_list_(current_list)
            else:
                self._web_display_list_(current_list)
        except (TypeError, ValueError, ProtocolBufferEncodeError) as exc:  # filtering all non-integers in parameter
            logging.error(str(exc))
            self.set_error(constants.STATUS_BAD_REQUEST, message=self.gettext("There's not such list, sorry."), url="/")

    def _api_display_list_(self, list_to_display):
        """ Displays list with the given id in JSON format """
        self.response.headers['Content-Type'] = 'application/json'
        response_json = to_JSON(list_to_display.get_items())
        self.response.out.write(response_json)

    def _web_display_list_(self, list_to_display):
        """ Renders the website containing the list items of the list with the given id """
        list_items = list_to_display.get_items()
        list_id = list_to_display.key().id_or_name()
        template = self.jinja2_env.get_template('shoppinglist.html')
        template_values = {
            'user_email': self.user_email,
            'shopping_list': list_to_display,
            'list_id': list_id,
            'list_items': list_items
        }
        self.response.out.write(template.render(template_values))
