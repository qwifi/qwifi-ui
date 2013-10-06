
from cgi import parse_qs, escape


fileLocation='c:\config.txt'#fileReplace

html=(open('C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/base.txt','r').read())#fileReplace


def application(environ, start_response):

   returnMessage='Changes Saved!'
   backGroundColor='003000'
   foreGroundColor='008000'

   try:
	configFile=open(fileLocation, 'r')
	pastTimeout=configFile.readline().rstrip()
	pastTimeUnit=configFile.readline().rstrip()
	pastSsidName=configFile.readline().rstrip()
	configFile.close()
   except:
    returnMessage='ERROR! Could not open file'
    backGroundColor='300000'
    foreGroundColor='800000'
    response_body=html%(backGroundColor,foreGroundColor,foreGroundColor,foreGroundColor,returnMessage)
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return response_body

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
   timeout =(timeout or pastTimeout)
   ssidName=(ssidName or pastSsidName)
   timeUnit=str(timeUnit)
   
   timeout = int(timeout)
   
   if timeUnit is 'minutes':#if else statements determine what the selection for timeUnit was
		timeout=timeout*60#multiplies the timeout variable based on what the timeUnit was into seconds
   elif timeUnit =='hours':
		timeout=timeout*3600
   elif timeUnit == 'days':
		timeout=timeout*86400 
   
   
   try:
	configFile=open(fileLocation,'w')
	configFile.write(str(timeout))
	configFile.write('\n')
	configFile.write(timeUnit)
	configFile.write('\n')
	configFile.write(str(ssidName))
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
  
