from datetime import date

from views import Index, Contact


# front controller
def date_adding(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [date_adding, other_front]

routes = {
    '/': Index(),
    '/contact/': Contact(),
}
