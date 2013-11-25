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

        if (config.get('session', 'mode') == 'device'):
            result += '<table id="sessions"/>'

            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    username = row[0]
                    station_id = row[1].replace('-', ':')
                    result += "<tr><td>%(username)s</td><td>%(station_id)s</td><td><a href=\"/sessions/revoke?user=%(username)s&id=%(station_id)s\">Revoke</a></td></tr>" % {'username' : username, 'station_id' : station_id}
            else:
                result += "None"

            result += '</table>'
        elif (config.get('session', 'mode') == 'ap'):
            rows = cursor.fetchall()

            if rows:
                username = rows[0][0]
                result += '<div id="sessions">%(username)s:' % { 'username' : username }
                result += '<ul>'

                for row in rows:
                    station_id = row[1].replace('-', ':')
                    result += "<li>%(station_id)s</li>" % { 'station_id' : station_id }

                result += '</ul><a class="revoke" href="/sessions/revoke?user=%(username)s">Revoke Access Code</a>' % { 'username' : username }
            else:
                query = "SELECT DISTINCT username FROM radcheck WHERE username LIKE 'qwifi%';"
                cursor.execute(query)
                query_result = cursor.fetchall()
                if query_result:
                    username = query_result[0][0]
                    result += '<div id="sessions"><h2>%(username)s</h2>' % { 'username' : username }
                    result += '<ul><li>No Active Sessions</li></ul>'
                    result += '<a class="revoke" href="/sessions/revoke?user=%(username)s">Revoke Access Code</a>' % { 'username' : username }
                else:
                    result += '<p class="error">No active access codes.</p>'

            result += "</div>"

    except MySQLdb.Error, e:
        print("Failed to query database")
        print e
        status = '500 Internal Server Error'
        result = '<p class="error">Error querying database</a>'

    result = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read()) % {'returnMessage':result}
    start_response(status, response_headers)

    return result
