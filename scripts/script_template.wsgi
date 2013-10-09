from cgi import parse_qs, escape

fileLocation = 'c:\config.txt'  # fileReplace

html = (open('C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/base.txt', 'r').read())  # fileReplace


def application(environ, start_response):

	response_body = html % ('')

	status = '200 OK'
	response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)

	return [response_body]