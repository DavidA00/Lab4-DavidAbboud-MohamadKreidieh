import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import OOP as o


class MainApp:
    '''This class represents the main application. It uses functions to create each separate tab

    :param master: The parent frame that contains all the other tabs
    :type master: tk.Tk
    '''

    def __init__(self, master):
        '''
        Initializes the Main App
        :param master: The parent frame that contains all the other tabs
        :type master: tk.Tk
        '''

        self.master = master
        self.master.title("Course Management")
        self.master.geometry("1000x563")

        self.tabControl = tk.ttk.Notebook(master)
        self.tabControl.pack(expand=1, fill='both')

        self.createStudentTab()
        self.createInstructorTab()
        self.createCourseTab()
    
    def createStudentTab(self):
        '''
        creates the student management tab. This allows users to create students, and register them for classes. 
        It also displays the students in a table
        '''
        self.studentFrame = tk.Frame(self.tabControl)
        self.tabControl.add(self.studentFrame, text = "Students")

        tk.Label(self.studentFrame, text="Name:").grid(row = 0, column = 0)
        self.studentNameEntry = tk.Entry(self.studentFrame)
        self.studentNameEntry.grid(row = 0, column = 1)

        tk.Label(self.studentFrame, text="Age:").grid(row = 1, column = 0)
        self.studentAgeEntry = tk.Entry(self.studentFrame)
        self.studentAgeEntry.grid(row = 1, column = 1)

        tk.Label(self.studentFrame, text="Email:").grid(row = 2, column = 0)
        self.studentEmailEntry = tk.Entry(self.studentFrame)
        self.studentEmailEntry.grid(row = 2, column = 1)

        tk.Label(self.studentFrame, text="ID:").grid(row = 3, column = 0)
        self.studentIDEntry = tk.Entry(self.studentFrame)
        self.studentIDEntry.grid(row = 3, column = 1)

        tk.Button(self.studentFrame, text="Add Student", command=self.addStudent).grid(row=4, columnspan=2)

        tk.Label(self.studentFrame, text="--- Register for Courses ---").grid(row=6, columnspan=2)

        tk.Label(self.studentFrame, text="Student ID:").grid(row = 8, column = 0)
        self.studentIDRegistryEntry = tk.Entry(self.studentFrame)
        self.studentIDRegistryEntry.grid(row = 8, column = 1)

        tk.Label(self.studentFrame, text="Course:").grid(row = 9, column = 0)
        self.studentCourseDropdown = ttk.Combobox(self.studentFrame)
        self.studentCourseDropdown.grid(row = 9, column = 1)

        # courseOptions = [(course.course_name, course.course_id) for course in o.coursesStorage]
        # self.studentCourseDropdown['values'] = courseOptions
        # self.studentCourseDropdown.set("")
        self.refreshStudentCourseList()

        tk.Button(self.studentFrame, text="Register Course", command=self.registerCourse).grid(row=10, columnspan=2)

        # STUDENT DATABASE
        self.studentSearch = tk.Entry(self.studentFrame)
        self.studentSearch.grid(row = 0, column = 6)

        tk.Button(self.studentFrame, text="Search", command=self.searchStudent).grid(row=0, column=7)

        self.studentTable = ttk.Treeview(self.studentFrame, columns=("ID", "Name", "Age"), show = "headings")
        self.studentTable.heading("ID", text="ID")
        self.studentTable.heading("Name", text="Name")
        self.studentTable.heading("Age", text="Age")
        self.studentTable.grid(row=2, columnspan=1, column=5, rowspan=10, sticky='ns')

        tk.Label(self.studentFrame, text="Name:").grid(row = 14, column = 6)
        self.studentNameEdit = tk.Entry(self.studentFrame)
        self.studentNameEdit.grid(row = 14, column = 7)

        tk.Label(self.studentFrame, text="Age:").grid(row = 15, column = 6)
        self.studentAgeEdit = tk.Entry(self.studentFrame)
        self.studentAgeEdit.grid(row = 15, column = 7)

        # tk.Label(self.studentFrame, text="ID:").grid(row = 16, column = 6)
        # self.studentIDEdit = tk.Entry(self.studentFrame)
        # self.studentIDEdit.grid(row = 16, column = 7)
        # self.studentTable.configure(yscroll=self.scrollbar.set)

        tk.Button(self.studentFrame, text="Edit", command=self.editStudent).grid(row=17, column=6)

        self.studentTable.bind("<ButtonRelease-1>", self.selectStudent)

        tk.Button(self.studentFrame, text="Delete", bg="red", fg="white", command=self.deleteStudent).grid(row=17, column=7)

        self.refreshStudentTable()
    
    def deleteStudent(self):
        '''
        deletes the student selected in the table. It also un-enrolls them from any courses they are taking
        '''

        selectedStudent = self.studentTable.selection()
        if not selectedStudent:
            messagebox.showwarning("Edit Student", "Please select a student to edit.")
            return
        
        item = self.studentTable.item(selectedStudent)

        studentID = item['values'][0]
        student = o.studentsStorage[str(studentID)]

        for course in student.registered_courses:
            course.enrolled_students.remove(student)

        del o.studentsStorage[str(studentID)]

        self.refreshStudentTable()
    
    def selectStudent(self, event):
        '''
        This function is called when a student is selected (clicked on) in the table. 
        If not student is selected, it shows a warning, and returns
        Otherwise, it finds the name of the student, and fills the edit fields with the student's information (name and age), allowing users to edit them
        '''

        selectedStudent = self.studentTable.selection()
        if not selectedStudent:
            messagebox.showwarning("Edit Student", "Please select a student to edit.")
            return
    
        item = self.studentTable.item(selectedStudent)

        studentID = item['values'][0]
        studentName = item['values'][1]
        studentAge = item['values'][2]

        # self.studentIDEdit.delete(0, tk.END)
        # self.studentIDEdit.insert(tk.END, studentID)

        self.studentNameEdit.delete(0, tk.END)
        self.studentNameEdit.insert(tk.END, studentName)

        self.studentAgeEdit.delete(0, tk.END)
        self.studentAgeEdit.insert(tk.END, studentAge)

    def searchStudent(self):
        '''
        searches for a student with a name or ID which matches the value in the search bar
        Fills the table with only the matching students
        '''

        searchText = self.studentSearch.get().lower()

        for row in self.studentTable.get_children():
            self.studentTable.delete(row)

        for student in o.studentsStorage.values():
            if student.name == searchText or student.student_id == searchText:
                self.studentTable.insert("", "end", values=(student.student_id, student.name, student.age))

    def refreshStudentCourseList(self):
        '''
        This refreshes the list of courses, that will be displayed when registering a student
        '''

        courseOptions = [courseName for courseName in o.courseNameStorage.keys()]
        self.studentCourseDropdown['values'] = courseOptions
        self.studentCourseDropdown.set("")

    def refreshStudentTable(self):
        '''
        Refreshes the student table, showing any new students
        To be called when new students are added, or existing students are edited or deleted
        '''

        for row in self.studentTable.get_children():
            self.studentTable.delete(row)
        
        for student in o.studentsStorage.values():
            self.studentTable.insert("", "end", values=(student.student_id, student.name, student.age))
    
    def editStudent(self):
        '''
        Edits the selected student, changing their name and age to the new values entered by the user in the edit fields
        If not student is selected, a warning will display, asking the user to select a student
        '''

        selectedStudent = self.studentTable.selection()
        if not selectedStudent:
            messagebox.showwarning("Edit Student", "Please select a student to edit.")
            return
    
        item = self.studentTable.item(selectedStudent)

        studentID = item['values'][0]
        print("Student ID:", studentID)
        print(o.studentsStorage)
        student = o.studentsStorage[str(studentID)]

        # newID = self.studentIDEdit
        newName = self.studentNameEdit.get()
        newAge = self.studentAgeEdit.get()

        student.name = newName
        student.age = newAge

        self.refreshStudentTable()
    
    def addStudent(self):
        '''
        Adds a new student, with the data entered by the user
        Displays an error if any necessary fields are empty, or if the ID provided is already in use
        Displays a success message on successful completion of the creation
        :raised ValueError: If the input is invalid
        '''
        try:
            studentName = self.studentNameEntry.get()
            studentAge = int(self.studentAgeEntry.get())
            studentEmail = self.studentEmailEntry.get()
            studentID = self.studentIDEntry.get()

            if(studentName != None and studentName != "" and studentAge != None and studentEmail != None and studentEmail != "" and studentID != None and studentID != ""):
                if studentID in o.studentsStorage:
                    messagebox.showerror("Invalid ID", "ID already in use. Please enter a valid ID")
                
                else:
                    newStudent = o.Student(studentName, studentAge, studentEmail, studentID)
                    messagebox.showinfo("Success!", "Student added successfully!")
                    self.refreshStudentTable()
            
            else:
                messagebox.showerror("Error", "Invalid ID: Please enter all values")
        except ValueError as ve:
            messagebox.showerror("Error", "Invalid Entry: please enter correct values")
    
    def registerCourse(self):
        '''
        Registers the student for a course. It takes the student, and course as inputs from the form.
        It will show an error message if the student ID is invalid, or if no course is selected
        '''

        courseName = self.studentCourseDropdown.get()
        studentID = self.studentIDRegistryEntry.get()
        if(not studentID in o.studentsStorage):
            messagebox.showerror("Error", "Invalid Student ID: Please enter a valid student ID")
        elif(courseName != None and courseName != ""):
            course = o.courseNameStorage[courseName]
            course.add_student(o.studentsStorage[studentID])
            student = o.studentsStorage[studentID]
            student.registerCourse(course)
            print(student.registered_courses)
        else:
            messagebox.showerror("Invalid Course", "Please select a valid course")

    def createInstructorTab(self):
        '''
        Creates the instructor tab, and loads the values for the course options, and the table
        '''
        self.instructorFrame = tk.Frame(self.tabControl)
        self.tabControl.add(self.instructorFrame, text = "Instructors")

        tk.Label(self.instructorFrame, text="Name:").grid(row = 0, column = 0)
        self.instructorNameEntry = tk.Entry(self.instructorFrame)
        self.instructorNameEntry.grid(row = 0, column = 1)

        tk.Label(self.instructorFrame, text="Age:").grid(row = 1, column = 0)
        self.instructorAgeEntry = tk.Entry(self.instructorFrame)
        self.instructorAgeEntry.grid(row = 1, column = 1)

        tk.Label(self.instructorFrame, text="Email:").grid(row = 2, column = 0)
        self.instructorEmailEntry = tk.Entry(self.instructorFrame)
        self.instructorEmailEntry.grid(row = 2, column = 1)

        tk.Label(self.instructorFrame, text="ID:").grid(row = 3, column = 0)
        self.instructorIDEntry = tk.Entry(self.instructorFrame)
        self.instructorIDEntry.grid(row = 3, column = 1)

        tk.Button(self.instructorFrame, text="Add Instructor", command=self.addInstructor).grid(row=4, columnspan=2)

        tk.Label(self.instructorFrame, text="--- Assign To Courses ---").grid(row=6, columnspan=2)

        tk.Label(self.instructorFrame, text="Instructor ID:").grid(row = 8, column = 0)
        self.instructorIDRegistryEntry = tk.Entry(self.instructorFrame)
        self.instructorIDRegistryEntry.grid(row = 8, column = 1)

        tk.Label(self.instructorFrame, text="Course:").grid(row = 9, column = 0)
        self.instructorCourseDropdown = ttk.Combobox(self.instructorFrame)
        self.instructorCourseDropdown.grid(row = 9, column = 1)

        # courseOptions = [(course.course_name, course.course_id) for course in o.coursesStorage]
        # self.studentCourseDropdown['values'] = courseOptions
        # self.studentCourseDropdown.set("")
        self.refreshInstructorCourseList()

        tk.Button(self.instructorFrame, text="Assign Course", command=self.assignCourse).grid(row=10, columnspan=2)

        # INSTUCTOR TABLE

        self.instructorSearch = tk.Entry(self.instructorFrame)
        self.instructorSearch.grid(row = 0, column = 6)

        tk.Button(self.instructorFrame, text="Search", command=self.searchInstructor).grid(row=0, column=7)

        self.instructorTable = ttk.Treeview(self.instructorFrame, columns=("ID", "Name", "Age"), show = "headings")
        self.instructorTable.heading("ID", text="ID")
        self.instructorTable.heading("Name", text="Name")
        self.instructorTable.heading("Age", text="Age")
        self.instructorTable.grid(row=1, columnspan=1, column=5, rowspan=10, sticky='ns')
        # self.studentTable.configure(yscroll=self.scrollbar.set)

        tk.Label(self.instructorFrame, text="Name:").grid(row = 14, column = 6)
        self.instructorNameEdit = tk.Entry(self.instructorFrame)
        self.instructorNameEdit.grid(row = 14, column = 7)

        tk.Label(self.instructorFrame, text="Age:").grid(row = 15, column = 6)
        self.instructorAgeEdit = tk.Entry(self.instructorFrame)
        self.instructorAgeEdit.grid(row = 15, column = 7)

        # tk.Label(self.studentFrame, text="ID:").grid(row = 16, column = 6)
        # self.studentIDEdit = tk.Entry(self.studentFrame)
        # self.studentIDEdit.grid(row = 16, column = 7)
        # self.studentTable.configure(yscroll=self.scrollbar.set)

        tk.Button(self.instructorFrame, text="Edit", command=self.editInstructor).grid(row=17, column=6)

        self.instructorTable.bind("<ButtonRelease-1>", self.selectInstructor)

        tk.Button(self.instructorFrame, text="Delete", bg="red", fg="white", command=self.deleteInstructor).grid(row=17, column=7)

        self.refreshInstructorTable()
    
    def deleteInstructor(self):
        '''
        Deletes the selected instructor
        Shows a warning if no instructor is selected
        Removes the instructor from all courses he is teaching, and then deletes him from the database
        Finally, it refreshes the instructor  table, to show its new values. It also refreshes the courses table, to update the Instructor column
        '''
        
        selectedInstructor = self.instructorTable.selection()
        if not selectedInstructor:
            messagebox.showwarning("Delete Instructor", "Please select an instructor to Delete.")
            return
        
        item = self.instructorTable.item(selectedInstructor)

        instructorID = item['values'][0]
        instructor = o.InstructorsStorage[str(instructorID)]

        for course in instructor.assigned_courses:
            if course.instructor == instructor:
                course.instructor = None
        
        print("right before instructor deletion")

        del o.InstructorsStorage[str(instructorID)]

        print("right before table refresh")

        self.refreshCourseTable()
        print("between table refresh")
        self.refreshInstructorTable()
        print("after table refresh")

    def selectInstructor(self, event):
        '''
        When an instructor is selected, this will copy their name and age into the edit fields, so the user can modify them
        Shows a warning if no instructor is selected
        Empties the edit fields, then replaces them with the name and age of the selected instructor
        '''

        selectedInstructor = self.instructorTable.selection()
        if not selectedInstructor:
            messagebox.showwarning("Edit Instructor", "Please select an instructor to edit.")
            return
    
        item = self.instructorTable.item(selectedInstructor)

        instructorID = item['values'][0]
        instructorName = item['values'][1]
        instructorAge = item['values'][2]

        # self.studentIDEdit.delete(0, tk.END)
        # self.studentIDEdit.insert(tk.END, studentID)

        print("REACHED HERE")

        self.instructorNameEdit.delete(0, tk.END)
        self.instructorNameEdit.insert(tk.END, instructorName)

        self.instructorAgeEdit.delete(0, tk.END)
        self.instructorAgeEdit.insert(tk.END, instructorAge)
    
    def editInstructor(self):
        '''
        Edits the selected instructor. This changes the instructor's name and age to those entered by the user in the edit fields
        Shows a warning if no instructor is selected
        This also refreshes the instructor table, to update its values, as well as the courses table (in case the name was changed)
        '''

        selectedInstructor = self.instructorTable.selection()
        if not selectedInstructor:
            messagebox.showwarning("Edit Instructor", "Please select an Instructor to edit.")
            return
    
        item = self.instructorTable.item(selectedInstructor)

        instructorID = item['values'][0]
        print("Instructor ID:", instructorID)
        print(o.InstructorsStorage)
        instructor = o.InstructorsStorage[str(instructorID)]

        # newID = self.studentIDEdit
        newName = self.instructorNameEdit.get()
        newAge = self.instructorAgeEdit.get()

        instructor.name = newName
        instructor.age = newAge

        self.refreshInstructorTable()
        self.refreshCourseTable()
    
    def searchInstructor(self):
        '''
        This searches the instructor table for instructors with a matching name or ID.
        It then displays only the fields with a matching name or ID in the table
        '''

        searchText = self.instructorSearch.get().lower()

        for row in self.instructorTable.get_children():
            self.instructorTable.delete(row)

        for instructor in o.InstructorStorage.values():
            if instructor.name == searchText or instructor.instructor_id == searchText:
                self.instructorTable.insert("", "end", values=(instructor.student_id, instructor.name, instructor.age))
    
    def refreshInstructorCourseList(self):
        '''
        Refreshes the list of courses available for an instructor to be assigned to
        '''
        courseOptions = [courseName for courseName in o.courseNameStorage.keys()]
        self.instructorCourseDropdown['values'] = courseOptions
        # self.instructorCourseDropdown.set("")
    
    def refreshInstructorTable(self):
        '''
        Refreshes the instructor table, displaying all the instructors
        '''

        for row in self.instructorTable.get_children():
            self.instructorTable.delete(row)
        
        for instructor in o.InstructorsStorage.values():
            self.instructorTable.insert("", "end", values=(instructor.instructor_id, instructor.name, instructor.age))
    
    def addInstructor(self):
        '''
        Adds a new instructor to the database, using data in the form fields
        Displays an Invalid ID error if the ID is already in use
        Displays an error message if any values are invalid, or any required fields are left empty
        Displays a success message upon successfully creating an instructor, and refreshes the instructor table
        Finally, it refreshes the instructor table to show any changes

        :raises ValueError: if the inputted values are invalid (e.g. negative date, invalid email)
        '''
        try:
            instructorName = self.instructorNameEntry.get()
            instructorAge = int(self.instructorAgeEntry.get())
            instructorEmail = self.instructorEmailEntry.get()
            instructorID = self.instructorIDEntry.get()

            if(instructorName != None and instructorName != "" and instructorAge != None and instructorEmail != None and instructorEmail != "" and instructorID != None and instructorID != ""):
                
                if instructorID in o.InstructorsStorage:
                    messagebox.showerror("Invalid ID", "ID already in use. Please enter a valid ID")
                
                else:
                    newInstructor = o.Instructor(instructorName, instructorAge, instructorEmail, instructorID)
                    messagebox.showinfo("Success!", "Instructor added successfully!")
                    self.refreshInstructorTable()
            
            else:
                messagebox.showerror("Error", "Empty Value: Please enter all values")
        except ValueError as ve:
            messagebox.showerror("Error", "Invalid Entry: please enter correct values")
    
    def assignCourse(self):
        '''
        Assigns a course to an instructor
        Displays an error if the instructor ID is not valid (no instructor with this ID exists), or if no course is selected
        Otherwise, assigns the course to the instructor'''
        courseName = self.instructorCourseDropdown.get()
        instructorID = self.instructorIDRegistryEntry.get()
        if(not instructorID in o.InstructorsStorage):
            messagebox.showerror("Error", "Invalid Instructor ID: Please enter a valid student ID")
        elif(courseName != None and courseName != ""):
            course = o.courseNameStorage[courseName]
            course.assignInstructor(o.InstructorsStorage[instructorID])
            instructor = o.InstructorsStorage[instructorID]
            # instructor.assignCourse(course)
            # print(student.registered_courses)
            print(instructor.assigned_courses)
        else:
            messagebox.showerror("Invalid Course", "Please select a valid course")
    
    def createCourseTab(self):
        '''
        Creates the course tab, to create new courses, and display existing courses, as well as edit and delete any existing courses
        '''
        self.courseFrame = tk.Frame(self.tabControl)
        self.tabControl.add(self.courseFrame, text = "Courses")

        tk.Label(self.courseFrame, text="Name:").grid(row = 0, column = 0)
        self.courseNameEntry = tk.Entry(self.courseFrame)
        self.courseNameEntry.grid(row = 0, column = 1)

        tk.Label(self.courseFrame, text="Instructor ID:").grid(row = 1, column = 0)
        self.courseInstructorEntry = tk.Entry(self.courseFrame)
        self.courseInstructorEntry.grid(row = 1, column = 1)

        tk.Label(self.courseFrame, text="ID:").grid(row = 3, column = 0)
        self.courseIDEntry = tk.Entry(self.courseFrame)
        self.courseIDEntry.grid(row = 3, column = 1)

        tk.Button(self.courseFrame, text="Add Course", command=self.addCourse).grid(row=4, columnspan=2)

        # COURSE DATABASE

        self.courseSearch = tk.Entry(self.courseFrame)
        self.courseSearch.grid(row = 0, column = 6)

        tk.Button(self.courseFrame, text="Search", command=self.searchCourse).grid(row=0, column=7)

        self.courseTable = ttk.Treeview(self.courseFrame, columns=("ID", "Name", "Instructor"), show = "headings")
        self.courseTable.heading("ID", text="ID")
        self.courseTable.heading("Name", text="Name")
        self.courseTable.heading("Instructor", text="Instructor")
        self.courseTable.grid(row=1, columnspan=1, column=5, rowspan=10, sticky='ns')
        # self.studentTable.configure(yscroll=self.scrollbar.set)

        tk.Label(self.courseFrame, text="Name:").grid(row = 14, column = 6)
        self.courseNameEdit = tk.Entry(self.courseFrame)
        self.courseNameEdit.grid(row = 14, column = 7)

        # tk.Label(self.studentFrame, text="ID:").grid(row = 16, column = 6)
        # self.studentIDEdit = tk.Entry(self.studentFrame)
        # self.studentIDEdit.grid(row = 16, column = 7)
        # self.studentTable.configure(yscroll=self.scrollbar.set)

        tk.Button(self.courseFrame, text="Edit", command=self.editCourse).grid(row=17, column=6)

        self.courseTable.bind("<ButtonRelease-1>", self.selectCourse)

        tk.Button(self.courseFrame, text="Delete", bg="red", fg="white", command=self.deleteCourse).grid(row=17, column=7)

        self.refreshCourseTable()
    
    def deleteCourse(self):
        '''
        Deletes the selected course in the courses table
        If no course is selected, a warning is displayed
        Finally, it refreshes the courses table, to display the changes
        '''
        selectedCourse = self.courseTable.selection()
        if not selectedCourse:
            messagebox.showwarning("Delete Course", "Please select a course to delete.")
            return
        
        item = self.courseTable.item(selectedCourse)

        courseID = item['values'][0]
        course = o.coursesStorage[str(courseID)]

        for student in course.enrolled_students:
            student.registered_courses.remove(course)
        
        if course.instructor != None:
            course.instructor.assigned_courses.remove(course)

        del o.coursesStorage[str(courseID)]

        self.refreshCourseTable()
    
    def selectCourse(self, event):
        '''
        When a course in the table is selected, retrieve the data of the course, and copy them to the edit field, for the user to modify them
        If no course is selected, display a warning
        '''
        selectedCourse = self.courseTable.selection()
        if not selectedCourse:
            messagebox.showwarning("Edit Course", "Please select a course to edit.")
            return
    
        item = self.courseTable.item(selectedCourse)

        courseID = item['values'][0]
        courseName = item['values'][1]

        # self.studentIDEdit.delete(0, tk.END)
        # self.studentIDEdit.insert(tk.END, studentID)

        print("REACHED HERE")

        self.courseNameEdit.delete(0, tk.END)
        self.courseNameEdit.insert(tk.END, courseName)
    
    def editCourse(self):
        '''
        Edits the selected course, replacing the course name with that in the Edit Field
        Displays a warning to the user if no course is selected, and returns without editing the course
        Displays an error to the user if a course with the entered name already exists, and returns without editing the course
        When completed, if any changes were made, refreshes the courses table
        '''
        selectedCourse = self.courseTable.selection()
        if not selectedCourse:
            messagebox.showwarning("Edit Course", "Please select a course to edit.")
            return
    
        item = self.courseTable.item(selectedCourse)

        courseID = item['values'][0]
        courseName = item['values'][1]
        print("Course ID:", courseID)
        print(o.coursesStorage)
        course = o.coursesStorage[str(courseID)]

        # newID = self.studentIDEdit
        newName = self.courseNameEdit.get()

        if(not newName in o.courseNameStorage):
            course.course_name = newName
            del o.courseNameStorage[str(courseName)]
            o.courseNameStorage[newName] = course
        else:
            messagebox.showerror("error", "A course with this name already exists. Please enter a unique name")

        self.refreshCourseTable()
    
    def searchCourse(self):
        '''
        Searches for a course with the same ID or name as that provided
        Clears the table and only displays courses that match this criteria
        If no instructor is assigned to the course, the instructor tab will show "N/A". Otherwise, it will show the name of the professor assigned
        '''
        searchText = self.courseSearch.get().lower()

        for row in self.courseTable.get_children():
            self.courseTable.delete(row)

        for course in o.coursesStorage.values():
            if course.course_name == searchText or course.course_id == searchText:
                if course.instructor == None:
                    self.courseTable.insert("", "end", values=(course.course_id, course.course_name, "N/A"))
                else:
                    self.courseTable.insert("", "end", values=(course.course_id, course.course_name, course.instructor.name))
    
    def refreshCourseTable(self):
        '''
        Displays all available courses in the table
        If no instructor is assigned to the course, the instructor tab will show "N/A". Otherwise, it will show the name of the professor assigned
        '''
        for row in self.courseTable.get_children():
            self.courseTable.delete(row)
        
        for course in o.coursesStorage.values():
            if course.instructor == None:
                self.courseTable.insert("", "end", values=(course.course_id, course.course_name, "N/A"))
            else:
                self.courseTable.insert("", "end", values=(course.course_id, course.course_name, course.instructor.name))
    
    def addCourse(self):
        '''
        Adds a course to the database, using the inputs provided in the user entered fields
        Displays an error if the course name or ID is already in user, and returns without creating the course
        Displays an error if an instructor ID is provided, but the ID is invalid, and returns without creating the course
        Displays an error if there are empty fields, which are required, or if the inputted data is invalid, and returns without creating the course
        Otherwise, creates the course and displays a success message. Then, it refreshes the courses table, as well as the courses list for the students and instructor pages
        '''
        try:
            courseName = self.courseNameEntry.get()
            courseInstructor = self.courseInstructorEntry.get()
            courseID = self.courseIDEntry.get()

            if(courseName != None and courseName != "" and courseID != None and courseID != ""):
                
                if courseID in o.coursesStorage or courseName in o.courseNameStorage:
                    messagebox.showerror("Invalid ID or Name", "Course ID or Name already in use. Please enter a valid ID and Name")
                
                else:
                    if courseInstructor != None and courseInstructor != "" and not courseInstructor in o.InstructorsStorage:
                        messagebox.showerror("Invalid Instructor", "No instructor with this ID exists. Please enter a valid instructor ID")
                    
                    elif courseInstructor == None or courseInstructor == "":
                        newCourse = o.Course(courseID, courseName, None)
                        messagebox.showinfo("Success!", "Course added successfully!")

                        self.refreshStudentCourseList()
                        self.refreshInstructorCourseList()

                        self.refreshCourseTable()

                    else:
                        newCourse = o.Course(courseID, courseName, o.InstructorsStorage[courseInstructor])
                        messagebox.showinfo("Success!", "Course added successfully!")

                        self.refreshStudentCourseList()
                        self.refreshInstructorCourseList()

                        self.refreshCourseTable()
            else:
                messagebox.showerror("Error", "Empty Value: Please enter all values")
        except ValueError as ve:
            messagebox.showerror("Error", "Invalid Entry: please enter correct values")
    
    def onTabChanged(self, event):
        selected_tab = self.tabControl.tab(self.tabControl.select(), "text")
        if selected_tab == "Students":
            self.refreshCourseDropdown()


# root = tk.Tk()
# root.title("Management System")
# root.geometry("1000x563")
# root.mainloop()

root = tk.Tk()
app = MainApp(root)
root.mainloop()


# instructor = o.Instructor("Prof. Smith", 45, "smith@example.com", "I001")
# instructor.introduce()

# course = o.Course("C101", "Math", instructor)
# print(course.course_name)

# instructor.assignCourse(course)

# student = o.Student("MK", 21, "mik30@mail.aub.edu.lb", "202202363", [course])

# for c in student.registered_courses:
#     print(c.instructor.name)