import os
from copy import deepcopy
from quopri import decodestring


class User:
    """abstract user"""
    pass


class Teacher(User):
    """teacher"""
    pass


class Student(User):
    """student"""
    pass


class Staff(User):
    """staff"""
    pass


class UserFactory:
    """creational pattern fabric method"""

    types = {
        'student': Student,
        'teacher': Teacher,
        'staff': Staff
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class CoursePrototype:
    """Creational pattern prototype"""

    def clone(self):
        """Create a deepcopy of current object instead of creating new black object"""
        return deepcopy(self)


class Course(CoursePrototype):
    """Course based on prototype"""

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    """Interactive course"""
    pass


class RecordCourse(Course):
    """Recorded course"""
    pass


class CourseFactory:
    """creational pattern fabric method"""

    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category:
    """Category"""

    # incrementing category id on class's level:
    category_id = 0

    def __init__(self, name, category):
        self.id = Category.category_id
        Category.category_id += 1
        self.name = name
        self.parent_category = category
        self.courses = []

    def course_count(self):

        parents_courses = self.parent_category.course_count() if self.parent_category else 0
        return parents_courses + len(self.courses)


class Engine:
    """Project's engine"""

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name: str, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'No category with id={id}')

    @staticmethod
    def create_course(type_, name: str, category):
        return CourseFactory.create(type_, name, category)

    def find_course_by_name(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        raise Exception(f'No course with name={name}')

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    """Creational pattern singleton"""

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    """Logger"""

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        with open(os.path.join('logs', 'log.txt'), 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
