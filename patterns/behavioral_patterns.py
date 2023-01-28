import os

from jsonpickle import dumps, loads
from framework.templator import render


class Observer:
    """behavior pattern observer"""

    def update(self, subject):
        pass


class Subject:
    """subject for observing"""

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):
    """SMS notification"""

    def update(self, subject):
        print('Sending SMS:', 'Welcome onboard, ', subject.students[-1].name)


class EmailNotifier(Observer):
    """Email notification"""

    def update(self, subject):
        print(('Sending email', 'Welcome onboard, ', subject.students[-1].name))


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


class TemplateView:
    """behavior pattern template method"""

    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


class ConsoleWriter:
    """behavior pattern Strategy"""

    def write(self, text):
        print(text)


class FileWriter:
    """behavior pattern Strategy"""

    def __init__(self):
        self.file_name = os.path.join('logs', 'log.txt')

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
