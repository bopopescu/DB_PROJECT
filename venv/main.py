#Author:#################
#Assignment: Online Registration System Database Assignment
#Date: 06/05/2018

import sys, os, time
import mysql.connector
import functionsDB

cnx = mysql.connector.connect(user='dbproject',
                              password='1234pass',
                              host='127.0.0.1',
                              database='dbproject')
cursor = cnx.cursor()

#================
#   MENU HEADER
#================

print('Menu:')
print('*********************************************************************')
print('***                                                               ***')
print('***             Welcome to Online Registration System             ***')
print('***                                                               ***')
print('*********************************************************************')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

time.sleep(1)
#===================
#   MENU FUNCTIONS
#===================

def main_menu():

    functionsDB.printSpaces()
    print('******MAIN MENU******')
    print('\t 1. Add a course')
    print('\t 2. Delete a course')
    print('\t 3. Add a student')
    print('\t 4. Delete a student')
    print('\t 5. Register a course')
    print('\t 6. Drop a course')
    print('\t 7. Check student registration')
    print('\t 8. Upload grades')
    print('\t 9. Check grade')
    print('\t 10. Quit')

    choice = input(" >> ")
    exec_menu(choice)
    return

#Execute Menu
def exec_menu(choice):
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print('Invalid selection, please input a value between 1-10.\n')
            menu_actions['main_menu']()
    return

#Menu 1 :: ADD A COURSE
def menu1():

    print('Add a course: \n')
    course_code = input('Please input the course code you would like to add: ')
    if len(course_code) > 10 :
        print('Your course code seems to be too long, please input the code again!')
        input('Please input the course code you would like to add: ')
    course_title = input('Please input the title of the course you would like to add: ')
    if len(course_title) > 50:
        print('Your course title seems to be too long, please input the title again!')
        input('Please input the course title you would like to add: ')
    course_data = (course_code,course_title)
    add_course = ("INSERT INTO Course"
                  "(code, title)"
                  "VALUES (%s, %s)")
    try:
        cursor.execute(add_course, course_data)
        cnx.commit()
    except mysql.connector.IntegrityError as err:
        print('ERROR: {}'.format(err))

    print('Would you like to return to the main menu or add another course?')
    mini_sel = input("Press 1 to return to main menu or 2 to add another course: ")
    if mini_sel == '2':
        menu_actions['1']()
    else:
        menu_actions['main_menu']()
        choice = input(" >> ")
        exec_menu(choice)
    return

#Menu2 :: DELETE A COURSE
def menu2():

    print('\nDelete a course: \n')
    delete_mess = 'Current courses available to delete: '
    print('-' * len(delete_mess))
    print(delete_mess)
    print('-' * len(delete_mess))

    functionsDB.showCourse()
    print('\nPlease input the course code you would like to delete or nothing to return to main menu: ')
    course_code = input(" >> ")
    select_course = ("SELECT code, title FROM Course WHERE code = %s")
    cursor.execute(select_course, (course_code, ))
    if select_course == '':
        print('Error: No course selected, returning you to main menu')
        menu_actions['main_menu']()
    else:

        for (code, title) in cursor:
            print('You have selected to delete Course: \n')
            print(title)
            print('-' * len(title))
            selected_course = ('{}\t\t |\t{}'.format(code,title))
            print(selected_course)
        print("\nAre you sure you want to delete Course Code:",code,',Course Title:',title,'?')

        confirm_sel = input('Press Y for YES and N for NO')
        confirm_sel = confirm_sel.lower()

        if confirm_sel == 'y':
            try:
                code = course_code
                delete_course = ("DELETE FROM Course WHERE code = %s")
                cursor.execute(delete_course, (course_code, ))
                cnx.commit()
                print('\nCourse: ', code, 'has been deleted')
            except mysql.connector.Error as err:
                print('Error code: ', err)

            print('\nWould you like to return to the main menu or delete another course?\n')
            mini_sel = input("Press 1 to return to main menu or 2 to delete another course: \n")

            if mini_sel == '2':
                menu_actions['2']()
            else:
                menu_actions['main_menu']()

                exec_menu(choice)
        else:
            menu_actions['2']()
    return

#Menu3 :: ADD A STUDENT (SSN, name, address, major)
def menu3():

    print('Add a student:')
    ssn = input('Please enter the new students SSN: ')
    name = input('Please input the new students name: ')
    address = input('Please enter the new students address: ')
    major = input('Please input the new students major: ')

    new_student = (ssn, name, address, major)
    add_student = ("INSERT INTO Student"
                  "(ssn, name, address, major)"
                  "VALUES (%s, %s , %s, %s)")

    try:
        cursor.execute(add_student, new_student)
        cnx.commit()
        print('\nStudent: ', name, 'has been added')
    except mysql.connector.Error as err:
        print('Error code: ', err)

    print('Would you like to add another student? Y for YES and N for NO!')
    choice = input(' >> ')
    choice = choice.lower()
    if choice == 'y':
        menu_actions['3']()
    else:
        menu_actions['main_menu']()

