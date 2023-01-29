import os
from sqlite3 import connect
from copy import deepcopy
from quopri import decodestring
from patterns.behavioral_patterns import FileWriter, Subject
from patterns.architectural_system_patterns import DomainObject


class User:
    """abstract user"""
    def __init__(self, name):
        self.name = name


class Teacher(User):
    """teacher"""
    pass


class Student(User, DomainObject):
    """student"""
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


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
    def create(cls, type_, name):
        return cls.types[type_](name)


class CoursePrototype:
    """Creational pattern prototype"""

    def clone(self):
        """Create a deepcopy of current object instead of creating new black object"""
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    """Course based on prototype"""

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


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
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

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

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Student):

            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
