from framework.main import Framework
from urls import routes, fronts


if __name__ == '__main__':
    application = Framework(routes, fronts)
