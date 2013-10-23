import ConfigParser, os

def get_config(config_path):
	config = ConfigParser.ConfigParser()

	config.add_section('main')
	config.set('main', 'timeout', '10')
	config.add_section('display')
	config.set('display', 'units', 'seconds')

	config.add_section('database')
	config.set('database', 'server', 'localhost')
	config.set('database', 'username', 'root')
	config.set('database', 'password', 'password')
	config.set('database', 'database', 'radius')
	config.add_section('logging')
	config.set('logging', 'level', 'debug')

	if (os.path.isfile(config_path)):
		config.read(config_path)
		# TODO: handle parsing exceptions

	return config
