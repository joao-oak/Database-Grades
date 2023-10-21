import pwinput
import psycopg2
import pyfiglet
import csv
#import configparser
#import sqlalchemy as sa

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

# ------------------------------------------ DELETE DATABASE RECORDS --------------------------------------------------#

def delete_records():
    cur0 = con.cursor()
    cur0.execute("""
                      DELETE FROM attendance;
                      DELETE FROM enrollment;
                      DELETE FROM exam;
                      DELETE FROM exam_type;
                      DELETE FROM room;
                      DELETE FROM building;
                      DELETE FROM student;
                      DELETE FROM course
        """)
    con.commit()
    print("All data have been deleted!!\n")

delete_records()

# ------------------------------------------ LOADING DATA -------------------------------------------------------------#

def insert_records():
    cur = con.cursor()

    # Open and read the CSV file
    with open(r"grades.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Check if the record already exists in the student table
            cur.execute("""
                SELECT student_id FROM student
                WHERE first_name = %(first_name)s
                AND last_name = %(last_name)s
                AND date_of_birth = %(date_of_birth)s;
            """, row)

            existing_record = cur.fetchone()

            if existing_record:
                student_id = existing_record[0]
            else:
                # Insert a new record
                cur.execute("""
                    INSERT INTO student (first_name, last_name, date_of_birth, state, email, gpa)
                    VALUES (%(first_name)s, %(last_name)s, %(date_of_birth)s, %(state)s, %(email)s, %(gpa)s)
                    RETURNING student_id;
                """, row)

                student_id = cur.fetchone()[0]
            
            # Check if the record already exists in the exam_type table
            cur.execute("""
                SELECT type_id FROM exam_type
                WHERE exam_name = %(exam_name)s;
            """, row)

            existing_record = cur.fetchone()

            if existing_record:
                type_id = existing_record[0]
            else:
                # Insert a new record into the exam_type table
                cur.execute("""
                    INSERT INTO exam_type (exam_name)
                    VALUES (%(exam_name)s)
                    RETURNING type_id;
                """, row)

                type_id = cur.fetchone()[0]
            
            # Check if the record already exists in the course table
            cur.execute("""
                SELECT course_id FROM course
                WHERE course_name = %(course_name)s;
            """, row)

            existing_course = cur.fetchone()

            if existing_course:
                course_id = existing_course[0]
            else:
                # Insert a new record into the course table
                cur.execute("""
                    INSERT INTO course (course_name)
                    VALUES (%(course_name)s)
                    RETURNING course_id;
                """, row)

                course_id = cur.fetchone()[0]
            
            # Check if the record already exists in the exam table
            cur.execute("""
                SELECT exam_id FROM exam
                WHERE exam_date = %(exam_date)s
                AND course_id = (SELECT course_id FROM course WHERE course_name = %(course_name)s)
                AND type_id = (SELECT type_id FROM exam_type WHERE exam_name = %(exam_name)s);
            """, row)

            existing_exam = cur.fetchone()

            if existing_exam:
                exam_id = existing_exam[0]
            else:
                # Insert a new record into the exam table
                cur.execute("""
                    INSERT INTO exam (exam_date, course_id, type_id)
                    SELECT %(exam_date)s, course_id, type_id
                    FROM course, exam_type
                    WHERE course_name = %(course_name)s
                    AND exam_name = %(exam_name)s
                    RETURNING exam_id;
                """, row)

                exam_id = cur.fetchone()[0]


            # Check if the record already exists in the building table
            cur.execute("""
                SELECT building_id FROM building
                WHERE building_name = %(building_name)s;
            """, row)

            existing_record = cur.fetchone()

            if existing_record:
                building_id = existing_record[0]
            else:
                # Insert a new record into the building table
                cur.execute("""
                    INSERT INTO building (building_name)
                    VALUES (%(building_name)s)
                    RETURNING building_id;
                """, row)

                building_id = cur.fetchone()[0]

            # Check if the record already exists in the room table
            cur.execute("""
                SELECT room_id FROM room
                WHERE room_name = %(room_name)s
                AND building_id = (SELECT building_id FROM building WHERE building_name = %(building_name)s);
            """, row)

            existing_record = cur.fetchone()

            if existing_record:
                room_id = existing_record[0]
            else:
                # Insert a new record into the room table
                cur.execute("""
                    INSERT INTO room (room_name, capacity, has_projector, has_computers, is_accessible, building_id)
                    SELECT %(room_name)s, %(capacity)s, %(has_projector)s,%(has_computers)s, %(is_accessible)s, building_id
                    FROM building
                    WHERE building_name = %(building_name)s
                    RETURNING room_id;
                """, row)

                room_id = cur.fetchone()[0]

            # Check if the enrollment record already exists in enrollment
            cur.execute("""
                SELECT student_id, course_id FROM enrollment
                WHERE student_id = (SELECT student_id FROM student WHERE email = %(email)s)
                AND course_id = (SELECT course_id FROM course WHERE course_name = %(course_name)s);
            """, row)

            existing_enrollment = cur.fetchone()

            if not existing_enrollment:
                # Insert a new enrollment record
                cur.execute("""
                    INSERT INTO enrollment (student_id, course_id)
                    SELECT student_id, course_id 
                    FROM student, course
                    WHERE email = %(email)s
                    AND course_name = %(course_name)s;
                """,row)

            # Check if the attendance record already exists
            cur.execute("""
                SELECT student_id, exam_id FROM attendance
                WHERE student_id = (SELECT student_id FROM student WHERE email = %(email)s)
                AND exam_id = (
                        SELECT exam_id FROM exam
                        WHERE exam_date = %(exam_date)s
                        AND course_id = (SELECT course_id FROM course WHERE course_name = %(course_name)s)
                        AND type_id = (SELECT type_id FROM exam_type WHERE exam_name = %(exam_name)s));
            """, row)

            existing_attendance = cur.fetchone()

            if not existing_attendance:
                # Insert a new attendance record
                cur.execute("""
                    INSERT INTO attendance (student_id, exam_id, room_id, grade)
                    SELECT student_id, exam_id, room_id, %(grade)s
                    FROM student, exam, room
                    WHERE email = %(email)s
                    AND exam_date = %(exam_date)s
                        AND course_id = (SELECT course_id FROM course WHERE course_name = %(course_name)s)
                        AND type_id = (SELECT type_id FROM exam_type WHERE exam_name = %(exam_name)s)
                    AND room_name = %(room_name)s
                    AND building_id = (SELECT building_id FROM building WHERE building_name = %(building_name)s);
                """, row) 

    con.commit()
    con.close()
    print("All data have been inserted!")


insert_records()

