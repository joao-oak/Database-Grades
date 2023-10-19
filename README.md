# Database-Grades
### FEUP, Faculty of Engineering, University of Porto Master in Data Science and Enginnering 
### Silvia Tavares, João Carvalho, Abílio Neves, Md. Wakil Ahmad
### Databases, October 2023
---
This project regards the design of a database for the grades, using the tools of SQL and Python. In order to have a better understanding, we created a storytelling to specify the requirements.

University JS is a university that offers its students an intensive 1-year associate degree that will prepare them to later enroll in a bachelor's degree of their choice. In order to improve its services, the university intends to use a database to store academic information for all students. For more information about the US education system, visit Education in the United States - Wikipedia.
As a pilot program to be started in the new academic year, 30 1-year associate degree students were chosen. These students are enrolled in 15 different courses and in the first semester.

A student must be enrolled in at least one course, and there is no limit to the number of courses a student can be enrolled in.
The university needs to store the following data for each student: first_name, last_name, email, date_of_birth, state, gpa and whether the student needs accessibility (for example, a room needs to have a ramp or elevator so that a student in wheelchair can have access to it). This information is not given in the dataset, but we decided to add so we make sure that if a student has special needs, the room needs to be appropriated.

A room has a name, maximum capacity and may or may not have a projector and/or computers. Additionally, some of the rooms are accessible to students with disabilities. A room belongs to a building that also has a name. The names of the buildings are unique.
For each course there are several types of assessment (exam_type), but they are defined. Each assessment will take place on a specific date and time (start time and end time), but the same assessment may take place, at the same date and time, in more than one room. The start time and end time are not in the dataset but given the fact that they are important fields, they are added in the database structure. A type of assessment may or may not require a projector and/or computers. The attendance of each student in each assessment modality of the course in which the student is enrolled will be recorded, as well as the grade obtained.

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

- Relation between age and time
- Relation between distance and time
- Relation between event and sex
- Relation between event year and distance
![image](https://github.com/silviatvares/Database-Grades/assets/116115008/591397e4-755b-4ffb-ad25-325d2c7f507e)
