from quopri import decodestring

from framework.http_requests import PostRequest, GetRequest


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    def __init__(self, routes_obj, fronts_obj):
        self.routes_list = routes_obj
        self.fronts_list = fronts_obj

    def __call__(self, environ, start_response):
        # get request path
        path = environ['PATH_INFO']

        # adding slash if need
        if not path.endswith('/'):
            path = f'{path}/'

        request = dict()
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            print(f'POST-request: {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequest().get_request_params(environ)
            request['request_params'] = Framework.decode_value(request_params)
            print(f'GET-params:'f' {Framework.decode_value(request_params)}')

        # Page Controller pattern
        if path in self.routes_list:
            view = self.routes_list[path]
        else:
            view = PageNotFound404()

        # Front Controller pattern
        # request = {}
        # for front in self.fronts_list:
        #     front(request)

        # start controller for request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        decoded_data = {}
        for k, v in data.items():
            value = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            value_decode_str = decodestring(value).decode('UTF-8')
            decoded_data[k] = value_decode_str
        return decoded_data
