import psycopg2
import csv
from psycopg2 import extras
import pwinput
import pyfiglet
import os
import msvcrt


#--------------------------------------CONNECTION----------------------------------------------#

# Function to clear the interaction screen

def clear_screen():
    os.system('cls')

clear_screen()
text = "G R A D E S"
ascii_art = pyfiglet.figlet_format(text)
lines = "-" * len(ascii_art.splitlines()[0])

print(lines)
print(ascii_art)
print(lines)

connected = False
print("Welcome to Grades Database!")

while not connected:

    username = input('Type your database username: ')
    password = pwinput.pwinput(prompt='Type your database password: ', mask='*')

    try:
        con = psycopg2.connect(
            database=username,  # your database is the same as your username
            user=username,  # your username
            password=password,  # your password
            host="dbm.fe.up.pt",  # the database host
            port="5433",
            options='-c search_path=grades')  # use the schema you want to connect to
        connected = True

    except psycopg2.OperationalError:
        print("You're not connected to FEUP VPN or inputed wrong credentials.\n")
    else:
        print("You successfully connected to the database.\n")
    finally:
        continue


#----------------------------------------STUDENT-----------------------------------------------#

# Retrieve student data

def student_data():
    
    
    while True:
        
        try:
            student_name = input('Please insert the first and last name of the student you want to search (example:Carlos Tavares):')
            names = student_name.split()
            
            first_name = names[0].capitalize()
            last_name = names[1].capitalize()
            
            query = '''
            SELECT
                first_name,
                last_name,
                email,
                date_of_birth,
                state,
                gpa
            FROM student
            WHERE first_name LIKE %s AND last_name LIKE %s
            '''
        
            cursor = con.cursor()
            cursor.execute(query, (first_name, last_name))
            records = cursor.fetchall()
            records = records[0]
        
        except:
            print('\n')
            print("We don't have any record in the database for that name.")
            print("Please remember to input the first and last names of the student")
            
            while True:
                
                answer = input('Do you want to try again?')
                
                if answer[0].lower() == 'n':
                    break
                    
                elif answer[0].lower() != 'y':
                    print('Please answer yes or no.')
                
                else:
                    break
                    
            if answer[0].lower() == 'n':
                break
    
    
        else:
            print('\n')
            print(f'Name: {records[0]} {records[1]}\n')
            print(f'Email: {records[2]}\n')
            print(f'Birthdate: {records[3]}\n')
            print(f'State: {records[4]}\n')
            print(f'GPA: {records[5]}\n')
            
            break


# Retrieve grades for a student for every / a specific course

def performance():
    
    while True:
        
        student_name = input('Please insert the first and last name of the student you want to search (example:Carlos Tavares):')
        
        while True:
            try:
                names = student_name.split()
                first_name = names[0].capitalize()
                last_name = names[1].capitalize()

            except:
                print("Please insert the student's first and last names.")
                student_name = input(f'Please insert the first and last name of the student you want to search (example:Carlos Tavares):')

            else:
                break

        while True:
            cursor = con.cursor()
            check_course = input(f"Do you want to check {first_name}'s grades for a specific course? (Y/N)")

            if check_course[0].lower() == 'y':
                query =("""
                SELECT DISTINCT course.course_name
                FROM enrollment
                JOIN student ON enrollment.student_id = student.student_id
                JOIN course ON enrollment.course_id = course.course_id
                WHERE student.first_name = %s AND student.last_name = %s;""")
                
                cursor.execute(query, (first_name, last_name))
                # Fetch all the results and store them in a list
                result_list = [row[0] for row in cursor.fetchall()]

                # Print the list of results
                print('\n')
                for course_name in result_list:
                    print(course_name)
                course = input('\nWhat is the name of the course you want to check?')
                course = course.capitalize()
                break

            elif check_course[0].lower() == 'n':
                course = '%'
                break

            else:
                print("Please answer 'yes' or 'no'")

        query = '''
            SELECT
                first_name,
                last_name,
                course_name,
                exam_name,
                grade
            FROM student
            JOIN attendance USING (student_id)
            JOIN exam USING (exam_id)
            JOIN course USING (course_id)
            JOIN exam_type USING (type_id)
            WHERE first_name LIKE %s
                AND last_name LIKE %s
                AND course_name LIKE %s
            ORDER BY course_name
            '''    

        cursor.execute(query, (first_name, last_name, course))
        records = cursor.fetchall()

            
        if not records:
            print("\n")
            print("We don't have any record for that student and/or course.")
                
            while True:
                
                answer = input('Do you want to try again?')
                
                if answer[0].lower() == 'n':
                    break
                    
                elif answer[0].lower() != 'y':
                    print('Please answer yes or no.')
                
                else:
                    break
                    
            if answer[0].lower() == 'n':
                break
            
            
        else:
            print('\n')
            print(f'Student: {first_name} {last_name}\n')

            for i in range(len(records)):
                print(f'Course: {records[i][2]} || Assessment type: {records[i][3]} || Grade: {records[i][4]}\n')


            break