#Menu4 :: DELETE STUDENT (BY SSN)
def menu4():

    print('Delete a student: ')
    functionsDB.showStuds()
    del_ssn = input('Please input the SSN of the student you would like to delete: ')
    print("\nAre you sure you want to delete Student SSN: ", del_ssn, '?')

    confirm_sel = input('Press Y for YES and N for NO')
    confirm_sel = confirm_sel.lower()

    try:
        delete_stud = ("DELETE FROM Student WHERE ssn = %s")
        cursor.execute(delete_stud, (del_ssn,))
        cnx.commit()
        print('\nStudent: ', del_ssn, 'has been deleted')
    except mysql.connector.Error as err:
        print('Error code: ', err)

    print('Would you like to delete another student? Y for YES and N for NO!')
    choice = input(' >> ')
    choice = choice.lower()
    if choice == 'y':
        menu_actions['4']()
    else:
        menu_actions['main_menu']()

#Register a course ((SSN), (code), year, semester)
def menu5():
    print("Register a student for a course: ")
    functionsDB.showStuds()
    selSSN = input('Please enter a SSN of the student you would like to register: (ENTER NOTHING TO RETURN TO THE MAIN MENU)')

    if selSSN == '':
        print('No course selected, returning you to main menu')
        menu_actions['main_menu']()
    else:
        print("Available courses to register: ")
        functionsDB.showCourse()
        selCC = input('Please input a course code you would like to register a student for:')
        selYear = input('Please input a year for the course registration: ')
        selSem = input('Spring | Summer | Fall: ')
        register_student = (selSSN, selCC, selYear, selSem)

        try:
            register_query = ("INSERT INTO Registered"
                            "(ssn, code, year, semester)"
                            "VALUES (%s, %s , %s, %s)")
            cursor.execute(register_query, register_student)
            cnx.commit()
            print('\nStudent: ', selSSN, 'has been registered for: ', selCC,"!")
        except mysql.connector.Error as err:
            print('Error code: ', err)

    print('Would you like to register another student? Y for YES and N for NO!')
    choice = input(' >> ')
    choice = choice.lower()
    if choice == 'y':
        menu_actions['5']()
    else:
        menu_actions['main_menu']()

#Menu6 :: Drop a student from a course (code, SSN, year, semester)
def menu6():

    print("Drop a student from a course: ")
    print("Current courses: ")
    functionsDB.showCourse()
    selCC = input('Please input a course code you would like to drop a student from: (ENTER NOTHING TO RETURN TO MAIN MENU)')

    if selCC == '':
        print('Error: No course selected, returning you to main menu')
        menu_actions['main_menu']()
    else:
        try:
            sel_course = ('SELECT ssn, year, semester FROM Registered WHERE code = %s')
            cursor.execute(sel_course, (selCC, ))

            print("\nStudents curently registered for ",selCC," :")
            reg_state = "Students:\t | Year: | Semester:"
            print(reg_state)
            print('-' * len(reg_state))
            for (ssn,year, semester) in cursor:
                current_reg = ('{}\t | {}\t | {}'.format(ssn, year, semester))
                print(current_reg)
            sel_SSN = input("Please input the Student's SSN you would like to drop the student from the course: ")
            sel_year =input("Please input the Year you would like to drop the student from the course: ")
            sel_sems = input("Please input the Semster you would like to drop the student from the course: ")

            drop_query = ('DELETE FROM Registered WHERE ssn = %s AND code = %s AND year = %s AND semester = %s')

            dropArgs = (sel_SSN, selCC, sel_year, sel_sems)
            drop_sel = input("Are you sure you want to drop this student from the course? [Y/N]")
            confirm_sel = drop_sel.lower()
            if confirm_sel == 'y':
                try:
                    cursor.execute(drop_query, dropArgs)
                    cnx.commit()
                    print(sel_SSN," has been droped from: ",selCC)
                except mysql.connector.Error as err:
                    print('Error code: ', err)
        except mysql.connector.Error as err:
            print('Error code: ', err)

        print('Would you like to drop another student? Y for YES and N for NO!')
        choice = input(' >> ')
        choice = choice.lower()
        if choice == 'y':
            menu_actions['6']()
        else:
            menu_actions['main_menu']()

