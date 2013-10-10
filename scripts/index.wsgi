from cgi import parse_qs, escape
import ConfigParser, os
import qwifiutils

def application(environ, start_response):
	backGroundColor = '003000'
	foreGroundColor = '008000'

	config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])

	timeout = config.getint('main', 'timeout')
	ssid = config.get('main', 'ssid')
	units = config.get('display', 'units')

	html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())

	formString = '<p>Administrative controls</p><form method="post" action="/config/update"><p>SSID Name<input name="ssid" value="'
	formString += ssid
	formString += '" /></p><p>Time until timeout<input name="timeout" value="'
	formString += str(timeout)
	formString += '" /></p><p>Time is in:<br><input type="radio" name = "timeUnit" value = "seconds" checked>Seconds<br><input type = "radio" name = "timeUnit" value = "minutes">Minutes<br><input type = "radio" name = "timeUnit" value = "hours">Hours<br><input type = "radio" name = "timeUnit" value = "days">days</p><input type="submit" />'
	response_body = html % (backGroundColor, foreGroundColor, foreGroundColor, foreGroundColor, formString)

	status = '200 OK'
	response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)

	return [response_body]