#-----------------------------------------EXAMS------------------------------------------------#

# Search for exam to see which room/rooms will hold the exam and the respective date

def check_exam():
    cursor = con.cursor()
    while True:
        
        while True:
            cursor.execute ("""
                SELECT DISTINCT course.course_name
                FROM course;""")
            
            # Fetch all the results and store them in a list
            result_list = [row[0] for row in cursor.fetchall()]

            # Print the list of results
            print('\n')
            for course_name in result_list:
                print(course_name)
            
            course = input('\nPlease insert the name of the course:')
            course = course.split()
            for i in range(len(course)):
                course[i] = course[i].capitalize()
            course = ' '.join(course)

            query = f'''
                    SELECT DISTINCT exam_name
                    FROM exam
                    JOIN course USING (course_id)
                    JOIN exam_type USING (type_id)
                    WHERE course_name LIKE %s
                    '''

            cursor.execute(query, (course,))
            records = cursor.fetchall()

            if not records:
                print("\n")
                print(f"We don't have any exam for that course.")

                while True:

                    answer = input('Do you want to try again?')

                    if answer[0].lower() == 'n':
                        break

                    elif answer[0].lower() != 'y':
                        print('Please answer yes or no.')

                    else:
                        break

                if answer[0].lower() == 'n':
                    break

            else:
                print(f'\nThese are the availabe exams for {course}:')
                for i in range(len(records)):
                    print(records[i][0])
                break
        
        
        if 'answer' in globals():
            
            if answer[0].lower() == 'n':
                break
        
        
        exam_t = input('\nPlease insert the type of the exam you want to search:')
        exam_t = exam_t.split()
        for i in range(len(exam_t)):
            exam_t[i] = exam_t[i].capitalize()
        exam_t = ' '.join(exam_t)
        
        query = f'''
                SELECT DISTINCT course_name, exam_name, exam_date, room_name, building_name
                FROM exam
                JOIN exam_type USING (type_id)
                JOIN course USING (course_id)
                JOIN attendance USING (exam_id)
                JOIN room USING (room_id)
                JOIN building USING (building_id)
                WHERE course_name LIKE %s AND exam_name LIKE %s
                '''
        cursor = con.cursor()
        cursor.execute(query, (course, exam_t))
        records = cursor.fetchall()
        
        if not records:
            print(f"\nWe don't have any record for that type of exam and course you chose.")
            
            while True:
                
                answer = input('Do you want to try again?')
                
                if answer[0].lower() == 'n':
                    break
                    
                elif answer[0].lower() != 'y':
                    print('Please answer yes or no.')
                
                else:
                    break
                    
            if answer[0].lower() == 'n':
                break
        
        else:
            print(f'\nCourse: {course}')
            print(f'Exam type: {exam_t}\n\n')
            for i in range(len(records)):
                print(f'Exam date: {records[i][2]} || Room: {records[i][3]} || Building: {records[i][4]}\n')
            break


