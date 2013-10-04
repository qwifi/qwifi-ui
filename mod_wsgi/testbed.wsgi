
from cgi import parse_qs, escape


fileLocation='c:\config.txt'#fileReplace

html=(open('C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/base.txt','r').read())#fileReplace


def application(environ, start_response):

   backGroundColor='003000'
   foreGroundColor='008000'
   try:
	configFile=open(fileLocation, 'r')
	pastTimeout=configFile.readline().rstrip()
	pastTimeUnit=configFile.readline().rstrip()
	pastSsidName=configFile.readline().rstrip()
	configFile.close()
   except:
	configFile=open(fileLocation, 'w')
	configFile.write('8000\n')
	configFile.write('seconds\n')
	configFile.write('standard')
	

   formString='<p>Administrative controls</p><form method="post" action="adminUI"><p>SSID Name<input name="ssidName" value="'
   formString+=str(pastSsidName)
   formString+='" /></p><p>Time until timeout<input name="timeout" value="'
   formString+=str(pastTimeout)
   formString+='" /></p><p>Time is in:<br><input type="radio" name = "timeUnit" value = "seconds" checked>Seconds<br><input type = "radio" name = "timeUnit" value = "minutes">Minutes<br><input type = "radio" name = "timeUnit" value = "hours">Hours<br><input type = "radio" name = "timeUnit" value = "days">days</p><input type="submit" />'
   response_body=html %(backGroundColor,foreGroundColor,foreGroundColor,foreGroundColor,formString)

   status = '200 OK'
   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)
   

   
   

   return [response_body]
  
