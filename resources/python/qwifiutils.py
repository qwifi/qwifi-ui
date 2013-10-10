import ConfigParser, os

def get_config(config_path):
	config = ConfigParser.ConfigParser()

	config.add_section('main')
	config.set('main', 'timeout', '10')
	config.set('main', 'ssid', 'qwifi')
	config.add_section('display')
	config.set('display', 'units', 'seconds')

	if (os.path.isfile(config_path)):
		config.read(config_path)
		# TODO: handle parsing exceptions

	return config
