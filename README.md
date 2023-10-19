# Database-Grades
### FEUP, Faculty of Engineering, University of Porto Master in Data Science and Enginnering 
### Silvia Tavares, João Carvalho, Abílio Neves, Md. Wakil Ahmad
### Databases, October 2023
---
This project regards the design of a database for the grades, using the tools of SQL and Python. In order to have a better understanding, we created a storytelling to specify the requirements.

University JS is a university that offer to its students an intensive 1-year Associate Degree that will prepare the students to afterwards enrol in a Bachelor Degree of their choice. With the intent of improving its services, the uni wants to use a database to store academic information of all students. For more information about the US educational system, please visit Education in the United States - Wikipedia.
As a pilot program to be started in the new academic year, 30 students of the 1-year Associate Degree were chosen. Those students are enrolled across 15 different courses and for semester 1.

A student must be enrolled in at least one course, and there is not a limit for the number of courses that a student can be enrolled.
The uni needs to store the following data for each student: first_name, last_name, email, date_of_birth, state, gpa from high school, and if the student needs accessibility (for example, a room needs to have a ramp or an elevator so that a student in a wheelchair can get access to it). 

A room has a name, a maximum capacity, and can have or not projector and/or computers. Also, some of the rooms are accessible to students with disabilities. A room belongs to a building which also has a name. In the whole university there are no rooms with the same name. And the names of the buildings are also unique.
For each course there are several but well-defined evaluation types (exam_names). Evaluations will occur each one of them on a specific date and time(start time and end time), but the same evaluation can take place, and at the same time, in more than one room. An evaluation type might require or not a projector and/or computers. Attendance of each student for each evaluation type of a course in which the student is enrolled will be recorded and the grade achieved as well.

---
The project is composed by the following steps:

:dart:  **1. Creation of the UML (uml.png) and Relational Model (relational.txt):**
Based on the fields provided on the excel file, a UML model of the database was created and the related relation model. 


:gear:  **2. Creation of SQL script (grades.sql):**
This script will create the tables in the database.


:hourglass_flowing_sand:  **3. Load the Data into the Data Base (load_grades.py):**
To load the data form python using **DELETE** command to delete all records and **INSERT** command to popullate de database.

:joystick:  **4. User Interface (grades.py):**
An interface that allows to manage and interact with the grades database. T:

- allows the user to consult some information from the database.

:chart_with_upwards_trend:  **5. Extra (extra.py):**
In order to extract some meaningful information from the database four plots were created:

- Relation between age and time
- Relation between distance and time
- Relation between event and sex
- Relation between event year and distance
![image](https://github.com/silviatvares/Database-Grades/assets/116115008/591397e4-755b-4ffb-ad25-325d2c7f507e)
