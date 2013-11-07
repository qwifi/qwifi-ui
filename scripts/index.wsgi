from cgi import parse_qs, escape
import ConfigParser
import os
import qwifiutils

time_unit_multipliers = { 'minutes': 60, 'hours': 3600, 'days': 86400 }

def generate_timeout_units(units):
    result = '<option value="seconds">Seconds</option><option value="minutes">Minutes</option><option value="hours">Hours</option><option value="days">Days</option>'

    if units.lower() == 'minutes':
        result = result.replace('value="minutes"', 'value="minutes" selected')
    elif units.lower() == 'hours':
        result = result.replace('value="hours"', 'value="hours" selected')
    elif units.lower() == 'days':
        result = result.replace('value="days"', 'value="days" selected')

    return result

def application(environ, start_response):
    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])#Pulls in the configuration file.
    html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())#reads in the html code to be displayed

    errorString = ''
    try:
        timeout = config.getint('session', 'timeout')#reads in the data from the configuation file
    except ValueError:
        errorString = '<p class="error">Unable to read timeout from configuration file.</p>'
	errorString +='<p class="error">Using default value of 10.</p><br>'
	timeout = 10

    units = config.get('display', 'units')
    if units != 'seconds' and units != 'minutes' and units != 'hours' and units != 'days':
        errorString +='<p class="error">Unable to read timeout units from configuration file.</p>'
	errorString +='<p class="error">Using default value of seconds</p><br>'
	units = 'seconds'

    #next 5 lines create the content(forms) to be displayed on the webpage.
    formString = '<h1>Administrative Controls</h1>\n'
    formString += errorString
    formString += '<form class="sessionsForm" method="post" action="/config/update">\n'
    #timeout
    formString += '<div class="configItem">Session timeout: <input id="timeout" type="number" name="timeout" value="%s" required />\n' % str(timeout / time_unit_multipliers.get(units, 1))
    formString += '<select name="timeUnit" autocomplete="off">%s</select>' % generate_timeout_units(units) #ref: http://stackoverflow.com/a/10096033/577298
    formString += '</div>\n'
    formString += '<input type="submit" value="Apply" />'
	

    response_body = html % {'returnMessage':formString}#adds the content to the html

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return response_body#sends the html to the user's web browser.
