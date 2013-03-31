import logging

def handle_404(request, response, exception):
	logging.exception(exception)
	response.write('Oops! I could swear this page was here!')
	response.set_status(404)

def handle_500(request, response, exception):
	logging.exception(exception)
	response.write("Leave me alone. I know what I'm doing")
	response.set_status(500)

def set_handlers(app):
	app.error_handlers[404] = handle_404
	app.error_handlers[500] = handle_500