from qrencode import Encoder
import MySQLdb
import qwifiutils
import pwgen

def application(environ, start_response):

    # reads in the html code to be displayed
    html = (open(environ['RESOURCE_BASE'] + '/html/qr.html', 'r').read())

    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])
    connection = True
    error_string = ''
    form_string = ''
    try:
        db = MySQLdb.connect(config.get('database', 'server'),
            config.get('database', 'username'),
            config.get('database', 'password'),
            config.get('database', 'database'))
        c = db.cursor()
    except:
        print("Failed to query database")
        status = '500 Internal Server Error'
        error_string += '<p>Could not connect to the Database</p>'
	connection = False

    try:
        timeout = config.getint('session', 'timeout')
    except ValueError:
        error_string += '<p class="error">Unable to read timeout from configuration file</p>' 

    timeout_units = config.get('display', 'units')
    if timeout_units != 'seconds' and timeout_units != 'minutes' and timeout_units != 'hours' and timeout_units != 'days':
        error_string +='<p class="error">Unable to read timeout units from configuration file</p>'

    if connection and error_string == '':
        # We've succesfully connected to the database
        config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])


        # converts timeout from seconds to value stored in timeout_units
        # user might not like seeing that their session time is '432,000 seconds'
        if timeout_units == 'minutes':
            timeout = timeout / 60
        elif timeout_units == 'hours':
            timeout = timeout / 3600
        elif timeout_units == 'days':
            timeout = timeout / 86400
        else:
            timeout = timeout

        pw_dict = pwgen.gen_user_pass()
        username = 'qwifi' + pw_dict['username']
        password = pw_dict['password']

        print 'Session mode: ' + config.get('session', 'mode')

        code = ''
        ssid = qwifiutils.get_ssid(environ['HOSTAPD_CONF'])

        end = ''

        try:
            query = "SELECT username,value FROM radcheck where username LIKE 'qwifi%'"
            c.execute(query)
            result = c.fetchall()
            if config.get('session', 'mode') == 'ap':
                if len(result) > 0:
                    username = result[0][0]
                    password = result[0][1]
                    print 'Using existing code: %s %s' % (username, password)
                else:
                    print "Couldn't find access code for ap mode. A new random code has been generated."

                    query = "INSERT INTO radcheck SET username='%(username)s',attribute='Cleartext-Password',op=':=',value='%(password)s';" % { 'username' : username, 'password' : password }
                    c.execute(query)
                    query = "INSERT INTO radcheck (username,attribute,op,value) VALUES ('%(username)s', 'Vendor-Specific', ':=', DATE_FORMAT(UTC_TIMESTAMP() + INTERVAL %(timeout)s SECOND, '%%Y-%%m-%%d %%H:%%i:%%s'));" % { 'username' : username, 'timeout' : config.get('session', 'timeout') }
                    c.execute(query)
                    db.commit()

                query = "SELECT value FROM radcheck WHERE attribute='Vendor-Specific'"
                c.execute(query)
                result = c.fetchall()
                end = result[0][0];

                code = "WIFI:T:WPAEAP;S:%(ssid)s;P:%(password)s;H:false;U:%(username)s;E:PEAP;N:MSCHAPV2;X:%(end)s;;" % {'ssid': ssid, 'username' : username, 'password' : password, 'end': end}
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

        print(code)

        enc = Encoder()
        im = enc.encode(code, {'width':200})
        im.save("/var/www/codes/qr.png")
        status = '200 OK'

        form_string += '<img src="/codes/qr.png"/>'
        form_string += '<p>Username: %s</p>' % username
        form_string += '<p>Password: %s</p>' % password
        if config.get('session', 'mode') == 'ap':
            form_string += '<p>Session End: %s UTC' % end
        else:
            form_string += '<p>Session Length: %s' % timeout
            form_string += ' %s</p>' % timeout_units
    else:
        form_string += error_string
        status = '500 Internal Server Error'


    # adds the content to the html
    response_body = html % {'returnMessage':form_string}
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    return response_body
