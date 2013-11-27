import ConfigParser
import MySQLdb
import os
import pwgen
import re

def get_config(config_path):
    config = ConfigParser.ConfigParser()

    config.add_section('display')
    config.set('display', 'units', 'seconds')

    config.add_section('database')
    config.set('database', 'server', 'localhost')
    config.set('database', 'username', 'root')
    config.set('database', 'password', 'password')
    config.set('database', 'database', 'radius')
    config.add_section('logging')
    config.set('logging', 'level', 'debug')

    config.add_section('session')
    config.set('session', 'timeout', '10')
    config.set('session', 'mode', 'device')

    if (os.path.isfile(config_path)):
        config.read(config_path)
        # TODO: handle parsing exceptions

    return config

def get_ssid(hostapd_conf_path):
    if not hostapd_conf_path:
        hostapd_conf_path = '/etc/hostapd/hostapd.conf'

    ssid = 'qwifi'

    try:
        with open(hostapd_conf_path) as infile:
            for line in infile:
                # TODO: make this match less naive: hostapd.conf printf-escaped strings as SSIDs
                match = re.match('^\s?ssid=(".+"|[^"].+)\s', line)
                if match:
                    ssid = match.group(1)
    except IOError as error:
        print error

    return ssid

def get_session_info(config_path, hostapd_conf_path):
    """
    Get a dictionary containing session information.

    Dictionary keys:
    ssid -- the SSID of the network
    username -- the username/identity
    password -- the password
    timeout OR end -- the timeout in seconds OR the absolute end time in UTC

    Returns a string error message if there's a problem.
    """

    config = get_config(config_path)

    try:
        db = MySQLdb.connect(config.get('database', 'server'),
            config.get('database', 'username'),
            config.get('database', 'password'),
            config.get('database', 'database'))
        c = db.cursor()
    except:
        return 'Could not connect to the database.'

    timeout = ''
    try:
        timeout = config.getint('session', 'timeout')
    except ValueError:
        return 'Unable to read timeout from configuration file.'

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
                return 'ERROR: Program could not generate a unique username.'
        else:
            break

    ssid = get_ssid(hostapd_conf_path)

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

            return {'ssid': ssid, 'username' : username, 'password' : password, 'end': end}
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
                    return 'No timeout found.'
                if len(result) > 1:
                    return 'Found %s timeouts (expected 1).' % len(result)
                else:
                    timeout = result[0][0]
            else:
                timeout = config.get('session', 'timeout')
                # use randomly generated password
                query = "INSERT INTO radcheck SET username='%(username)s',attribute='Cleartext-Password',op=':=',value='%(password)s';" % { 'username' : username, 'password' : password }
                c.execute(query)
                query = "INSERT INTO radcheck SET username='%(username)s',attribute='Session-Timeout',op=':=',value='%(timeout)s';" % { 'username' : username, 'timeout' : timeout }
                c.execute(query)
                query = "INSERT INTO radcheck SET username='%(username)s',attribute='Simultaneous-Use',op=':=',value='1';" % { 'username' : username }
                c.execute(query)
                db.commit()

            return {'ssid': ssid, 'username' : username, 'password' : password, 'timeout': timeout}

    except MySQLdb.Error, e:
        db.rollback()
        return str(e)
