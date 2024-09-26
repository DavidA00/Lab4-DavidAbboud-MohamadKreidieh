import tkinter as tk
import re
import json

studentsStorage = {}
InstructorsStorage = {}
coursesStorage = {}
courseNameStorage = {}

visited = set()

desMap = set()

class Person:
    '''
    This is the base class, which the student and instructor classes inherit from
    :param name: Name of the person
    :type name: String
    :param age: Age of the person
    :type age: int
    :param email: Email of the person
    :type email: string
    :raises ValueError: if the email format is invalid, or if the age is 0 or less
    '''
    def __init__(self, name: str, age: int, email: str):
        emailRegex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(emailRegex, email):
            raise ValueError("Invalid Email Format")
        
        elif age <= 0:
            raise ValueError("Invalid Age")
        
        else:
            self.name = name
            self.age = age
            self.__email = email
    
    def introduce(self):
        '''
        Introduces the person, saying their name, age, and email
        '''
        print("My name is", self.name + ". I am", self.age, "years old, and my email is", self.__email)
    
    def serialize(self):
        '''
        Serializes the person, to be stored in a file
        '''
        return {
            "name": self.name,
            "age": self.age,
            "email": self.__email
        }
    
    @classmethod
    def deserialize(cls, data):
        '''
        Deserializes a person's data which was stored in a file
        '''
        return cls(data["name"], data["age"], data["email"])

class Student(Person):
    '''
    A student class, which inherits the Person Class. It stores student's information, including name, age, email, id, and a list of registered courses
    :param name: The student's name
    :type name: str
    :param age: The student's age
    :type age: int
    :param email: The student's email
    :type email: str
    :param id: The student's ID
    :type id: str
    :param registeredCourses: The list of courses to which the student is registered, defaults to None
    :type registeredCourses: list, optional
    :raises ValueError: the email format is invalid, or the age is invalid
    '''
    def __init__(self, name: str, age: int, email: str, id: str, registeredCourses = None):
        Person.__init__(self, name, age, email)
        self.student_id = id
        if registeredCourses == None:
            self.registered_courses = []
        else:
            self.registered_courses = registeredCourses
        
        studentsStorage[str(id)] = self
    
    def registerCourse(self, course):
        '''
        Registers a student to a course
        :param course: the course to which the student will be registered
        :type course: class:"Course"
        '''
        if not course in self.registered_courses:
            self.registered_courses.append(course)
    
    def id(self):
        '''
        returns a unique ID for the student, among all other data types
        :return: the unique ID
        :rtype: string
        '''
        return "s" + self.student_id

    def serialize(self):
        '''
        serializes the student object
        :return: serialized student object
        :rtype: dictionary
        '''
        if self.id() in visited:
            return {"id": self.student_id}

        visited.add(self.id())

        return {
            "name": self.name,
            "age": self.age,
            "email": self._Person__email,
            "id": self.student_id,
            "registered_courses": [course.serialize() for course in self.registered_courses]
        }
    
    @classmethod
    def deserialize(cls, data):
        '''
        deserializes the student data
        :param data: the data to be deserialized
        :type data: dict
        :return: a new Student Object containing deserialized data
        :rtype: class:Student
        '''
        if 'id' in data:
            if "s" + data["id"] in desMap:
                return desMap["s" + data["id"]]

        return cls(data["name"], data["age"], data["email"], data["id"], data["registered_courses"])
    
    # # made this a class method so that I can create a person object, and so that it can be used by subclasses
    # @classmethod
    # def deserialize(cls, data):
    #     if(data["name"] != None and data["age"] > 0 and )
    #     return cls(data["name"], data["age"], data["email"])

class Instructor(Person):
    '''
    Stores the data for the instructor. This includes name, age, email, instructor ID, and a list of assigned courses
    :param name: The name of the instructor
    :type name: str
    :param age: The age of the instructor
    :type age: int
    :param email: The email of the instructor
    :type email: str
    :param instructor_id: The ID of the instructor
    :type instructor_id: str
    :param assigned_courses: A list of courses to which the instructor is assigned as instructor defaults to None
    :type assigned_courses: list optional
    :raises ValueError: the ID is already in use by another instructor, or the age or email is invalid
    :'''
    def __init__(self, name: str, age: int, email: str, instructor_id: str, assignedCourses = None):
        if (not instructor_id) or (instructor_id in InstructorsStorage):
            raise ValueError("An instructor with this ID already exists")
        Person.__init__(self, name, age, email)
        self.instructor_id = instructor_id
        if assignedCourses == None:
            self.assigned_courses = []
        else:
            self.assigned_courses = assignedCourses
        
        InstructorsStorage[instructor_id] = self
    
    def assignCourse(self, course):
        '''
        Assigns a course to an instructor
        Also adds it to the course
        :param course: The course to which the instructor is assigned
        :type course: class:Course
        '''
        if not course in self.assigned_courses:
            self.assigned_courses.append(course)
            course.assignInstructor(self)
    
    def id(self):
        '''
        Creates a unique identifier for the instructor
        :returns: The unique identifier
        :rtype: str
        '''
        return "i" + self.instructor_id
    
    def serialize(self):
        '''
        serializes the instructor object
        :return: the serialized instructor object
        :rtype: dictionary
        '''
        if id(self) in visited:
            return {"id": self.instructor_id}

        visited.add(self.id())

        return {
            "name": self.name,
            "age": self.age,
            "email": self._Person__email,
            "instructor_id": self.instructor_id,
            "assigned_courses": [course.serialize() for course in self.assigned_courses]
        }
    
    @classmethod
    def deserialize(cls, data):
        '''
        Deserializes the data provided
        :param data: the data to be deserialized
        :type data: dictionary
        :return: A new Instructor object, containing the deserialized data
        :rtype: class:Instructor
        '''
        assigned_courses_data = data.get("assigned_courses", [])
        assigned_courses = [Course.deserialize(course_data) for course_data in assigned_courses_data]
        # assigned_courses = [Course.deserialize(course_data) for course_data in data["assigned_courses"]]
        return cls(data["name"], data["age"], data["email"], data["instructor_id"], assignedCourses=assigned_courses)

