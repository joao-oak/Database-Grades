# Database-Grades
### FEUP, Faculty of Engineering, University of Porto Master in Data Science and Enginnering 
### Silvia Tavares, João Carvalho, Abílio Neves, Md. Wakil Ahmad
### Databases, October 2023
---
This project regards the design of a database for the grades, using the tools of SQL and Python. In order to have a better understanding, we created a small storytelling:

University JS is a university that offers to its students an intensive 1-year Associate Degree that will prepare the students to afterwards enrol in a Bachelor Degree of their choice. With the intent of improving its services, the uni wants to use a database to store academic information of all students. For more information about the US educational system, please visit Education in the United States - Wikipedia.

The requirements for the database are:

A student can enroll in many courses, and there is not a limit for the number of courses that a student can be enrolled in. Each enrollment is an association between student and course.
The university needs to store the following data for each student: first_name, last_name, email, date_of_birth, state, gpa from high school, and if the student needs accessibility (for example, a room needs to have a ramp or an elevator so that a student in a wheelchair can get access to it). Each student has a unique student number.
Email is composed by <first_name>.<last_name>@jsuniversity.edu.

A room has a name, a maximum capacity, and can have or not projector and/or computers. Also, some of the rooms are accessible to students with disabilities. A room belongs to a building which also has a name. The names of the buildings are also unique. There is an identifier code for every room and building.

For each course there are several but well-defined evaluation types (exam_names).  Each Evaluations will occur in a specific date and time(start time and end time), but the same evaluation can take place, and at the same time, in more than one room for different students. An evaluation type might require or not a projector and/or computers. Attendance of each student for each evaluation type of a course ,in which the student is enrolled, will be recorded and the grade achieved as well.

---
The project is composed by the following steps:

**1. Creation of the UML (uml.png) and Relational Model (relational.txt):**
Based on the fields provided, a UML model of the database was created and the related relation model. 


**2. Creation of SQL script (grades.sql):**
This script will create the tables in the database. For this section we also created 2 triggers:

- trigger_validate_exam_room_capacity: this trigger raises an error if we try to insert into the table attendance a number of student_id(s) for an exam_id taking place on a room_id that overflows the capacity of the room;

- trigger_validate_exam_room_constraints: this trigger raises an error if we try to insert into the table attendance a student with a disability in a room that is not accessiible. On the other hand, it also raises an error if the exam needs to be in a room with projector or computer and the room don't have this devices.

Besides the main sql code(grades.sql), we also created a separate folder called helper where we have a python code (Load_aux.py) with the databases configuration from the .ini file were we load the whole dataset, an sql code with DQL, DML, inserts and testing (including trigger testing).


**3. Load the Data into the Data Base (load_grades.py):**
To load the data form python using the cursor to operate the **DELETE** command to delete all records and **INSERT** command to popullate de database.

**4. User Interface (grades.py):**
An interface that allows to manage and interact with the grades database and obtain the following information:

Student:
- Personal Data;
- Grades for every / specific course
  
Exam:
- Search for the exam to see which room/rooms and building it will hold and the respective date;
- Retrieve the average grade for a given group (Student, State, Course or Exam Type);
 
Room:
- Search for rooms based on given characteristics (has computer, has projector, is accessible);

**5. Extra (extra.py):**
In order to extract some meaningful information from the database the following plots were created:

- Histogram with the grades distribution;
- Bar chart with the average grade by course;
- Scatter plot with relation between gpa and average grades for each student with a linear regression.

---
**Future work:**

For the future work we believe that some of the following improvements can be made:
- Calculated field email;
- Creation of indexes;
- Cardinality issue follow-up if needed;
- Assure that a we can not insert in the databases, exam that are not related to a specific course. For that a list of the related exam for each course should be provided.
