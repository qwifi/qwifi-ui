from types import StringType
from datetime import datetime
from dateutil import tz
import qwificore

def application(environ, start_response):

    session_info = qwificore.get_session_info(environ['CONFIGURATION_FILE'], environ['HOSTAPD_CONF'])

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
            # ref: http://stackoverflow.com/a/4771733/577298
            output_format = '%Y-%m-%d %I:%M:%S %p %Z'
            utc_zone = tz.tzutc()
            to_zone = tz.tzlocal()

            #can't use strtptime because of http://bugs.python.org/issue8098 >:(
            utc_time_string = session_info['end']
            year = int(utc_time_string[:4])
            month = int(utc_time_string[5:7])
            day = int(utc_time_string[8:10])
            hour = int(utc_time_string[11:13])
            minute = int(utc_time_string[14:16])
            second = int(utc_time_string[17:19])

            utc_time = datetime(year, month, day, hour, minute, second, 0, utc_zone)
            local_time = utc_time.astimezone(to_zone)

            session_info['end'] = local_time.strftime(output_format)

            result = '<p>SSID: %(ssid)s</p><p>Username: %(username)s</p><p>Password: %(password)s</p><p>Session End: %(end)s </p>' % session_info

        status = '200 OK'

    response_body = result
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    return response_body
