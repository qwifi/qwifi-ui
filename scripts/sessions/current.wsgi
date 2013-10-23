import MySQLdb
import qwifiutils

def application(environ, start_response):
    status = '200 OK'

    response_headers = [('Content-type', 'text/html')]

    result = ''

    try:
        config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])
        db = MySQLdb.connect(config.get('database', 'server'),
            config.get('database', 'username'),
            config.get('database', 'password'),
            config.get('database', 'database'))
        cursor = db.cursor()
        cursor.execute("SELECT radcheck.username, radacct.callingstationId FROM radcheck INNER JOIN radacct ON radcheck.username=radacct.username WHERE radacct.acctstoptime is NULL AND radcheck.attribute='Cleartext-Password';")

        result = "<h1>Active Sessions</h1>"

        rows = cursor.fetchall()

        if rows:
            for row in rows:
                username = row[0]
                station_id = row[1].replace('-', ':')
                result += "%(username)s %(station_id)s <a href=\"/sessions/revoke?user=%(username)s&id=%(station_id)s\">Revoke</a><br />" % {'username' : username, 'station_id' : station_id}
        else:
            result += "None"

    except:
        print("Failed to query database")
        status = '500 Internal Server Error'
        result = '<p class="error">Error querying database</a>'

    result = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read()) % result
    start_response(status, response_headers)

    return result
