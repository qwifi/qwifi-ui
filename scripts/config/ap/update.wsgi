from cgi import parse_qs, escape
import ConfigParser
import os
import re
import shutil
import subprocess

def legal_ssid(test_ssid):
    valid = True
    # Check if it is a complete number
    if test_ssid.isdigit():
        valid = False
    # Don't allow SSID to start with a digit
    elif test_ssid[0].isdigit():
        valid = False
    # Test if SSID contains a space
    elif ' ' in test_ssid:
        valid = False
    # Test if SSID is a decimal number(isdigit wont catch it)
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

    status = '200 OK'
    result_message = '<p class="error">Default message (this is a bug)'

    if not legal_ssid(ssid):
        result_message = '<p class="error">SSID given is not in the correct format</p>'
    else:
        hostapd_conf_path = environ['HOSTAPD_CONF']
        temp_path = '/tmp/hostapd.conf'
        if not hostapd_conf_path:
            hostapd_conf_path = '/etc/hostapd.conf'

        try:
            infile = open(hostapd_conf_path)
            outfile = open(temp_path, 'w')

            for line in infile:
                if re.match("^\s?ssid", line):
                    outfile.write('ssid=%s\n' % ssid)
                else:
                    outfile.write(line)

            infile.close()
            outfile.close()

            shutil.copyfile(temp_path, hostapd_conf_path)

            result = subprocess.call(["sudo", "service", "hostapd", "restart"])

            if result is not 0:
                result_message = '<p class="error">Failed to restart hostapd. See log for details.</p>'
            else:
                result_message = '<table class="config">'
                result_message += '<tr><td>SSID:</td><td>%s</td></tr>' % ssid
                result_message += '</table>'
                result_message += '<p class="success">Changes saved.</p>'

        except IOError as error:
            status = '500 Internal Server Error'
            result_message = '<p class="error">Failed to update configuration file. See log file for details.</p>'
            print error

    response_body = html % {'returnMessage':result_message}

    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    return response_body  # sends the html to the user's web browser.
