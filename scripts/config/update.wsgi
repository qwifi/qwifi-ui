from cgi import parse_qs, escape
import ConfigParser, os

def application(environ, start_response):
	html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())  # reads in HTML

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

	timeout = d.get('timeout', ['10'])[0]  # Takes in the form input. All the form inputs
	timeUnit = d.get('timeUnit', ['seconds'])[0]
        
        
        if timeout.isdigit():
	        timeout = int(timeout)  # converts timeout to integer for math operations.

        	if timeUnit == 'minutes':  # if else statements determine what the selection for timeUnit was
        		timeout = timeout * 60  # multiplies the timeout variable based on what the timeUnit was into seconds
        	elif timeUnit == 'hours':
        		timeout = timeout * 3600
        	elif timeUnit == 'days':
        		timeout = timeout * 86400
        	else:
	        	timeout = timeout

	        result_message = '<p class="success">Changes saved.</p>'

                config = ConfigParser.ConfigParser()
                config_path = environ['CONFIGURATION_FILE']

                config.add_section('main')
                config.set('main', 'timeout', timeout)
                config.add_section('display')
                config.set('display', 'units', timeUnit)

                result_message = '<p class="error">Default message (this is a bug)</p>'
                
                try:  # tries to save to the config file
                        with open(config_path, 'wb') as config_file:
                                config.write(config_file)

                        result_message = '<table class="config">'
                        result_message += '<tr><td>%s</td><td>%s</td></tr>' % ('Timeout (in seconds):', timeout)
                        result_message += '<tr><td>%s</td><td>%s</td></tr>' % ('Time Units:', timeUnit)
                        result_message += '</table>'
                        result_message += '<p class="success">Changes saved.</p>'

                except IOError:
                        result_message = '<p class="error">Could not save to file.</p>'  # changes the returned message if unable to save to the config file

        else:
                result_message = '<p> Error, the timeout specific was not the correct format</p>'

	response_body = html % (result_message)

	status = '200 OK'
	response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)

	return response_body  # sends the html to the user's web browser.
