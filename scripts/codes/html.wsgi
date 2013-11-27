from types import StringType
import qwifiutils

def application(environ, start_response):

    session_info = qwifiutils.get_session_info(environ['CONFIGURATION_FILE'], environ['HOSTAPD_CONF'])

    timeout_units = "seconds"  # set a default value

    result = ''
    if type(session_info) is StringType:
        print session_info
        status = '500 Internal Server Error'
    else:
        if 'timeout' in session_info:  # we have a relative timeout

            display_timeout = int(session_info['timeout'])
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

            session_info['timeout'] = display_timeout
            session_info['display_units'] = timeout_units

            result = '<p>SSID: %(ssid)s</p><p>Username: %(username)s</p><p>Password: %(password)s</p><p>Session Length: %(timeout)s %(display_units)s</p>' % session_info
        else:
            result = '<p>SSID: %(ssid)s</p><p>Username: %(username)s</p><p>Password: %(password)s</p><p>Session End: %(end)s UTC</p>' % session_info

        status = '200 OK'

    response_body = result
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    return response_body
