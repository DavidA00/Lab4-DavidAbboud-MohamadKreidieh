import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QComboBox, QTableWidget, QAction, 
                             QTabWidget, QFormLayout, QMessageBox, QFileDialog)


from david.database import Database
import os

class SchoolManagementGUI(QMainWindow):
    """
    This class represents the main window for the School Management System GUI.

    It provides the graphical interface for managing students, instructors, courses, 
    and registrations in a school environment. Users can add, edit, delete, and display records,
    as well as export and back up the database.

    :param db: An instance of the Database class for data storage
    :type db: Database
    :param student_name: Input field for the student's name
    :type student_name: QLineEdit
    :param student_age: Input field for the student's age
    :type student_age: QLineEdit
    :param student_email: Input field for the student's email
    :type student_email: QLineEdit
    :param student_id: Input field for the student's ID
    :type student_id: QLineEdit
    :param instructor_name: Input field for the instructor's name
    :type instructor_name: QLineEdit
    :param instructor_age: Input field for the instructor's age
    :type instructor_age: QLineEdit
    :param instructor_email: Input field for the instructor's email
    :type instructor_email: QLineEdit
    :param instructor_id: Input field for the instructor's ID
    :type instructor_id: QLineEdit
    :param course_id: Input field for the course ID
    :type course_id: QLineEdit
    :param course_name: Input field for the course name
    :type course_name: QLineEdit
    :param course_instructor: Dropdown for selecting the course instructor
    :type course_instructor: QComboBox
    :param reg_student: Dropdown for selecting a student during registration
    :type reg_student: QComboBox
    :param reg_course: Dropdown for selecting a course during registration
    :type reg_course: QComboBox
    :param records_table: Table displaying all records
    :type records_table: QTableWidget
    """

    def __init__(self):
        """
        Initializes the SchoolManagementGUI class and sets up the main window for the application.

        :raises IOError: If the database file is not found
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)
        self.db = Database('school.db')

        if os.path.exists('gui_2.sql'):
            self.db.load_database('gui_2.sql')
        else:
            print("Warning: gui_2.sql not found. Starting with an empty database.")

        self.init_ui()

    def init_ui(self):
        """
        Initializes the main UI components, including tabs for students, instructors, courses, and registrations.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tabs
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Student tab
        student_tab = QWidget()
        tabs.addTab(student_tab, "Students")
        student_layout = QVBoxLayout(student_tab)
        self.setup_student_form(student_layout)

        # Instructor tab
        instructor_tab = QWidget()
        tabs.addTab(instructor_tab, "Instructors")
        instructor_layout = QVBoxLayout(instructor_tab)
        self.setup_instructor_form(instructor_layout)

        # Course tab
        course_tab = QWidget()
        tabs.addTab(course_tab, "Courses")
        course_layout = QVBoxLayout(course_tab)
        self.setup_course_form(course_layout)

        # Registration tab
        registration_tab = QWidget()
        tabs.addTab(registration_tab, "Registration")
        registration_layout = QVBoxLayout(registration_tab)
        self.setup_registration_form(registration_layout)

        # Display tab
        display_tab = QWidget()
        tabs.addTab(display_tab, "Display Records")
        display_layout = QVBoxLayout(display_tab)
        self.setup_display_tab(display_layout)

        # Setup menu
        self.setup_menu()
        self.refresh_display()
        self.update_all_dropdowns()

    def setup_student_form(self, layout):
        """
        Sets up the form for adding a student.

        :param layout: The layout to add the form fields and button to
        :type layout: QVBoxLayout
        """
        form_layout = QFormLayout()
        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()
        form_layout.addRow("Name:", self.student_name)
        form_layout.addRow("Age:", self.student_age)
        form_layout.addRow("Email:", self.student_email)
        form_layout.addRow("Student ID:", self.student_id)
        layout.addLayout(form_layout)

        add_button = QPushButton("Add Student")
        add_button.clicked.connect(self.add_student)
        layout.addWidget(add_button)

    def add_student(self):
        """
        Adds a new student to the database using the input fields for name, age, email, and student ID.

        :raises ValueError: If the age is not an integer or if an input field is left empty.
        """
        try:
            self.db.create_student(
                self.student_id.text(),
                self.student_name.text(),
                int(self.student_age.text()),
                self.student_email.text()
            )
            QMessageBox.information(self, "Success", "Student added successfully!")
            self.clear_student_fields()
            self.refresh_display()
            self.update_registration_dropdowns()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def setup_instructor_form(self, layout):
        """
        Sets up the form for adding an instructor.

        :param layout: The layout to add the form fields and button to
        :type layout: QVBoxLayout
        """
        form_layout = QFormLayout()
        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()
        form_layout.addRow("Name:", self.instructor_name)
        form_layout.addRow("Age:", self.instructor_age)
        form_layout.addRow("Email:", self.instructor_email)
        form_layout.addRow("Instructor ID:", self.instructor_id)
        layout.addLayout(form_layout)

        add_button = QPushButton("Add Instructor")
        add_button.clicked.connect(self.add_instructor)
        layout.addWidget(add_button)

    def add_instructor(self):
        """
        Adds a new instructor to the database using the input fields for name, age, email, and instructor ID.

        :raises ValueError: If the age is not an integer or if an input field is left empty.
        """
        try:
            self.db.create_instructor(
                self.instructor_id.text(),
                self.instructor_name.text(),
                int(self.instructor_age.text()),
                self.instructor_email.text()
            )
            QMessageBox.information(self, "Success", "Instructor added successfully!")
            self.clear_instructor_fields()
            self.refresh_display()
            self.update_instructor_dropdown()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def setup_course_form(self, layout):
        """
        Sets up the form for adding a course.

        :param layout: The layout to add the form fields and button to
        :type layout: QVBoxLayout
        """
        form_layout = QFormLayout()
        self.course_id = QLineEdit()
        self.course_name = QLineEdit()
        self.course_instructor = QComboBox()
        form_layout.addRow("Course ID:", self.course_id)
        form_layout.addRow("Course Name:", self.course_name)
        form_layout.addRow("Instructor:", self.course_instructor)
        layout.addLayout(form_layout)

        add_button = QPushButton("Add Course")
        add_button.clicked.connect(self.add_course)
        layout.addWidget(add_button)

    def add_course(self):
        """
        Adds a new course to the database using the input fields for course ID, name, and selected instructor.

        :raises ValueError: If there is an issue with the provided input values.
        """
        try:
            instructor_name = self.course_instructor.currentText()
            instructor = self.db.read_instructor(instructor_name.split('(')[-1].strip(')'))
            self.db.create_course(
                self.course_id.text(),
                self.course_name.text(),
                instructor[0] if instructor else None
            )
            QMessageBox.information(self, "Success", "Course added successfully!")
            self.clear_course_fields()
            self.refresh_display()
            self.update_registration_dropdowns()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def setup_registration_form(self, layout):
        """
        Sets up the form for registering a student in a course.

        :param layout: The layout to add the form fields and button to
        :type layout: QVBoxLayout
        """
        form_layout = QFormLayout()
        self.reg_student = QComboBox()
        self.reg_course = QComboBox()
        form_layout.addRow("Student:", self.reg_student)
        form_layout.addRow("Course:", self.reg_course)
        layout.addLayout(form_layout)

        reg_button = QPushButton("Register Student")
        reg_button.clicked.connect(self.register_student)
        layout.addWidget(reg_button)

    def register_student(self):
        """
        Registers a selected student for a selected course in the database.

        :raises ValueError: If the student or course selection is invalid or missing.
        """
        try:
            student_name = self.reg_student.currentText()
            course_name = self.reg_course.currentText()
            student = self.db.read_student(student_name.split('(')[-1].strip(')'))
            course = self.db.read_course(course_name.split('(')[-1].strip(')'))
            if not student or not course:
                raise ValueError("Invalid student or course selection.")

            self.db.register_student(student[0], course[0])
            QMessageBox.information(self, "Success", f"{student_name} registered in {course_name} successfully!")
            self.refresh_display()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def setup_display_tab(self, layout):
        """
        Sets up the display table for showing all records of students, instructors, courses, and registrations.

        :param layout: The layout to add the display table to
        :type layout: QVBoxLayout
        """
        self.records_table = QTableWidget()
        layout.addWidget(self.records_table)

    def setup_menu(self):
        """
        Sets up the main menu with options for database backup and export.
        """
        main_menu = self.menuBar()

        # File menu
        file_menu = main_menu.addMenu('File')

        # Export Database Action
        export_action = QAction('Export Database', self)
        export_action.triggered.connect(self.export_database)
        file_menu.addAction(export_action)

        # Backup Database Action
        backup_action = QAction('Backup Database', self)
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_action)

    def refresh_display(self):
        """
        Refreshes the records displayed in the records table, showing the latest student, instructor, course,
        and registration information from the database.
        """
        self.records_table.clear()
        records = self.db.get_all_records()
        self.records_table.setRowCount(len(records))
        self.records_table.setColumnCount(5)
        self.records_table.setHorizontalHeaderLabels(['Type', 'ID', 'Name', 'Age', 'Other'])

        for row_idx, record in enumerate(records):
            for col_idx, item in enumerate(record):
                self.records_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def export_database(self):
        """
        Exports the current database to a selected file location.

        :raises IOError: If there is an issue with saving the file to the specified location.
        """
        try:
            file_dialog = QFileDialog.getSaveFileName(self, "Export Database", "", "SQL Files (*.sql)")
            file_path = file_dialog[0]
            if file_path:
                self.db.save_database(file_path)
                QMessageBox.information(self, "Success", "Database exported successfully!")
        except IOError as e:
            QMessageBox.warning(self, "Error", str(e))

    def backup_database(self):
        """
        Creates a backup of the current database by saving it to a predefined backup file.

        :raises IOError: If there is an issue during the backup process.
        """
        try:
            backup_path = 'backup.sql'
            self.db.save_database(backup_path)
            QMessageBox.information(self, "Success", "Database backed up successfully!")
        except IOError as e:
            QMessageBox.warning(self, "Error", str(e))

    def update_all_dropdowns(self):
        """
        Updates all dropdowns (comboboxes) used for student, instructor, and course selection.
        """
        self.update_student_dropdown()
        self.update_instructor_dropdown()
        self.update_registration_dropdowns()

    def update_student_dropdown(self):
        """
        Updates the dropdown list for student selection by fetching the latest students from the database.
        """
        self.reg_student.clear()
        students = self.db.read_all_students()
        for student in students:
            self.reg_student.addItem(f"{student[1]} ({student[0]})")

    def update_instructor_dropdown(self):
        """
        Updates the dropdown list for instructor selection by fetching the latest instructors from the database.
        """
        self.course_instructor.clear()
        instructors = self.db.read_all_instructors()
        for instructor in instructors:
            self.course_instructor.addItem(f"{instructor[1]} ({instructor[0]})")

    def update_registration_dropdowns(self):
        """
        Updates the dropdowns used for student and course selection during registration.
        """
        self.update_student_dropdown()
        self.reg_course.clear()
        courses = self.db.read_all_courses()
        for course in courses:
            self.reg_course.addItem(f"{course[1]} ({course[0]})")

    def clear_student_fields(self):
        """
        Clears the input fields in the student form.
        """
        self.student_name.clear()
        self.student_age.clear()
        self.student_email.clear()
        self.student_id.clear()

    def clear_instructor_fields(self):
        """
        Clears the input fields in the instructor form.
        """
        self.instructor_name.clear()
        self.instructor_age.clear()
        self.instructor_email.clear()
        self.instructor_id.clear()

    def clear_course_fields(self):
        """
        Clears the input fields in the course form.
        """
        self.course_id.clear()
        self.course_name.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = SchoolManagementGUI()
    gui.show()
    sys.exit(app.exec_())