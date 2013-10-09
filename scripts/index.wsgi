from cgi import parse_qs, escape

def application(environ, start_response):
	fileLocation = environ['CONFIGURATION_FILE']
	html = (open(environ['TEMPLATE_BASE'] + '/base', 'r').read())

	backGroundColor = '003000'
	foreGroundColor = '008000'
	try:
		configFile = open(fileLocation, 'r')
		pastTimeout = configFile.readline().rstrip()
		pastTimeout = pastTimeout.replace('Timeout=', '')
		pastTimeUnit = configFile.readline().rstrip()
		pastTimeUnit = pastTimeUnit.replace('TimeUnit=', '')
		pastSsidName = configFile.readline().rstrip()
		pastSsidName = pastSsidName.replace('SSIDName=', '')
		pastSsidName = pastSsidName.replace("'", '')
		pastSsidName = pastSsidName.replace('[', '')
		pastSsidName = pastSsidName.replace(']', '')
		configFile.close()
	except:
		configFile = open(fileLocation, 'w')
		configFile.write('Timeout=')
		configFile.write('8000\n')
		configFile.write('TimeUnit=')
		configFile.write('seconds\n')
		configFile.write('SSIDName=')
		configFile.write('standard')
		configFile.close()
		pastSsidName = 'standard'
		pastTimeout = 8000
		pastTimeUnit = 'seconds'

	formString = '<p>Administrative controls</p><form method="post" action="update"><p>SSID Name<input name="ssidName" value="'
	formString += str(pastSsidName)
	formString += '" /></p><p>Time until timeout<input name="timeout" value="'
	formString += str(pastTimeout)
	formString += '" /></p><p>Time is in:<br><input type="radio" name = "timeUnit" value = "seconds" checked>Seconds<br><input type = "radio" name = "timeUnit" value = "minutes">Minutes<br><input type = "radio" name = "timeUnit" value = "hours">Hours<br><input type = "radio" name = "timeUnit" value = "days">days</p><input type="submit" />'
	response_body = html % (backGroundColor, foreGroundColor, foreGroundColor, foreGroundColor, formString)

	status = '200 OK'
	response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
	start_response(status, response_headers)

	return [response_body]