import threading

class APIView():    
    instance = None
    instance_lock = threading.Lock()
    
    @staticmethod
    def get_instance():
        with APIView.instance_lock:
            if APIView.instance is None:
                APIView.instance = APIView()
        return APIView.instance
    
    def display_error(self, baseHandler, error, message=None, url=None):
        baseHandler.error(error)
        
    def ok(self, baseHandler, url=None):
        pass
