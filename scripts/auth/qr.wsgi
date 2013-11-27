def application(environ, start_response):

    # reads in the html code to be displayed
    html = (open(environ['RESOURCE_BASE'] + '/html/qr.html', 'r').read())

    status = '200 OK'

    response_body = html
    response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    return response_body