#Menu 8 :: Check Student registration by entering ssn or name
def menu7():

    print("Check a Students registration: ")
    functionsDB.showStuds()
    sel7 = input('Check a students registration by name or ssn: (TYPE EITHER OR NOTHING TO RETURN TO MAIN MENU )')
    if sel7 == '':
        print('Error: No course selected, returning you to main menu')
        menu_actions['main_menu']()

    else:
        if sel8.isdigit():
            check_query = ('SELECT s.name, r.ssn, r.code, c.title, r.year, r.semester '
                           'FROM Student s, Registered r, Course c '
                           'WHERE s.ssn = r.ssn AND c.code = r.code AND r.ssn = {}'.format(sel8))
            try:
                cursor.execute(check_query)
                cnx.commit()
            except mysql.connector.Error as err:
                print('Error code: ', err)
            for (name, ssn, code, title, year, semester) in cursor:
                curent_reg = ('{} | {} | {} | {} | {} | {}'.format(name, ssn, code, year, semester, title))
                print(curent_reg)
        else:
            check_query = ('SELECT s.name, r.ssn, r.code, c.title, r.year, r.semester '
                           'FROM Student s, Registered r, Course c '
                           'WHERE s.ssn = r.ssn AND c.code = r.code AND s.name = %s')
            try:
                cursor.execute(check_query, (sel8, ))
                cnx.commit()

            except mysql.connector.Error as err:
                print('Error code: ', err)
            for (name, ssn, code, title, year, semester) in cursor:
                curent_reg = ('{} | {} | {}\t\t | {} | {} | {}'.format(name, ssn, code, year, semester, title))
                print(curent_reg)

        print('Would you like to check another student''s registration? Y for YES and N for NO!')
        choice = input(' >> ')
        choice = choice.lower()
        if choice == 'y':
            menu_actions['7']()
        else:
            menu_actions['main_menu']()

#Menu8 :: Upload grades (give code, year ,semster (then input grade for every registered student)
def menu8():

    print("Upload grades for students:")
    # functionsDB.showReg()
    sel8 = input("Please give course code of the class you would like to enter grades for: (ENTER NOTHING TO RETURN TO THE MAIN MENU)")
    if sel8 == '':
        print('Error: No course selected, returning you to main menu')
        menu_actions['main_menu']()
    else:
        sel8_year = input('Please select the course year: ')
        sel8_semester = input('Please input the course semester: ')
        sel8_args = (sel8, sel8_year, sel8_semester)
        try:
            sel8_q1 = 'SELECT ssn FROM Registered WHERE code = %s AND year = %s AND semester = %s'
            cursor.execute(sel8_q1, sel8_args)
            cnx.commit()
        except mysql.connector.Error as err:
            print('Error code: ', err)
        print('Please enter grades for students in course', sel8,': ')
        i = 0
        try:
            for ssn in cursor:
                sel8_grade = input('Please input grade for {}: '.format(ssn))
                update_grade = "UPDATE Registered SET grade = %s WHERE ssn = %s AND code = %s year = %s AND semester = %s"
                sel8_grade_args = (sel8_grade, ssn(i), sel8,  sel8_year, sel8_semester)
                cursor.execute(update_grade, sel8_grade_args)
                cnx.commit()
                print('Student {} grade has been updated to {} '.format(ssn, sel8_grade))
                i += 1;
        except mysql.connector.Error as err:
            print('Error code: ', err)

    print('Would you like to edit another student''s grades? Y for YES and N for NO!')
    choice = input(' >> ')
    choice = choice.lower()
    if choice == 'y':
        menu_actions['8']()
    else:
        menu_actions['main_menu']()

#Menu9 :: Check grades by giving (code, student SSN or name ,year semster
def menu9():

    print("Check a Students grades: ")
    functionsDB.showCourse()
    reg9 = input('Please input a course code to check the students grades: (TYPE NOTHING TO RETURN TO MAIN MENU )')

    if reg9 == '':
        print('Error: No course selected, returning you to main menu')
        menu_actions['main_menu']()

    else:
        sel9_SSNname = input('Check a students grades by name or ssn: (TYPE EITHER HERE)')
        sel9_year = input('Please enter year: ')
        sel9_semester = input('Please enter semester: ')

        if sel9_SSNname.isdigit():
            query9_args = (reg9, sel9_SSNname, sel9_year, sel9_semester)
            print('Here is the grades you requested: ')
            check_query = ('SELECT s.name, r.ssn, r.code, r.grade '
                           'FROM Registered r, Student s WHERE r.code = %s AND s.ssn = r.ssn AND r.ssn = %s AND r.year = %s AND r.semester = %s')
            try:
                cursor.execute(check_query, query9_args)
                cnx.commit()
            except mysql.connector.Error as err:
                print('Error code: ', err)

        else:
            query9_args = (reg9, sel9_SSNname, sel9_year, sel9_semester)
            check_query = ('SELECT s.name, r.ssn, r.code, r.grade '
                           'FROM Student s, Registered r '
                           'WHERE s.ssn = r.ssn AND r.code = %s AND s.Name = %s AND r.year = %s AND r.semester = %s')
            try:
                cursor.execute(check_query, query9_args)
                print('Here is the grades you requested: ')
                for (name, ssn, code, grade) in cursor:
                    print('{} | {} | {} | {}'.format(name,ssn, code, grade))
            except mysql.connector.Error as err:
                print('Error code: ', err)

        print('Would you like to check another student''s grades? Y for YES and N for NO!')
        choice = input(' >> ')
        choice = choice.lower()
        if choice == 'y':
            menu_actions['9']()
        else:
            menu_actions['main_menu']()

# Exit program
def exit():
    print("\tClosing connection.")
    cnx.close()
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '4': menu4,
    '5': menu5,
    '6': menu6,
    '7': menu7,
    '8': menu8,
    '9': menu9,
    '10': exit
}

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
