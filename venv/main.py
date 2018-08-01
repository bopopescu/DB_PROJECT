#!/usr/bin/env python
#Author: Russ Seaman
#Assignment: Online Registration System Database Assignment
#Date: 06/05/2018

import sys, os
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

menu_actions = {}

#===================
#   MENU FUNCTIONS
#===================

def main_menu():
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
    clear()
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
    clear()
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
            print(title_bar)
            print('-' * len(title_bar))
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

    # confirm_sel = input('Press Y for YES and N for NO')
    # confirm_sel = confirm_sel.lower()


    try:
        delete_stud = ("DELETE FROM Student WHERE ssn = %s")
        cursor.execute(delete_stud, (del_ssn,))
        cnx.commit()
        print('\nStudent: ', del_ssn, 'has been deleted')
    except mysql.connector.Error as err:
        print('Error code: ', err)


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    print("\tThank you for using the app! Closing connection.")
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
    '9': back,
    '10': exit,
}

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()

