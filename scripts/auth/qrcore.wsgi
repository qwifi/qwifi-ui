from qrencode import Encoder
import MySQLdb
import qwifiutils
import pwgen
import sys
import time

def application(environ, start_response):

    # reads in the html code to be displayed
    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])
    connection = True
    error_string = ''
    content = ''
    try:
        db = MySQLdb.connect(config.get('database', 'server'),
            config.get('database', 'username'),
            config.get('database', 'password'),
            config.get('database', 'database'))
        c = db.cursor()
    except:
        print("Failed to query database")
        status = '500 Internal Server Error'
        error_string += '<p class="error">Could not connect to the database</p>'
	connection = False

    timeout = ''
    try:
        timeout = config.getint('session', 'timeout')
    except ValueError:
        error_string += '<p class="error">Unable to read timeout from configuration file</p>'

    if connection and error_string == '':
        # We've successfully connected to the database
        config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])

        pw_dict = pwgen.gen_user_pass()
        username = 'qwifi' + pw_dict['username']
        password = pw_dict['password']

        x = 0
        while x < 3:
            query = "SELECT username FROM radius.radacct WHERE username = '%s';" % username
            c.execute(query)
            result = c.fetchall()

            if len(result) > 0:
                # generate new username and password
                pw_dict = pwgen.gen_user_pass()
                username = 'qwifi' + pw_dict['username']
                password = pw_dict['password']
                x = x + 1

                if x == 3:
                    print 'ERROR: Program could not generate a unique username.'
                    sys.exit()
            else:
                break

        # print 'Session mode: ' + config.get('session', 'mode')

        code = ''
        ssid = qwifiutils.get_ssid(environ['HOSTAPD_CONF'])

        end = ''

        try:
            if config.get('session', 'mode') == 'ap':
                query = "SELECT username,value FROM radcheck where username LIKE 'qwifi%'"
                c.execute(query)
                result = c.fetchall()
                if len(result) > 0:
                    username = result[0][0]
                    password = result[0][1]
                else:
                    print "Couldn't find access code for ap mode. A new random code has been generated."

                    query = "INSERT INTO radcheck SET username='%(username)s',attribute='Cleartext-Password',op=':=',value='%(password)s';" % { 'username' : username, 'password' : password }
                    c.execute(query)
                    query = "INSERT INTO radcheck (username,attribute,op,value) VALUES ('%(username)s', 'Vendor-Specific', ':=', DATE_FORMAT(UTC_TIMESTAMP() + INTERVAL %(timeout)s SECOND, '%%Y-%%m-%%d %%H:%%i:%%s'));" % { 'username' : username, 'timeout' : timeout }
                    c.execute(query)
                    db.commit()

                query = "SELECT value FROM radcheck WHERE attribute='Vendor-Specific'"
                c.execute(query)
                result = c.fetchall()
                end = result[0][0];

                code = "WIFI:T:WPAEAP;S:%(ssid)s;P:%(password)s;H:false;U:%(username)s;E:PEAP;N:MSCHAPV2;X:%(end)s;;" % {'ssid': ssid, 'username' : username, 'password' : password, 'end': end}
            else:
                query = "SELECT DISTINCT username,value FROM radcheck WHERE username LIKE 'qwifi%' AND attribute='Cleartext-Password' AND NOT EXISTS (SELECT username FROM radacct where radacct.username = radcheck.username);"

                c.execute(query)
                result = c.fetchall()
                if len(result) > 0:  # we have at least one existing, unused code
                    username = result[0][0]
                    password = result[0][1]

                    query = "SELECT DISTINCT value FROM radcheck WHERE username = '%s' AND attribute='Session-Timeout';" % username
                    c.execute(query)
                    result = c.fetchall()

                    if len(result) == 0:
                        error_string += '<p class="error">No timeout found.</p>'
                    if len(result) > 1:
                        error_string += '<p class="error">Found %s timeouts (expected 1).</p>' % len(result)
                    else:
                        timeout = result[0][0]
                else:
                    # use randomly generated password
                    query = "INSERT INTO radcheck SET username='%(username)s',attribute='Cleartext-Password',op=':=',value='%(password)s';" % { 'username' : username, 'password' : password }
                    c.execute(query)
                    query = "INSERT INTO radcheck SET username='%(username)s',attribute='Session-Timeout',op=':=',value='%(timeout)s';" % { 'username' : username, 'timeout' : timeout }
                    c.execute(query)
                    query = "INSERT INTO radcheck SET username='%(username)s',attribute='Simultaneous-Use',op=':=',value='1';" % { 'username' : username }
                    c.execute(query)
                    db.commit()

                code = "WIFI:T:WPAEAP;S:%(ssid)s;P:%(password)s;H:false;U:%(username)s;E:PEAP;N:MSCHAPV2;X:%(timeout)s;;" % {'ssid': ssid, 'username' : username, 'password' : password, 'timeout': timeout}

        except MySQLdb.Error, e:
            db.rollback()
            print("Database error: %s" % e)
            raise

        # print(code)

    display_timeout = int(timeout)
    timeout_units = "seconds"

    # converts timeout from seconds to value stored in timeout_units
    # user might not like seeing that their session time is '432000 seconds'
    if display_timeout / 86400 > 0:
        display_timeout /= 86400
        timeout_units = "days"
    elif display_timeout / 3600 > 0:
        display_timeout /= 3600
        timeout_units = "hours"
    elif display_timeout / 60 > 0:
        display_timeout /= 60
        timeout_units = "minutes"

    if error_string == '':
        enc = Encoder()
        im = enc.encode(code, {'width':200})
        im.save("/var/www/codes/qr.png")
        status = '200 OK'

        # append timestamp argument to make sure code is never cached (thanks, Stack-O!)
        content += '<img src="/codes/qr.png?%s" />' % str(int(time.time()))
        content += '<p>Username: %s</p>' % username
        content += '<p>Password: %s</p>' % password
        if config.get('session', 'mode') == 'ap':
            content += '<p>Session End: %s UTC' % end
        else:
            content += '<p>Session Length: %s' % display_timeout
            content += ' %s</p>' % timeout_units
    else:
        content += error_string
        status = '500 Internal Server Error'

    # adds the content to the html
    response_body = content
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    return response_body
