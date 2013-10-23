import ConfigParser, os
import qwifiutils

def application(environ, start_response):
    html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())#reads in HTML
    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])#Pulls in the configuration file.

    ssid = config.get('main', 'ssid')

    #SSID
    formString = '<div class="configItem">SSID Name<input name="ssid" value="%s" /></div>\n' % ssid
    formString += '<form method="post" action="/config/ap/update">\n'
    formString += '<input type="submit" value="Apply" />'

    response_body = html % (formString)#adds the cmntent to the html
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return response_body #sends the html to the user's web browser.