class Course:
    '''
    Contains the data for a course, including course ID, course name, instructor, and a list of enrolled students
    :param course_id: The ID of the course
    :type course_id: str
    :param course_name: The name of the course
    :type course_name: str
    :param instructor: The instructor of the course
    :type instructor: class:Instructor
    :param enrolled_students: A list of students who are enrolled in the course, defaults to None
    :type enrolled_students: list optional
    '''
    def __init__(self, course_id: str, course_name: str, instructor: Instructor, enrolled_students = None):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        if instructor != None:
            instructor.assignCourse(self)
        
        if enrolled_students == None:
            self.enrolled_students = []
        else:
            self.enrolled_students = enrolled_students
        
        coursesStorage[course_id] = self
        courseNameStorage[course_name] = self
    
    def add_student(self, student: Student):
        '''
        Adds a student to a course
        :param student: The student to be enrolled
        :type student: class:Student
        :raises ValueError: If the student is invalid
        '''
        if student == None:
            raise ValueError("Invalid Student")
        elif not student in self.enrolled_students:
            self.enrolled_students.append(student)

    def assignInstructor(self, instructor: Instructor):
        '''
        Assigns an instructor to the course, replacing the old instructor, and removes the course from the instructor list of assigned courses
        :param instructor: The new instructor
        :type instructor: class:Instructor
        '''
        if instructor != None and self.instructor != instructor:
            if(self.instructor != None):
                self.instructor.assigned_courses.remove(self)
            self.instructor = instructor
            instructor.assignCourse(self)
    
    def id(self):
        '''
        Creates a unique identifier for the object
        :return: The unique identifier for the object
        :rtype: str
        '''
        return "c" + self.course_id
    
    def serialize(self):
        '''
        Serializes the data
        :return: A dictionary containing the data
        :rtype: dictionary
        '''
        if self.id() in visited:
            return {"id": self.course_id}

        visited.add(self.id())

        if self.instructor:
            return {
                "course_id": self.course_id,
                "course_name": self.course_name,
                "course_instructor": self.instructor.serialize(),
                "enrolled_students": [student.serialize() for student in self.enrolled_students]
            }
        else:
            return {
                "course_id": self.course_id,
                "course_name": self.course_name,
                "course_instructor": None,
                "enrolled_students": [student.serialize() for student in self.enrolled_students]
            }
    
    @classmethod
    def deserialize(cls, data):
        '''
        Deserializes the given data
        :param data: The data to be deserialized
        :type data: dictionary
        :return: A new Course object, which contains the deserialized data
        '''
        instructor_data = data.get("course_instructor")
        instructor = Instructor.deserialize(instructor_data) if instructor_data else None
        enrolled_students = [Student.deserialize(student_data) for student_data in data["enrolled_students"]]
        return cls(data["course_id"], data["course_name"], instructor, enrolled_students=enrolled_students)
    
def saveData(filename: str):
    '''
    Saves the data to a file
    :param filename: The name of the file to which the data will be stored
    :type filename: str
    '''
    data = {
        "students": [student.serialize() for student in studentsStorage.values()],
        "instructors": [instructor.serialize() for instructor in InstructorsStorage.values()],
        "courses": [course.serialize() for course in coursesStorage.values()]
    }

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def loadData(filename: str):
    '''
    Loads the data from the file
    :param filename: The name of the file in which the data is stored
    :type filename: str'''
    global studentsStorage, InstructorsStorage, coursesStorage
    try:
        with open(filename, 'r') as file:
            data = json.load(file)

            studentsStorage = {student["id"]: Student.deserialize(student) for student in data["students"]}
            InstructorsStorage = {instructor["instructor_id"]: Instructor.deserialize(instructor) for instructor in data["instructors"]}
            coursesStorage = {course["course_id"]: Course.deserialize(course) for course in data["courses"]}
    except FileNotFoundError:
        print("Error: file not found.")


# s1 = Student("student 1", 10, "s1@s1.s1", "s1")
# i1 = Instructor("instructor 1", 10, "i1@i1.i1", "i1")
# c1 = Course("c1", "course 1", None)

# s2 = Student("student 2", 20, "s2@s2.s2", "s2")
# s2.registerCourse(c1)
# i2 = Instructor("instructor 2", 20, "i2@i2.i2", "i2")
# c2 = Course("c2", "course 2", i2)

# saveData("trial2")

# print(studentsStorage)
# print(InstructorsStorage)
# print(coursesStorage)

# loadData("trial1")
# print(studentsStorage)
# print(InstructorsStorage)
# print(coursesStorage)