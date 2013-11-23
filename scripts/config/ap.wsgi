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
    form_string=''
    if session_mode != 'device' and session_mode != 'ap':
        form_string += '<p class="error">Unable to determine Session Mode from configuration file.</p>'
    else:
        form_string += '<form method="post" class="apForm" action="/config/ap/update">\n'
        form_string += '<h1>Access Point Settings</h1>'
        form_string += '<div class="configItem">SSID Name<input name="ssid" value="%s" pattern ="[A-Za-z]+[0-9]*" title="Must start with a letter. Can end with numbers." required /></div>\n' % ssid

        form_string += '<h2>Session Mode</h2>'
        if session_mode == 'device':
            form_string += '<div class="configItem"><input name="session_mode" value="device" type="radio" checked />Device</div>'
        else:
            form_string += '<div class="configItem"><input name="session_mode" value="device" type="radio" />Device</div>'

        if session_mode == 'ap':
            form_string += '<div class="configItem"><input name="session_mode" value="ap" type="radio" checked />Access Point</div>'
        else:
            form_string += '<div class="configItem"><input name="session_mode" value="ap" type="radio" />Access Point</div>'

        #form_string += '<h2>RADIUS Server</h2>'
        #form_string += '<div class="configItem">IP Address<input disabled id="ipAddress" name="ip_address" value="%s" pattern="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" title="(e.x. 192.168.10.2)" required /></div>\n' % ip_address
        #form_string += '<div class="configItem">Default Gateway<input disabled id="defGateway" name="default_gateway" value="%s" pattern="^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" title=" (e.x. 192.168.10.5)" required/></div>\n' % default_gateway
        #form_string += '<div class="configItem">Subnet Mask<input disabled id="subnetMask" name="subnet_mask" value="%s" pattern="^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" title="(e.x. 255.255.255.1)" required/></div>\n' % subnet_mask
        form_string += '<input type="submit" value="Apply" />'
    

    html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())  # reads in HTML
    response_body = html % {'returnMessage':form_string}  # adds the cmntent to the html
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return response_body  # sends the html to the user's web browser.
