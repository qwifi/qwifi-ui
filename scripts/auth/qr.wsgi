from qrencode import Encoder
import string, random
import MySQLdb

def application(environ, start_response):
	db = MySQLdb.connect("localhost","radius","radius","radius")#host, user, password, db
	c = db.cursor()

	pwsize = 10
	user = ''.join(random.sample(string.ascii_lowercase, pwsize))
	password = ''.join(random.sample(string.ascii_lowercase, pwsize))

	query = "INSERT INTO radcheck SET username='%(username)s',attribute='Cleartext-Password',op=':=',value='%(password)s';" % { 'username' : user, 'password' : password }

	try:
 		#Execute the sql command
 		c.execute(query)
  		#commit the changes to the database
  		db.commit()
	except:
  		#Something bad happened rollback the changes
  		db.rollback()
  		print("Error adding credentials to database")


	query = "INSERT INTO radcheck SET username='%(username)s',attribute='Session-Timeout',op=':=',value='%(timeout)s';" % { 'username' : user, 'timeout' : 10 }

	try:
 		#Execute the sql command
 		c.execute(query)
  		#commit the changes to the database
  		db.commit()
	except:
  		#Something bad happened rollback the changes
  		db.rollback()
		print("Error adding session timeout to database")

	code = "WIFI:T:WPAEAP;S:qwifi;P:%(password)s;H:false;U:%(user)s;E:PEAP;N:MSCHAPV2;;" % {'user' : user, 'password' : password}
	
	print(code)

	enc = Encoder()
	im = enc.encode(code, {'width':200})
	im.save("/tmp/out.png")
	status = '200 OK'
	response_headers = [('Content-type', 'image/png')] 
	start_response(status, response_headers)
	return file("/tmp/out.png")
	#return [output]
