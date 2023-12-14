#!/usr/bin/python3
import sys 
import logging
logging.basicConfig(filename='/var/www/webapp/webapp/rgbapp.log', filemode='w', format='%(asctime)s - %(levelname)s -%(message)s', level=logging.INFO)
sys.path.insert(0, "/var/www/webapp/")
from webapp import app as application
application.secret_key = '1433'

class LoggingMiddleware:
	def __init__(self, app):
		self.app = app
		
	def __call__(self, environ, start_response):
		request_ip = environ.get('HTTP_X_REAL_IP', environ.get('REMOTE_ADDR'))
		
		log_message = 'IP: %s - Request: %s %s' % (request_ip, environ['REQUEST_METHOD'], environ['PATH_INFO'])
		#logging.info('IP: %s', request_ip)
		logging.info(log_message)
		
		return self.app(environ, start_response)
		
application.wsgi_app = LoggingMiddleware(application.wsgi_app)
