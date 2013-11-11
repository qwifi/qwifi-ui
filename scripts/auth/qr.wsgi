from qrencode import Encoder
import string, random
import MySQLdb
import qwifiutils
import pwgen

def application(environ, start_response):

    #reads in the html code to be displayed
    html = (open(environ['RESOURCE_BASE'] + '/html/qr.html', 'r').read())

    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])
    try:
        db = MySQLdb.connect(config.get('database', 'server'),
            config.get('database', 'username'),
            config.get('database', 'password'),
            config.get('database', 'database'))
        c = db.cursor()
    except:
        print("Failed to query database")
        status = '500 Internal Server Error'
        result = '<p class="error">Error querying database</p>'
        return result

    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])

    timeout = config.getint('session', 'timeout')
    timeout_units = config.get('display', 'units') 

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

    #pwsize = 10
    #username = 'qwifi' + ''.join(random.sample(string.ascii_lowercase, pwsize))
    #password = ''.join(random.sample(string.ascii_lowercase, pwsize))
    pw_dict = pwgen.gen_user_pass()
    username = pw_dict['username']
    password = pw_dict['password']

    print 'Session mode: ' + config.get('session', 'mode')

    code = ''
    ssid = qwifiutils.get_ssid(environ['HOSTAPD_CONF'])

    try:
        query = "SELECT username,value FROM radcheck where username LIKE 'qwifi%'"
        c.execute(query)
        result = c.fetchall()
        if config.get('session', 'mode') == 'ap':
            if len(result) > 0:
                username = result[0][0]
                password = result[0][1]
                print 'Using existing code: %s %s' %(username, password)
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

            code = "WIFI:T:WPAEAP;S:%(ssid)s;P:%(password)s;H:false;U:%(username)s;E:PEAP;N:MSCHAPV2;X:%(endtime)s;;" % {'ssid': ssid, 'username' : username, 'password' : password, 'endtime': result[0][0]}
        else:
            # use randomly generated password
            query = "INSERT INTO radcheck SET username='%(username)s',attribute='Cleartext-Password',op=':=',value='%(password)s';" % { 'username' : username, 'password' : password }
            c.execute(query)
            query = "INSERT INTO radcheck SET username='%(username)s',attribute='Session-Timeout',op=':=',value='%(timeout)s';" % { 'username' : username, 'timeout' : timeout }
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
    im.save("/var/www/qr.png")
    status = '200 OK'

    formString = '<img src="/var/www/qr.png"/>'
    formString += '<p>Username: %s</p>'   % username
    formString += '<p>Password: %s</p>'   % password
    formString += '<p>Session Length: %s' % timeout
    formString += ' %s</p>' % timeout_units

    #adds the content to the html
    response_body = html % {'returnMessage':formString}
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    return response_body
