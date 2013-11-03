import ConfigParser
import os
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
        hostapd_conf_path = '/etc/hostapd.conf'

    ssid = 'qwifi'

    try:
        with open(hostapd_conf_path) as infile:
            for line in infile:
                #TODO: make this match less naive: hostapd.conf printf-escaped strings as SSIDs
                match = re.match('^\s?ssid=(".+"|[^"].+)\s', line)
                if match:
                    ssid = match.group(1)
    except IOError as error:
        print error

    return ssid
