import ConfigParser, os
import qwifiutils

def application(environ, start_response):
    ssid = qwifiutils.get_ssid(environ['HOSTAPD_CONF'])

    formString = '<form method="post" class="apForm" action="/config/ap/update">\n'
    formString += '<div class="configItem">SSID Name<input name="ssid" value="%s" pattern ="[A-Za-z]+[0-9]*" title="Must start with a letter. Can end with numbers." required /></div>\n' % ssid
    formString += '<input type="submit" value="Apply" />'

    html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())#reads in HTML
    response_body = html % {'returnMessage':formString}#adds the cmntent to the html
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return response_body #sends the html to the user's web browser.
