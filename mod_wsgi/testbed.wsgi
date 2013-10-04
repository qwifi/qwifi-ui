
from cgi import parse_qs, escape


fileLocation='c:\config.txt'#fileReplace

html=(open('C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/base.txt','r').read())#fileReplace


def application(environ, start_response):

   response_body=html %('<p>Administrative controls</p><form method="post" action="adminUI"><p>SSID Name<input name="ssidName" /></p><p>Time until timeout<input name="timeout" /></p><p>Time is in:<br><input type="radio" name = "timeUnit" value = "seconds">Seconds<br><input type = "radio" name = "timeUnit" value = "minutes">Minutes<br><input type = "radio" name = "timeUnit" value = "hours">Hours<br><input type = "radio" name = "timeUnit" value = "days">days</p><input type="submit" />')

   status = '200 OK'
   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)
   

   
   

   return [response_body]
  
