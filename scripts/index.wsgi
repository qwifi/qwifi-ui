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
    # Pulls in the configuration file.
    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])

    # Reads in the html code to be displayed
    html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())

    error_string = ''
    try:
	# Reads in the timeout from the configuation file
        timeout = config.getint('session', 'timeout')
    except ValueError:
        error_string = '<p class="error">Unable to read timeout from configuration file.</p>'
	error_string +='<p class="error">Using default value of 10.</p><br>'
	timeout = 10

    units = config.get('display', 'units')
    if units != 'seconds' and units != 'minutes' and units != 'hours' and units != 'days':
        error_string +='<p class="error">Unable to read timeout units from configuration file.</p>'
	error_string +='<p class="error">Using default value of seconds</p><br>'
	units = 'seconds'

    # Next 5 lines create the content(forms) to be displayed on the webpage.
    form_string = '<h1>Administrative Controls</h1>\n'
    form_string += error_string
    form_string += '<form class="sessionsForm" method="post" action="/config/update">\n'
    form_string += '<div class="configItem">Session timeout: <input id="timeout" type="number" name="timeout" value="%s" required />\n' % str(timeout / time_unit_multipliers.get(units, 1))
    # Ref: http://stackoverflow.com/a/10096033/577298
    form_string += '<select name="timeUnit" autocomplete="off">%s</select>' % generate_timeout_units(units) 
    form_string += '</div>\n'
    form_string += '<input type="submit" value="Apply" />'
	

    # Adds the content to the html
    response_body = html % {'returnMessage':form_string}

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    # sends the html to the user's web browser.
    return response_body
