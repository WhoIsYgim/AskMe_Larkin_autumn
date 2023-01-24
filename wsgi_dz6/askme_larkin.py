from urllib.parse import urlparse, parse_qs


def app(environ, start_response):
    print(environ)

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    body = b'GET PARAMETERS:\n'
    URI = urlparse(environ['RAW_URI'])

    qs = parse_qs(URI.query)
    print(qs)
    for key in qs:
        str_ = key + ':'
        for value in qs[key]:
            str_ += value + ' '
        str_ += '\n'

        body += str_.encode()

    body += b'POST PARAMETERS:\n'
    request_body = environ['wsgi.input'].read(request_body_size)

    #post = parse_qs(request_body)
    # print(post)
    # for key in post:
    #     str_ = key + ':'.encode()
    #     for value in qs[key]:
    #         str_ += value + ' '.encode()
    #     str_ += '\n'.encode()
    #
    #     body += str_

    body += request_body

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return [body]
