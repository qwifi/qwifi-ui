from cgi import parse_qs, escape
import ConfigParser, os

def legal_ssid(test_ssid):
        valid = True
        #Check if it is a complete number
        if test_ssid.isdigit():
                valid = False
        #Don't allow SSID to start with a digit
        elif test_ssid[0].isdigit():
                valid = False
        #Test if SSID contains a space
        elif ' ' in test_ssid:
                valid = False
        #Test if SSID is a decimal number(isdigit wont catch it)
        else:
                try:
                        temp = float(test_ssid)
                except:
                        valid = True

        return valid


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
        
	ssid = d.get('ssid', [''])[0]  # Takes in the form input. All the form inputs

        if not legal_ssid(ssid):
                result_message = '<p> Error, the SSID given was not in the correct format </p>'
        else:
                result_message = '<p class="error">Default message (this is a bug)</p>'
                result_message = '<table class="config">'
                result_message += '<tr><td>%s</td><td>%s</td></tr>' % ('SSID: ', ssid)
                result_message += '</table>'
                result_message += '<p class="success">Changes saved.</p>'


	response_body = html % (result_message)

	status = '200 OK'
	response_headers = [('Content-Type', 'text/html'), 
                            ('Content-Length', str(len(response_body)))]

	start_response(status, response_headers)

	return response_body  # sends the html to the user's web browser.
