from datetime import date

from views import Index, Contact, Courses, CreateCategory, CoursesList, CreateCourse, CopyCourse


# front controller
# def date_adding(request):
#     request['date'] = date.today()
#
#
# def other_front(request):
#     request['key'] = 'key'
#
#
# fronts = [date_adding, other_front]
fronts = []

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/courses/': Courses(),
    '/create-category/': CreateCategory(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/copy-course/': CopyCourse()
}
