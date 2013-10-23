from cgi import parse_qs, escape

fileLocation = 'c:\config.txt'  #finds the location of the config file

html = (open('C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/base.txt', 'r').read())  # reads in the html file

def application(environ, start_response):
    response_body = html % ('')#adds any strings to the html if so desired.

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]#sends the html to the user's web browser
