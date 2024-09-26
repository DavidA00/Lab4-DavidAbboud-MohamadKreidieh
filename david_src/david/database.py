import sqlite3
import csv

class Database:
    """This class handles database operations for students, instructors, courses, and registrations.

    :param db_name: The name of the SQLite database file
    :type db_name: str
    """

    def __init__(self, db_name):
        """Initializes the database connection and creates the required tables.

        :param db_name: The name of the SQLite database file
        :type db_name: str
        :return: None
        :rtype: None
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates the necessary tables in the database.

        :return: None
        :rtype: None
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS instructors (
            instructor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            instructor_id TEXT,
            FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id)
        )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
            student_id TEXT,
            course_id TEXT,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (course_id) REFERENCES courses (course_id)
        )''')

        self.conn.commit()

    def create_student(self, student_id, name, age, email):
        """Creates a new student in the database.

        :param student_id: Unique identifier for the student
        :type student_id: str
        :param name: Name of the student
        :type name: str
        :param age: Age of the student
        :type age: int
        :param email: Email address of the student
        :type email: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('INSERT INTO students VALUES (?, ?, ?, ?)', (student_id, name, age, email))
        self.conn.commit()

    def read_student(self, student_id):
        """Reads a student's information from the database.

        :param student_id: Unique identifier for the student
        :type student_id: str
        :return: Student information as a tuple
        :rtype: tuple or None
        """
        self.cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
        return self.cursor.fetchone()

    def update_student(self, student_id, name, age, email):
        """Updates an existing student's information in the database.

        :param student_id: Unique identifier for the student
        :type student_id: str
        :param name: Updated name of the student
        :type name: str
        :param age: Updated age of the student
        :type age: int
        :param email: Updated email address of the student
        :type email: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('UPDATE students SET name = ?, age = ?, email = ? WHERE student_id = ?', 
                            (name, age, email, student_id))
        self.conn.commit()

    def delete_student(self, student_id):
        """Deletes a student from the database.

        :param student_id: Unique identifier for the student to delete
        :type student_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        self.conn.commit()

    def create_instructor(self, instructor_id, name, age, email):
        """Creates a new instructor in the database.

        :param instructor_id: Unique identifier for the instructor
        :type instructor_id: str
        :param name: Name of the instructor
        :type name: str
        :param age: Age of the instructor
        :type age: int
        :param email: Email address of the instructor
        :type email: str
        :raises sqlite3.IntegrityError: If the instructor_id already exists
        :return: None
        :rtype: None
        """
        self.cursor.execute('INSERT INTO instructors VALUES (?, ?, ?, ?)', (instructor_id, name, age, email))
        self.conn.commit()

    def read_instructor(self, instructor_id):
        """Reads an instructor's information from the database.

        :param instructor_id: Unique identifier for the instructor
        :type instructor_id: str
        :return: Instructor information as a tuple
        :rtype: tuple or None
        """
        self.cursor.execute('SELECT * FROM instructors WHERE instructor_id = ?', (instructor_id,))
        return self.cursor.fetchone()

    def update_instructor(self, instructor_id, name, age, email):
        """Updates an existing instructor's information in the database.

        :param instructor_id: Unique identifier for the instructor
        :type instructor_id: str
        :param name: Updated name of the instructor
        :type name: str
        :param age: Updated age of the instructor
        :type age: int
        :param email: Updated email address of the instructor
        :type email: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('UPDATE instructors SET name = ?, age = ?, email = ? WHERE instructor_id = ?', 
                            (name, age, email, instructor_id))
        self.conn.commit()

    def delete_instructor(self, instructor_id):
        """Deletes an instructor from the database.

        :param instructor_id: Unique identifier for the instructor to delete
        :type instructor_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('DELETE FROM instructors WHERE instructor_id = ?', (instructor_id,))
        self.conn.commit()

    def create_course(self, course_id, course_name, instructor_id):
        """Creates a new course in the database.

        :param course_id: Unique identifier for the course
        :type course_id: str
        :param course_name: Name of the course
        :type course_name: str
        :param instructor_id: Unique identifier for the instructor teaching the course
        :type instructor_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('INSERT INTO courses VALUES (?, ?, ?)', (course_id, course_name, instructor_id))
        self.conn.commit()

    def read_course(self, course_id):
        """Reads a course's information from the database.

        :param course_id: Unique identifier for the course
        :type course_id: str
        :return: Course information as a tuple
        :rtype: tuple or None
        """
        self.cursor.execute('SELECT * FROM courses WHERE course_id = ?', (course_id,))
        return self.cursor.fetchone()

    def update_course(self, course_id, course_name, instructor_id):
        """Updates an existing course in the database.

        :param course_id: Unique identifier for the course
        :type course_id: str
        :param course_name: Updated name of the course
        :type course_name: str
        :param instructor_id: Updated instructor ID for the course
        :type instructor_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('UPDATE courses SET course_name = ?, instructor_id = ? WHERE course_id = ?', 
                            (course_name, instructor_id, course_id))
        self.conn.commit()

    def delete_course(self, course_id):
        """Deletes a course from the database.

        :param course_id: Unique identifier for the course to delete
        :type course_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('DELETE FROM courses WHERE course_id = ?', (course_id,))
        self.conn.commit()

    def register_student(self, student_id, course_id):
        """Registers a student for a course.

        :param student_id: Unique identifier for the student
        :type student_id: str
        :param course_id: Unique identifier for the course
        :type course_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('INSERT INTO registrations VALUES (?, ?)', (student_id, course_id))
        self.conn.commit()

    def unregister_student(self, student_id, course_id):
        """Unregisters a student from a course.

        :param student_id: Unique identifier for the student
        :type student_id: str
        :param course_id: Unique identifier for the course
        :type course_id: str
        :return: None
        :rtype: None
        """
        self.cursor.execute('DELETE FROM registrations WHERE student_id = ? AND course_id = ?', (student_id, course_id))
        self.conn.commit()

    def get_student_courses(self, student_id):
        """Retrieves all courses for a specific student.

        :param student_id: Unique identifier for the student
        :type student_id: str
        :return: List of courses the student is enrolled in
        :rtype: list
        """
        self.cursor.execute('''
            SELECT c.* FROM courses c
            JOIN registrations r ON c.course_id = r.course_id
            WHERE r.student_id = ?
        ''', (student_id,))
        return self.cursor.fetchall()

    def get_course_students(self, course_id):
        """Retrieves all students enrolled in a specific course.

        :param course_id: Unique identifier for the course
        :type course_id: str
        :return: List of students enrolled in the course
        :rtype: list
        """
        self.cursor.execute('''
            SELECT s.* FROM students s
            JOIN registrations r ON s.student_id = r.student_id
            WHERE r.course_id = ?
        ''', (course_id,))
        return self.cursor.fetchall()

    def get_all_students(self):
        """Retrieves all students from the database.

        :return: A list of all students
        :rtype: list
        """
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()

    def get_all_instructors(self):
        """Retrieves all instructors from the database.

        :return: A list of all instructors
        :rtype: list
        """
        self.cursor.execute('SELECT * FROM instructors')
        return self.cursor.fetchall()

    def get_all_courses(self):
        """Retrieves all courses from the database.

        :return: A list of all courses
        :rtype: list
        """
        self.cursor.execute('SELECT * FROM courses')
        return self.cursor.fetchall()

    def export_to_csv(self, filename):
        """Exports all records to a CSV file.

        :param filename: The name of the CSV file to create
        :type filename: str
        :return: None
        :rtype: None
        """
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Type', 'ID', 'Name', 'Age', 'Email'])

            students = self.get_all_students()
            for student in students:
                csv_writer.writerow(['Student'] + list(student))

            instructors = self.get_all_instructors()
            for instructor in instructors:
                csv_writer.writerow(['Instructor'] + list(instructor))

            courses = self.get_all_courses()
            for course in courses:
                csv_writer.writerow(['Course', course[0], course[1], '', ''])

    def backup_database(self, backup_filename):
        """Creates a backup of the database.

        :param backup_filename: The name of the backup file
        :type backup_filename: str
        :return: None
        :rtype: None
        """
        with sqlite3.connect(backup_filename) as backup_conn:
            self.conn.backup(backup_conn)

    def load_database(self, filename):
        """Loads a database from a file.

        :param filename: The name of the file containing the database
        :type filename: str
        :return: None
        :rtype: None
        """
        new_conn = sqlite3.connect(filename)
        new_conn.backup(self.conn)
        new_conn.close()
        
    def search_records(self, search_term):
        """Searches for records matching a search term.

        :param search_term: The term to search for in student, instructor, and course records
        :type search_term: str
        :return: A list of matching records
        :rtype: list
        """
        search_term = f"%{search_term}%"
        self.cursor.execute('''
            SELECT 'Student' as type, student_id as id, name, age, email
            FROM students
            WHERE student_id LIKE ? OR name LIKE ? OR email LIKE ?
            UNION ALL
            SELECT 'Instructor' as type, instructor_id as id, name, age, email
            FROM instructors
            WHERE instructor_id LIKE ? OR name LIKE ? OR email LIKE ?
            UNION ALL
            SELECT 'Course' as type, course_id as id, course_name as name, '' as age, '' as email
            FROM courses
            WHERE course_id LIKE ? OR course_name LIKE ?
        ''', (search_term, search_term, search_term, search_term, search_term, search_term, search_term, search_term))
        return self.cursor.fetchall()

    def close(self):
        """Closes the database connection.

        :return: None
        :rtype: None
        """
        self.conn.close()
