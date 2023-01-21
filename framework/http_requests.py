class Request:

    @staticmethod
    def parse_input_data(data: str):
        parsed_data = dict()
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                parsed_data[k] = v
        return parsed_data


class GetRequest(Request):

    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = GetRequest.parse_input_data(query_string)
        return request_params


class PostRequest(Request):

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        parsed_data = dict()
        if data:
            data_str = data.decode(encoding='utf-8')
            parsed_data = self.parse_input_data(data_str)
        return parsed_data

    def get_request_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data
