import psycopg2
import pwinput
import numpy as np
import matplotlib.pyplot as plt
import pyfiglet
import decimal

#--------------------------------------CONNECTION----------------------------------------------#

text = "G R A D E S"
ascii_art = pyfiglet.figlet_format(text)
lines = "-" * len(ascii_art.splitlines()[0])

print(lines)
print(ascii_art)
print(lines)

connected = False
print("Welcome to Grades Database!")
connected = False

while not connected:

    username = input('Type your database username: ')
    password = pwinput.pwinput(prompt='Type your database password: ', mask='*')

    try:
        con = psycopg2.connect(
            database=username,
            user=username,
            password=password, 
            host="dbm.fe.up.pt",
            port="5433",
            options='-c search_path=grades')
        connected = True

    except psycopg2.OperationalError:
        print("You're not connected to FEUP VPN or inputed wrong credentials.\n")
    else:
        print("You successfully connected to the database.\n")
    finally:
        continue

cursor = con.cursor()

#--------------------------------------PLOTS---------------------------------------------------#

while True:
    try:
        print('Please choose the graphic that you want to see:')
        print('[1] Histogram for the distribution of grades')
        print('[2] Barplot of average grade per course')
        print('[3] Scatter plot between each student GPA and their average grade')
        print('[4] Exit')
        choice = input()
        choice = int(choice)

        if choice in [1, 2, 3, 4]:
            pass
        else:
            print('Please choose a number between 1 and 4.')
    except ValueError:
        print('Please input a valid number between 1 and 4.')


    if choice == 1:
            # Histogram for the distribution of grades
            query_grades = '''
            SELECT grade
            FROM attendance
            '''
            cursor.execute(query_grades)
            records = cursor.fetchall()

            x = []    
            for i in range(len(records)):
                x.append(records[i][0])

            average_grade = np.mean(x) # for the second plot

            fig = plt.figure(figsize = (10, 5))
            plt.xlabel("Grades")
            plt.title("Grades distribution")
            plt.hist(x, color='grey', alpha= 0.5, bins=20)
            plt.show()

    elif choice == 2:
            # Barpolt of average grade per course
            query_courses = '''
                    SELECT course_name
                    FROM course
                    ORDER BY course_name
                    '''

            cursor = con.cursor()
            cursor.execute(query_courses)
            records_courses = cursor.fetchall()


            courses_list = []
            for i in range(len(records_courses)):
                courses_list.append(records_courses[i][0])


            query_means = '''
                    SELECT course_id, course_name, AVG(grade)
                    FROM attendance
                    JOIN exam USING (exam_id)
                    JOIN course USING (course_id)
                    GROUP BY course_id, course_name
                    ORDER BY course_name
                    '''

            cursor.execute(query_means)
            records_means = cursor.fetchall()

            means_list = []
            for i in range(len(records_means)):
                means_list.append(records_means[i][2])


            fig, ax = plt.subplots(figsize = (10, 5))
            plt.bar(courses_list, means_list, color ='maroon', width = 0.4)
            plt.axhline(y = average_grade, linestyle='--', linewidth=2)
            plt.xlabel("Courses")
            plt.ylabel("Average grade")
            plt.title("Average grades per course")
            plt.xticks(rotation=60)
            ax.legend(['Mean'])
            plt.show()



    elif choice == 3:
            # Scatter plot between each student's GPA and their average grade
            query_gpa = '''
                SELECT student_id, gpa
                FROM student
                ORDER BY student_id
                '''

            cursor = con.cursor()
            cursor.execute(query_gpa)
            records_gpa = cursor.fetchall()

            gpa_list = []
            for i in range(len(records_gpa)):
                gpa_list.append(float(records_gpa[i][1]))

            query_student_grades = '''
                            SELECT student_id, AVG(grade)
                            FROM attendance
                            JOIN student USING (student_id)
                            GROUP BY student_id
                            ORDER BY student_id
                            '''

            cursor.execute(query_student_grades)
            records_student_grades = cursor.fetchall()

            student_grades_list = []
            for i in range(len(records_student_grades)):
                student_grades_list.append(float(records_student_grades[i][1]))
            
            fig, ax = plt.subplots(figsize = (10, 5))
            plt.scatter(gpa_list, student_grades_list, color ='green')
            plt.xlabel("Student's GPA")
            plt.ylabel("Average grade")
            plt.title("Relations between each student's GPA and their average grade")
            b, a = np.polyfit(gpa_list, student_grades_list, deg=1)
            xseq = np.linspace(2.8, 4)
            ax.plot(xseq, a + b * xseq, color="k", lw=1.5)
            plt.show()
    
    elif choice == 4: 
        break
    else:
        pass


cursor.close()

