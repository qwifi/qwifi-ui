
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

#lines 9-101 (the following ones) consists of HTML code to be output to the client
html="""<html>
<head>
<link rel="stylesheet" type="text/css" href="page.css">
<style> 
body
{
    background-color:#003000;
    margin:0px;
}
p
{
margin:0px;
}

.title
{
    background-color:#008000;
    margin-left:auto;
    margin-right:auto;
    margin-top:0px;
    margin-bottom:0px;
    width:70%;
    height:150px;
    border-top-left-radius:10% 50%;
    border-top-right-radius:10% 50%;
    text-align:center;
    color:#EBFFEB;
    font-size:80px;

}

.secTitle
{
    font-size:50px;
}

.linkBar
{
    background-color:#008000;
    margin-left:auto;
    margin-right:auto;
    width:70%;
    height:40px;
    text-align:center;
    color:#EBFFEB;
}

.mainBody
{
    background-color:#008000;
    margin-left:auto;
    margin-right:auto;
    width:70%;
    height:700px;
    color:#EBFFEB;
    font-size:20px;
}
</style><!--end of style-->
</head>
<div class="title">
    <p>
        Jormungandr Studios
    </p>
    <p style="font-size:40">
        Special Development Squadron
    </p>
</div>
<div class="linkBar">
</div>
<div class="mainBody">
    <p>
        Administrative controls
    </p>
        <form method="post" action="adminUI"><!--when form is filled out, goes to form2.html-->
            <p>
                SSID Name
        <input name="ssidName" /><!--saves the form input as a variable called 'bob'-->
                </p>
            <p>
            Time until timeout
        <input name="timeout" /><!--saves the form input as a variable called 'bob'-->
                </p>
            <p>
                Time is in:<br>
                <input type="radio" name = "timeUnit" value = "seconds">Seconds<br>
                <input type = "radio" name = "timeUnit" value = "minutes">Minutes<br>
                <input type = "radio" name = "timeUnit" value = "hours">Hours<br>
                <input type = "radio" name = "timeUnit" value = "days">days
            </p>
    <input type="submit" /><!--creates a button to be pressed-->
</div>
</html>"""

def application(environ, start_response):

   configFile=open('c:/config.txt', 'r')
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

   timeout = d.get('timeout', [''])[0] # Returns the first age value.
   timeUnit = d.get('timeUnit', []) # Returns a list of hobbies.
   ssidName = d.get('ssidName',[])
   timeout =(timeout or pastTimeout)
   timeUnit = (timeUnit or pastTimeUnit)
   ssidName=(ssidName or pastSsidName)
   
   configFile=open('C:/config.txt','w')
   configFile.write(str(timeout))
   configFile.write('\n')
   configFile.write(str(timeUnit))
   configFile.write('\n')
   configFile.write(str(ssidName))
   configFile.close()

   response_body=html

   status = '200 OK'
   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)
   

   
   

   return response_body
  
