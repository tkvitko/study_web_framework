from wsgiref.simple_server import make_server

from framework.main import Framework
from urls import routes, fronts


if __name__ == '__main__':
    application = Framework(routes, fronts)
    with make_server('', 8080, application) as httpd:
        print("Starting server on port 8080...")
        httpd.serve_forever()
