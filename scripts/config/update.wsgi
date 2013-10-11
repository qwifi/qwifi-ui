from cgi import parse_qs, escape
import ConfigParser, os

def application(environ, start_response):
	html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())

	returnMessage = 'Changes Saved!'

	# the environment variable CONTENT_LENGTH may be empty or missing
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0

	# When the method is POST the query string will be sent
	# in the HTTP request body which is passed by the WSGI server
	# in the file like wsgi.input environment variable.
	request_body = environ['wsgi.input'].read(request_body_size)
	d = parse_qs(request_body)

	timeout = d.get('timeout', [''])[0]  # Takes in the form input.
	timeUnit = d.get('timeUnit', [])[0]
	ssid = d.get('ssid', [])[0]

	timeout = int(timeout)

	if timeUnit == 'minutes':  # if else statements determine what the selection for timeUnit was
		timeout = timeout * 60  # multiplies the timeout variable based on what the timeUnit was into seconds
	elif timeUnit == 'hours':
		timeout = timeout * 3600
	elif timeUnit == 'days':
		timeout = timeout * 86400
	else:
		timeout = timeout

	config = ConfigParser.ConfigParser()
	config_path = environ['CONFIGURATION_FILE']

	config.add_section('main')
	config.set('main', 'timeout', timeout)
	config.set('main', 'ssid', ssid)
	config.add_section('display')
	config.set('display', 'units', timeUnit)

	try:
		with open(config_path, 'wb') as config_file:
			config.write(config_file)

	except:
		returnMessage = 'ERROR! Could not save to file!'


	response_body = html % (returnMessage)

	status = '200 OK'
	response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)

	return response_body
