import ConfigParser, os
import qwifiutils

def application(environ, start_response):
    ip_address = "192.168.52.1"
    default_gateway = "159.116.10.2"
    subnet_mask = "255.255.255.1"

    ssid = qwifiutils.get_ssid(environ['HOSTAPD_CONF'])
    config = qwifiutils.get_config(environ['CONFIGURATION_FILE'])
    session_mode = config.get('session', 'mode')

    #If the session_mode value is malformed in the config file, we'll just shut down.
    formString=''
    if session_mode != 'device' and session_mode != 'ap':
        formString += '<p class="error">Unable to determine Session Mode from configuration file.</p>'
    else:
        formString += '<form method="post" class="apForm" action="/config/ap/update">\n'
        formString += '<h1>Access Point Settings</h1>'
        formString += '<div class="configItem">SSID Name<input name="ssid" value="%s" pattern ="[A-Za-z]+[0-9]*" title="Must start with a letter. Can end with numbers." required /></div>\n' % ssid

        formString += '<h2>Session Mode</h2>'
        if session_mode == 'device':
            formString += '<div class="configItem"><input name="session_mode" value="device" type="radio" checked />Device</div>'
        else:
            formString += '<div class="configItem"><input name="session_mode" value="device" type="radio" />Device</div>'

        if session_mode == 'ap':
            formString += '<div class="configItem"><input name="session_mode" value="ap" type="radio" checked />Access Point</div>'
        else:
            formString += '<div class="configItem"><input name="session_mode" value="ap" type="radio" />Access Point</div>'

        formString += '<h2>RADIUS Server</h2>'
        formString += '<div class="configItem">IP Address<input disabled id="ipAddress" name="ip_address" value="%s" pattern="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" title="(e.x. 192.168.10.2)" required /></div>\n' % ip_address
        formString += '<div class="configItem">Default Gateway<input disabled id="defGateway" name="default_gateway" value="%s" pattern="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" title=" (e.x. 192.168.10.5)" required/></div>\n' % default_gateway
        formString += '<div class="configItem">Subnet Mask<input disabled id="subnetMask" name="subnet_mask" value="%s" pattern="^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" title="(e.x. 255.255.255.1)" required/></div>\n' % subnet_mask
        formString += '<input type="submit" value="Apply" />'
    

    html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())  # reads in HTML
    response_body = html % {'returnMessage':formString}  # adds the cmntent to the html
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return response_body  # sends the html to the user's web browser.
