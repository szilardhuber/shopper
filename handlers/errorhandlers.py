""" Nice error handler functions """
import logging


def handle_404(_, response, exception):
    """ Handle NOT FOUND error """
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)


def handle_500(_, response, exception):
    """ Handle SERVER ERROR """
    logging.exception(exception)
    response.write("Leave me alone. I know what I'm doing")
    response.set_status(500)


def set_handlers(app):
    """ Set the error handlers """
    app.error_handlers[404] = handle_404
    app.error_handlers[500] = handle_500
