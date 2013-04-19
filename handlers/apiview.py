""" Contains APIView class """
import threading


class APIView():
    """ No redirect handling """
    instance = None
    instance_lock = threading.Lock()

    @staticmethod
    def get_instance():
        """ Singleton Pattern """
        with APIView.instance_lock:
            if APIView.instance is None:
                APIView.instance = APIView()
        return APIView.instance

    def display_error(self, base_handler, error, message=None, url=None):
        """ Display an error to the handled output """
        base_handler.error(error)

    def ok(self, base_handler, url=None):
        """ Nothing to do here """
        import logging
        logging.info('APIView ok called')
        base_handler.response.status_int = 200
