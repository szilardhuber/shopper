""" Contains ListHandler Class """
import logging
import json

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
            self._display_list(list_id)

    @viewneeded
    @authenticate
    def post(self, api=None, list_id=None):
        """ POST request handler """
        current_user = User.getUser(self.user_email)
        if api is not None:
            try:
                if list_id is None:
                    list_name = self.request.get('name', None)
                    new_list = ShoppingList.create_list(current_user, list_name)
                    self._api_display_list_(new_list)
            except (ValueError) as exc:
                self.set_error(constants.STATUS_BAD_REQUEST)

        if list_id is not None:
            # Add item to list
            try:
                current_list = ShoppingList.get_by_id(int(list_id),
                                                      current_user)
                if current_list is None:
                    raise ValueError

                item = current_list.add_item(self.request.get('description', None),
                                      self.request.get('key', None),
                                      int(self.request.get('quantity', 1)))
                self.response.out.write(json.dumps(item.to_dict()))
                self.response.headers['Content-Type'] = 'application/json'
                self.ok('/Lists/'+str(list_id))

            except (TypeError,
                    ValueError,
                    BadKeyError,
                    BadValueError,
                    ProtocolBufferEncodeError) as exc:
                logging.error('Exception: ' + str(exc))
                error_message = self.gettext("There's not such list, sorry.")
                self.set_error(constants.STATUS_BAD_REQUEST,
                               message=error_message,
                               url="/")

    @viewneeded
    @authenticate
    def delete(self, api=None, list_id=None, item_id=None):
        """ DELETE request handler """
        if api is not None:
            try:
                current_user = User.getUser(self.user_email)
                current_list = ShoppingList.get_by_id(int(list_id),
                                                      current_user)
                current_list.delete_item(item_id)
            except (TypeError,
                    ValueError,
                    BadKeyError,
                    BadValueError,
                    ProtocolBufferEncodeError) as exc:
                logging.error('Exception: ' + str(exc))
                error_message = self.gettext("There's no such item, sorry.")
                self.set_error(constants.STATUS_BAD_REQUEST,
                               message=error_message,
                               url="/")

    @authenticate
    def put(self, api, list_id):
        """ PUT method is used to change item rankings """
        try:
            current_user = User.getUser(self.user_email)
            current_list = ShoppingList.get_by_id(int(list_id), current_user)
            items_json = self.request.get('items')
            self.response.out.write('Items json: ' + str(items_json)+ '\n')
            items_check = json.loads(items_json)
            current_list.items = items_json
            current_list.put()
            self.response.out.write('Ran with success')
        except (BadValueError, AttributeError) as exc:
            logging.error('Exception: ' + str(exc))
            error_message = self.gettext('Error while storing new order.')
            self.set_error(constants.STATUS_BAD_REQUEST,
                            message=error_message,
                            url="/")


#Private methods
    def _list_lists(self, api):
        """ Lists all shopping lists of current user """
        current_user = User.getUser(self.user_email)
        query = ShoppingList.all()
        query.ancestor(current_user)

        if api is not None:
            all_lists = query.run()
            self._api_list_lists_(all_lists)
        else:
            template = self.jinja2_env.get_template('ang-base.html')
            template_values = {
                'user_email': self.user_email
            }
            self.response.out.write(template.render(template_values))

    def _api_list_lists_(self, all_lists):
        """ Lists all shopping lists as JSON """
        self.response.headers['Content-Type'] = 'application/json'
        response_json = to_JSON(all_lists)
        self.response.out.write(response_json)

    def _display_list(self, list_id):
        """ Displays the list with the given id
            if it belongs to the current user """
        try:
            current_user = User.getUser(self.user_email)
            current_list = ShoppingList.get_by_id(int(list_id), current_user)
            if current_list is None:
                raise ValueError
            self._api_display_list_(current_list)
        except (TypeError, ValueError, ProtocolBufferEncodeError) as exc:
            logging.error(str(exc))
            error_message = self.gettext("There's not such list, sorry.")
            self.set_error(constants.STATUS_BAD_REQUEST,
                           message=error_message, url="/")

    def _api_display_list_(self, list_to_display):
        """ Displays list with the given id in JSON format """
        self.response.headers['Content-Type'] = 'application/json'
        items = list_to_display.get_items()
        if len(items) > 0:
            list_to_display.items = to_JSON(items)
        response = json.dumps(list_to_display.to_dict())
        self.response.out.write(response)
