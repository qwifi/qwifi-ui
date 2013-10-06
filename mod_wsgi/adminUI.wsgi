
from cgi import parse_qs, escape


fileLocation='/home/webserver/config.txt'#fileReplace

html=(open('/usr/local/wsgi/scripts/base.txt','r').read())#fileReplace


def application(environ, start_response):

   
   configFile=open(fileLocation, 'r')
   pastTimeout=configFile.readline().rstrip()
   pastTimeUnit=configFile.readline().rstrip()
   pastSsidName=configFile.readline().rstrip()
   configFile.close()

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
   timeUnit = d.get('timeUnit', []) 
   ssidName = d.get('ssidName',[])
   timeout =(timeout or pastTimeout)
   timeUnit = (timeUnit or pastTimeUnit)
   ssidName=(ssidName or pastSsidName)
   
   configFile=open(fileLocation,'w')
   configFile.write(str(timeout))
   configFile.write('\n')
   configFile.write(str(timeUnit))
   configFile.write('\n')
   configFile.write(str(ssidName))
   configFile.close()

   response_body=html %('<p id="intro">This is the mechanism used to make changes to your access point.</p><p id="text">How to make changes:<ol id="list_one"><li> Navigate to the Display/Edit page using the link above </li><li> Enter the requested data: </li><ul><li> SSID </li><li> Time until timeout </li><li> Unit of time desired </li></ul><li> Save your changes. </li></ol></p>')


   status = '200 OK'
   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)
   

   
   

   return response_body
  
