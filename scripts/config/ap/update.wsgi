from cgi import parse_qs, escape
import os
import re
import shutil
import subprocess
import qwificore
import MySQLdb

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

    session_mode = d.get('session_mode', [''])[0]

    status = '200 OK'
    result_message = '<p class="error">Default message (this is a bug)'

    config_path = environ['CONFIGURATION_FILE']
    config = qwificore.get_config(config_path)

    if not (session_mode == 'device' or session_mode == 'ap'):
        result_message = '<p class="error">Invalid session mode: %s</p>' % session_mode
        response_body = html % {'returnMessage':result_message}
        response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
        start_response(status, response_headers)
        return response_body  # sends the html to the user's web browser.
    else:
        if config.get('session', 'mode') != session_mode:

            config.set('session', 'mode', session_mode)
            with open(config_path, 'wb') as config_file:
                config.write(config_file)

            try:
                print 'Session mode changed, culling database'
                # remove all access codes if we're switching session modes
                db = MySQLdb.connect(config.get('database', 'server'),
                    config.get('database', 'username'),
                    config.get('database', 'password'),
                    config.get('database', 'database'))
                c = db.cursor()
                query = "DELETE FROM radcheck where username LIKE 'qwifi%';"
                c.execute(query)
                db.commit()
            except MySQLdb.Error, e:
                    print e
                    result_message = '<p class="error">Error updating database, see log for details.</p>'
                    response_body = html % {'returnMessage':result_message}
                    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
                    start_response(status, response_headers)
                    return response_body  # sends the html to the user's web browser.

    if not legal_ssid(ssid):
        result_message = '<p class="error">SSID given is not in the correct format.</p>'
    else:
        hostapd_conf_path = environ['HOSTAPD_CONF']
        if not hostapd_conf_path:
            hostapd_conf_path = '/etc/hostapd/hostapd.conf'

        shutil.copyfile(hostapd_conf_path, '/tmp/hostapd.conf.bck')

        temp_path = '/tmp/hostapd.conf'

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
                shutil.copyfile('/tmp/hostapd.conf.bck', hostapd_conf_path)
            else:
                result_message = '<table class="config">'
                result_message += '<tr><td>SSID:</td><td>%s</td></tr>' % ssid
                result_message += '<tr><td>Session Mode:</td><td>%s</td></tr>' % session_mode
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
