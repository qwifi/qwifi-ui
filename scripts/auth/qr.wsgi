from qrencode import Encoder
import string, random
import MySQLdb
import qwifiutils

def application(environ, start_response):
    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])
    db = MySQLdb.connect(config.get('database', 'server'),
        config.get('database', 'username'),
        config.get('database', 'password'),
        config.get('database', 'database'))
    c = db.cursor()

    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])

    timeout = config.getint('main', 'timeout')

    pwsize = 10
    username = 'qwifi' + ''.join(random.sample(string.ascii_lowercase, pwsize))
    password = ''.join(random.sample(string.ascii_lowercase, pwsize))

    print 'Session mode: ' + config.get('session', 'mode')

    try:
        query = "SELECT username,value FROM radcheck where username LIKE 'qwifi%'"
        c.execute(query)
        result = c.fetchall()
        if config.get('session', 'mode') == 'ap' and len(result) > 0:
            username = result[0][0]
            password = result[0][1]
            print 'Using existing code: %s %s' %(username, password)
        else:
            # use randomly generated password
            query = "INSERT INTO radcheck SET username='%(username)s',attribute='Cleartext-Password',op=':=',value='%(password)s';" % { 'username' : username, 'password' : password }
            c.execute(query)

            query = "INSERT INTO radcheck SET username='%(username)s',attribute='Session-Timeout',op=':=',value='%(timeout)s';" % { 'username' : username, 'timeout' : timeout }
            c.execute(query)
            db.commit()
    except MySQLdb.Error, e:
        db.rollback()
        print("Database error: %s" % e)
        raise

    ssid = qwifiutils.get_ssid(environ['HOSTAPD_CONF'])
    code = "WIFI:T:WPAEAP;S:%(ssid)s;P:%(password)s;H:false;U:%(username)s;E:PEAP;N:MSCHAPV2;X:%(timeout)s;;" % {'ssid': ssid, 'username' : username, 'password' : password, 'timeout': timeout}

    print(code)

    enc = Encoder()
    im = enc.encode(code, {'width':200})
    im.save("/tmp/out.png")
    status = '200 OK'
    response_headers = [('Content-type', 'image/png')]
    start_response(status, response_headers)

    return file("/tmp/out.png")
