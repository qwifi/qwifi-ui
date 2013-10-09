from cgi import parse_qs, escape

def application(environ, start_response):
   fileLocation=environ['CONFIGURATION_FILE']
   html=(open(environ['TEMPLATE_BASE'] + '/base','r').read())

   returnMessage='Changes Saved!'
   backGroundColor='003000'
   foreGroundColor='008000'

   # the environment variable CONTENT_LENGTH may be empty or missing
   try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
   except (ValueError):
      request_body_size = 0

   # When the method is POST the query string will be sent
   # in the HTTP request body which is passed by the WSGI server
   # in the file like wsgi.input environment variable.
   request_body = environ['wsgi.input'].read(request_body_size)
   d = parse_qs(request_body)

   timeout = d.get('timeout', [''])[0] # Takes in the form input.
   timeUnit = d.get('timeUnit',[]) 
   ssidName = d.get('ssidName',[])
   timeUnit=str(timeUnit)
   ssidName=str(ssidName)
   
   timeout = int(timeout)
   
   if timeUnit == 'minutes':#if else statements determine what the selection for timeUnit was
	timeout=timeout*60#multiplies the timeout variable based on what the timeUnit was into seconds
   elif timeUnit =='hours':
	timeout=timeout*3600
   elif timeUnit == 'days':
	timeout=timeout*86400
   else:
	timeout=timeout
   
   try:
	configFile=open(fileLocation,'w')
	configFile.write('Timeout=')
	configFile.write(str(timeout))
	configFile.write('\n')
	configFile.write('TimeUnit=')
	configFile.write(timeUnit)
	configFile.write('\n')
	configFile.write('SSIDName=')
	configFile.write(ssidName)
	configFile.close()
   except:
	returnMessage='ERROR! Could not save to file!'
	backGroundColor='300000'
	foreGroundColor='800000'
	

   response_body=html%(backGroundColor,foreGroundColor,foreGroundColor,foreGroundColor,returnMessage)

   status = '200 OK'
   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)
   

   
   

   return response_body
  
