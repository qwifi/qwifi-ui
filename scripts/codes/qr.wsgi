from qrencode import Encoder
from types import StringType
import qwifiutils

def application(environ, start_response):

    session_info = qwifiutils.get_session_info(environ['CONFIGURATION_FILE'], environ['HOSTAPD_CONF'])

    result = ''
    if type(session_info) is StringType:
        print session_info
        status = '500 Internal Server Error'
    else:
        if 'end' in session_info:  # we have an absolute timeout
            result = "WIFI:T:WPAEAP;S:%(ssid)s;P:%(password)s;H:false;U:%(username)s;E:PEAP;N:MSCHAPV2;X:%(end)s;;" % session_info
        else:
            result = "WIFI:T:WPAEAP;S:%(ssid)s;P:%(password)s;H:false;U:%(username)s;E:PEAP;N:MSCHAPV2;X:%(timeout)s;;" % session_info

        enc = Encoder()
        im = enc.encode(result, {'width':300})
        im.save("/tmp/qr.png")
        status = '200 OK'

    response_headers = [('Content-Type', 'image/png')]

    start_response(status, response_headers)

    return file("/tmp/qr.png")
