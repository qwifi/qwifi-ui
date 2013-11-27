import MySQLdb
from subprocess import call
from cgi import parse_qs
import qwificore

def validate_username(username):
    return username != '' and username != '%(username)s'

def validate_station_id(station_id):
    return station_id != ''

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]

    result = '<p class="error">Default result (this is a bug)</p>'

    query_dictionary = parse_qs(environ['QUERY_STRING'])

    username = query_dictionary.get('user', [''])[0]
    station_id = query_dictionary.get('id', [''])[0]

    config = qwificore.get_config(environ['CONFIGURATION_FILE'])

    if not validate_username(username):
        result = '<p class="error">Invalid user argument</p>'
    elif (config.get('session', 'mode') == 'device') and not (validate_station_id(station_id)):
        result = '<p class="error">Invalid id argument</p>'
    else:
        addresses = []

        try:
            db = MySQLdb.connect(config.get('database', 'server'),
                config.get('database', 'username'),
                config.get('database', 'password'),
                config.get('database', 'database'))
            cursor = db.cursor()

            query = "INSERT INTO radcheck (username, attribute, op, value) VALUES ('%s', 'Auth-Type', ':=', 'Reject');" % username
            print query
            cursor.execute(query)
            # query = "DELETE FROM radcheck where username='%s'" % username
            # cursor.execute(query)
            db.commit()

            if (config.get('session', 'mode') == 'device'):
                addresses += station_id
                result = '<p class="success">Revocation of access for station id %s successful.</p>' % station_id
            else:
                query = "SELECT callingstationid FROM radacct WHERE radacct.acctstoptime is NULL AND username='%s';" % username
                cursor.execute(query)
                addresses = [result[0] for result in cursor.fetchall()]
                result = '<p class="success">Revocation of access for code "%s" successful.</p>' % username
        except:
            db.rollback()
            status = '500 Internal Server Error'
            result = '<p class="success">Failed to update database</p>'

        for address in addresses:
            hostapd_result = call(["/usr/sbin/hostapd_cli", "disassociate", station_id])
            if hostapd_result is not 0:
                result = '<p class="error">Revocation of access for username "%s" and station id "%s" failed (code %s).</p>' % (username, station_id, str(hostapd_result))
                break

    start_response(status, response_headers)

    result = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read()) % {'returnMessage':result}

    return result
