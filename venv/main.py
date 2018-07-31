#!/usr/bin/env python
#Author: Russ Seaman
#Assignment: Online Registration System Database Assignment
#Date: 06/05/2018

import sys, os
import mysql.connector

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
#
# print('Are you using Windows or Linux/OSX(MAC)?')
# clear_Var = 0
# clear_Val = input('Press 1 for Windows and Press 2 for Linux/OSX(MAC)')
# if clear_Val == 1:
#     clear_var = 'cls'
# else:
#     clear_Var == 'clear'
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

menu_actions = {}

#===================
#   MENU FUNCTIONS
#===================

def main_menu():
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

    title_bar = 'Course Code: |\tCourse Title:'
    print(title_bar)
    print('-' * len(title_bar))
    check_course = ("SELECT code, title FROM Course")

    cursor.execute(check_course)


    for (code,title) in cursor:
        current_courses = ('{}\t\t |\t{}'.format(code,title))
        print(current_courses)

    print('\nPlease input the course code you would like to delete: ')
    course_code = input(" >> ")
    select_course = ("SELECT code, title FROM Course WHERE code = %s")
    cursor.execute(select_course, (course_code, ))

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
            cnx.commit()
            cursor.execute(delete_course, (course_code, ))
            print('\nCourse: ', code, 'has been deleted')
        except mysql.connector.Error as err:
            print('Error code: ', err)
    else:
        menu_actions['2']()

    print('\nWould you like to return to the main menu or delete another course?\n')
    mini_sel = input("Press 1 to return to main menu or 2 to delete another course: \n")
    if mini_sel == '2':
        menu_actions['2']()
    else:
        menu_actions['main_menu']()
        choice = input(" >> ")
        exec_menu(choice)
    return


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
    '9': back,
    '10': exit,
}

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()

