import MySQLdb
from subprocess import call
from cgi import parse_qs

def application(environ, start_response):
	status = '200 OK'
	response_headers = [('Content-type', 'text/html')]
	
	result = "Default result (this is a bug)"

	query_dictionary = parse_qs(environ['QUERY_STRING'])
	
	username = query_dictionary.get('user', [''])[0]
	if (username == ''):
		result = "Invalid user argument"
		start_response(status, response_headers)
		return result

	station_id = query_dictionary.get('id', [''])[0]
	if (station_id == ''):
		result = "Invalid station id argument"
		start_response(status, response_headers)
		return result
	
	try:
		db = MySQLdb.connect("localhost","radius","radius","radius")#host, user, password, db
		cursor = db.cursor()
	
		query = "INSERT INTO radcheck (username, attribute, op, value) VALUES ('%s', 'Auth-Type', ':=', 'Reject');" % username

		cursor.execute(query) 
		db.commit()
	except:
		status = '500 Internal Server Error'
		result = "Failed to update database"	

	hostapd_result = call(["/usr/sbin/hostapd_cli", "disassociate", station_id])
	
	result = "Result for address " + station_id + ": " + str(hostapd_result)
			
	start_response(status, response_headers)
	return result
