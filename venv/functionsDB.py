import mysql.connector

cnx = mysql.connector.connect(user='dbproject',
                              password='1234pass',
                              host='127.0.0.1',
                              database='dbproject')

cursor = cnx.cursor()

def showCourse():
    title_bar = 'Course Code: |\tCourse Title:'
    print(title_bar)
    print('-' * len(title_bar))
    check_course = ("SELECT code, title FROM Course")

    cursor.execute(check_course)

    for (code,title) in cursor:
        current_courses = ('{}\t\t |\t{}'.format(code,title))
        print(current_courses)

def showStuds():
    show_studs = ('SELECT * FROM Student')
    print('Current student database: ')
    cursor.execute(show_studs)

    for (ssn, name, address, major) in cursor:
        curr_studs = ('{}\t | {}'.format(ssn, name))
        print(curr_studs)