# Retrieve the average grade for a given group

def check_averages():
    cursor = con.cursor()
    while True:
          
        while True:

            try:
                print('Please insert the number corresponding to the variable you want to choose')
                print('[1] Student')
                print('[2] State')
                print('[3] Course')
                print('[4] Type of exam')
                choice = input()
                choice = int(choice)

            except:
                print('Please input a number between 1 and 4.')
                
            else:
                if choice not in [1,2,3,4]:
                    print('Please choose a number between 1 and 4.')

                else:
                    break

        category = ['Student', 'State', 'Course', 'Type of exam']
        chosen = category[choice - 1]

        if chosen == 'State':
                cursor.execute ("""
                SELECT DISTINCT state FROM student;""")
                
                # Fetch all the results and store them in a list
                result_list = [row[0] for row in cursor.fetchall()]
                print(f'\nThe available {chosen}s are:')
                for name in result_list:
                    print(name)

        elif chosen == 'Course':
                cursor.execute ("""
                SELECT DISTINCT course.course_name FROM course;""")
                
                # Fetch all the results and store them in a list
                result_list = [row[0] for row in cursor.fetchall()]
                print(f'\nThe available {chosen}s are:')
                for name in result_list:
                    print(name)
        
        elif chosen == 'Type of exam':
                cursor.execute ("""
                SELECT DISTINCT exam_name FROM exam_type;""")
                
                # Fetch all the results and store them in a list
                result_list = [row[0] for row in cursor.fetchall()]
                print(f'\nThe available {chosen}s are:')
                for name in result_list:
                    print(name)
        else: 
            pass

        name = input(f'Please insert the {chosen} you want to know the average grade for:')


        if choice == 1:
            
            while True:
                
                try:
                    name = name.split()
                    first_name = name[0].capitalize()
                    last_name = name[1].capitalize()
                
                except:
                    print("Please insert the student's first and last names.")
                    name = input(f'Please insert the {chosen} you want to know the average grade for:')
                
                else:
                    break

            query = f'''
            SELECT first_name, last_name, AVG(grade)
            FROM student
            JOIN attendance USING (student_id)
            GROUP BY first_name, last_name
            HAVING first_name LIKE %s AND last_name LIKE %s
            ''' 

            cursor.execute(query, (first_name, last_name))
            records = cursor.fetchall()
            
            name = f'{first_name} {last_name}'
        
        else:

            query_category = ['state', 'course_name', 'exam_name']
            chosen_query = query_category[choice - 2]

            name = name.split()
            for i in range(len(name)):
                name[i] = name[i].capitalize()
            name = ' '.join(name)

            query = f'''
                SELECT {chosen_query}, AVG(grade)
                FROM student
                JOIN attendance USING (student_id)
                JOIN exam USING (exam_id)
                JOIN exam_type USING (type_id)
                JOIN course USING (course_id)
                GROUP BY {chosen_query}
                HAVING {chosen_query} LIKE %s
                '''    

            cursor = con.cursor()
            cursor.execute(query, (name,))
            records = cursor.fetchall()
    
    
        if not records:
            print("\n")
            print(f"We don't have any record for the {chosen} you chose.")
            
            while True:
                
                answer = input('Do you want to try again?')
                
                if answer[0].lower() == 'n':
                    break
                    
                elif answer[0].lower() != 'y':
                    print('Please answer yes or no.')
                
                else:
                    break
                    
            if answer[0].lower() == 'n':
                break
            
        else:
            print('\n')
            print(f"Average grade for {name}: {records[0][-1]}")
            break



#-----------------------------------------ROOMS------------------------------------------------#

