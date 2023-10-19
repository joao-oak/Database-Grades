# Database-Grades
### FEUP, Faculty of Engineering, University of Porto Master in Data Science and Enginnering 
### Silvia Tavares, João Carvalho, Abílio Neves, Md. Wakil Ahmad
### Databases, October 2023
---
This project regards the design of a database for the grades, using the tools of SQL and Python. In order to have a better understanding, we created a small storytelling:

University JS is a university that offers to its students an intensive 1-year Associate Degree that will prepare the students to afterwards enrol in a Bachelor Degree of their choice. With the intent of improving its services, the uni wants to use a database to store academic information of all students. For more information about the US educational system, please visit Education in the United States - Wikipedia.

The requirements for the database are:

A student must be enrolled in at least one course, and there is not a limit for the number of courses that a student can be enrolled in. Each individual enrollment is an event with an associated ID.
The university needs to store the following data for each student: first_name, last_name, email, date_of_birth, state, gpa , and if the student needs accessibility (for example, a room needs to have a ramp or an elevator so that a student in a wheelchair can get access to it). Each student has a unique student number.
Email is composed by <first_name>.<last_name>@jsuniversity.edu.

A room has a name, a maximum capacity, and can have or not projector and/or computers. Also, some of the rooms are accessible to students with disabilities. A room belongs to a building which also has a name. In the whole university there are no rooms with the same name. And the names of the buildings are also unique. There is an identifier code for every room and building.

For each course there are several but well-defined evaluation types (exam_names).  Evaluations will occur each one of them on a specific date and time(start time and end time), but the same evaluation can take place, and at the same time, in more than one room for different students. An evaluation type might require or not a projector and/or computers. Attendance of each student for each evaluation type of a course ,in which the student is enrolled, will be recorded and the grade achieved as well.

---
The project is composed by the following steps:

:dart:  **1. Creation of the UML (uml.png) and Relational Model (relational.txt):**
Based on the fields provided, a UML model of the database was created and the related relation model. 


:gear:  **2. Creation of SQL script (grades.sql):**
This script will create the tables in the database.


:hourglass_flowing_sand:  **3. Load the Data into the Data Base (load_grades.py):**
To load the data form python using the cursor to operate the **DELETE** command to delete all records and **INSERT** command to popullate de database.

:joystick:  **4. User Interface (grades.py):**
An interface that allows to manage and interact with the grades database and obtain the following information:

Student:
- Personal Data;
- Grades for every / specific course
  
Exam:
- Search for the exam to see which room/rooms and building it will hold and the respective date;
- Retrieve the average grade for a given group (Student, State, Course or Exam Type);
 
Room:
- Search for rooms based on given characteristics (has computer, has projector, is accessible);

:chart_with_upwards_trend:  **5. Extra (extra.py):**
In order to extract some meaningful information from the database the following plots were created:

- Histogram with the grades distribution;
- Bar chart with the average grade by course;
- Scatter plot with gpa for each student;
- Scatter plot with average grade by student (regression)
---
:handshake:  **Contribution of each student in the project:**
The contribution of each student in the project in presented in a range from 0 to 100% representing the effort that each one made:
- Abílio Neves - up200000406 : 100%
- João Carvalho - up201507023 : 100%
- Md. Wakil Ahmad - up202109215 :
- Silvia Tavares - up202204392: 100%

