import MySQLdb
from subprocess import call
from cgi import parse_qs
import qwifiutils

def validate_input(username, station_id):
    if not username:
        return '<p class="error">Invalid user argument</p>'

    if not station_id:
        return '<p class="error">Invalid id argument</p>'

    return ''

def application(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]

    result = '<p class="error">Default result (this is a bug)</p>'

    query_dictionary = parse_qs(environ['QUERY_STRING'])

    username = query_dictionary.get('user', [''])[0]

    station_id = query_dictionary.get('id', [''])[0]

    result = validate_input(username, station_id)

    if not result:
        try:
            config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])
            db = MySQLdb.connect(config.get('database', 'server'),
                config.get('database', 'username'),
                config.get('database', 'password'),
                config.get('database', 'database'))
            cursor = db.cursor()

            query = "INSERT INTO radcheck (username, attribute, op, value) VALUES ('%s', 'Auth-Type', ':=', 'Reject');" % username

            cursor.execute(query)
            db.commit()
        except:
            db.rollback()
            status = '500 Internal Server Error'
            result = '<p class="success">Failed to update database</p>'

        hostapd_result = call(["/usr/sbin/hostapd_cli", "disassociate", station_id])

        if hostapd_result is 0:
            result = '<p class="success">Revocation of access for station id %s successful</p>' % station_id
        else:
            result = '<p class="error">Revocation of access for station id %s failed (code %s)</p>' % (station_id, str(hostapd_result))

    start_response(status, response_headers)

    result = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read()) % result

    return result
