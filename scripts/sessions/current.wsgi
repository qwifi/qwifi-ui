import MySQLdb

def application(environ, start_response):
	status = '200 OK'

	response_headers = [('Content-type', 'text/html')]
	html = (open(environ['RESOURCE_BASE'] + '/html/base.html', 'r').read())#reads in the html code to be displayed
	
	try:
		db = MySQLdb.connect("localhost","radius","radius","radius")#host, user, password, db
		cursor = db.cursor()
		cursor.execute("SELECT radcheck.username, radacct.callingstationId FROM radcheck INNER JOIN radacct ON radcheck.username=radacct.username WHERE radacct.acctstoptime is NULL AND radcheck.attribute='Cleartext-Password';")

		result = "<h1>Active Sessions</h1>"

		rows = cursor.fetchall()

		if rows:
			for row in rows:
				username = row[0]
				station_id = row[1].replace('-',':')
				result += "%(username)s %(station_id)s <a href=\"/sessions/revoke?user=%(username)s&id=%(station_id)s\">Revoke</a><br />" % {'username' : username, 'station_id' : station_id}
		else:
			result += "None"
		
		html=html%(result)
		start_response(status, response_headers)	
		return html

	except:
		print("Failed to query database")
		status = '500 Internal Server Error'
		
		start_response(status, response_headers)	
		return "Error querying database"