def room_needs():
    cursor = con.cursor()
    while True:
            
        while True:
            computers = input('Do you want a room with computers?')

            if computers[0].lower() == 'y':
                computers = True
                break
            elif computers[0].lower() == 'n':
                computers = False
                break
            else:
                print("Please answer 'y' or 'n'")

        while True:
            projector = input('Do you want to have a projector?')

            if projector[0].lower() == 'y':
                projector = True
                break
            elif projector[0].lower() == 'n':
                projector = False       # if False, it doesn't do harm to include the rooms with projectors anyway if the purpose is to book rooms
                break
            else:
                print("Please answer 'y' or 'n'")

        while True:
            accessible = input('Does the room have to have accessibility?')

            if accessible[0].lower() == 'y':
                accessible = True
                break
            elif accessible[0].lower() == 'n':      
                accessible = False
                break
            else:
                print("Please answer 'y' or 'n'")

        query = '''
        SELECT
            room_name,
            building_name
        FROM room
        JOIN building
        USING (building_id)
        WHERE has_computers is %s
          AND has_projector is %s
          AND is_accessible is %s
        '''

        cursor.execute(query, (computers, projector, accessible))
        records = cursor.fetchall()

        if not records:
            print('\n')
            print("We don't have any room with the characteristics you chose.")
            
            while True:
                
                answer = input('Do you want to try again?')
                
                if answer[0].lower() == 'n':
                    break
                    
                elif answer[0].lower() != 'y':
                    print('Please answer yes or no.')
                
                else:
                    break
                    
            if answer[0].lower() == 'n':
                break

        else:       
            print('\n')
            for i in range(len(records)):
                print(f'{records[i][0]} - {records[i][1]}')

            break



#-----------------------------------------MENU-------------------------------------------------#

# Interation environment and function integration

def menu():

    print('Please press any key to start.')
    msvcrt.getch()

    clear_screen()

    while True:
        
        print("Menu :")
        print("[1] Student information")
        print("[2] Exams information")
        print("[3] Rooms information")
        print("[0] Exit")
        
        while True:

            try:
                choice = input()
                choice = int(choice)

            except:
                print('Please input a number between 0 and 3.')
                
            else:
                if choice not in [0,1,2,3]:
                    print('Please choose a number between 0 and 3.')

                else:
                    break
        
        
        if choice == 1:
            clear_screen()
            print("Student information:")
            print("[1] Student personal data")
            print("[2] Student performance")
            print("[0] Exit")
        
            while True:

                try:
                    choice = input()
                    choice = int(choice)

                except:
                    print('Please input a number between 0 and 2.')

                else:
                    if choice not in [0,1,2]:
                        print('Please choose a number between 0 and 2.')

                    else:
                        break
            
            if choice == 1:
                clear_screen()
                student_data()
            
            elif choice == 2:
                clear_screen()
                performance()
                
            elif choice == 0:
                break         
        
        elif choice == 2:
            clear_screen()
            print("Exams information:")
            print("[1] Exams data")
            print("[2] Average grades")
            print("[0] Exit")
            
            while True:

                try:
                    choice = input()
                    choice = int(choice)

                except:
                    print('Please input a number between 0 and 2.')

                else:
                    if choice not in [0,1,2]:
                        print('Please choose a number between 0 and 2.')

                    else:
                        break
            
            if choice == 1:
                clear_screen()
                check_exam()
                
            elif choice == 2:
                clear_screen()
                check_averages()
                
            elif choice == 0:
                break
            
        elif choice == 3:                      # this can be cut if there's only one function for rooms
            clear_screen()
            print("Rooms information:")
            print("[1] Room characteristics")
            print("[0] Exit")
        
            while True:

                try:
                    choice = input()
                    choice = int(choice)

                except:
                    print('Please input a number between 0 and 2.')

                else:
                    if choice not in [0,1,2]:
                        print('Please choose a number between 0 and 2.')

                    else:
                        break
                        
            if choice == 1:
                clear_screen()
                room_needs()
                
            elif choice == 0:
                break
            
        elif choice == 0:
            break


menu()

con.close()