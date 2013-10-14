from cgi import parse_qs, escape
import ConfigParser, os
import qwifiutils

def application(environ, start_response):

	config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])#Pulls in the configuration file.

	timeout = config.getint('main', 'timeout')#reads in the data from the configuation file
	ssid = config.get('main', 'ssid')
	units = config.get('display', 'units')

	html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())#reads in the html code to be displayed

	#next 5 lines create the content(forms) to be displayed on the webpage.
	formString = '<p id="adminCtrl">Administrative controls</p><form method="post" action="/config/update"><p id="ssid">SSID Name<input name="ssid" value="'
	formString += ssid
	formString += '" /></p><p id="timeout">Time until timeout<input name="timeout" value="'
	formString += str(timeout)
	formString += '" /></p><p id="timeUnits">Time is in:<br><input type="radio" name = "timeUnit" value = "seconds" checked>Seconds<br><input type = "radio" name = "timeUnit" value = "minutes">Minutes<br><input type = "radio" name = "timeUnit" value = "hours">Hours<br><input type = "radio" name = "timeUnit" value = "days">Days</p><input type="submit" />'
	response_body = html % (formString)

	status = '200 OK'
	response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)

	return [response_body]
