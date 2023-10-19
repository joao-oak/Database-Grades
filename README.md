# Database-Grades
### FEUP, Faculty of Engineering, University of Porto Master in Data Science and Enginnering 
### Silvia Tavares, João Carvalho, Abílio Neves, Md. Wakil Ahmad
### Databases, October 2023
---
This project regards the design of a database for the grades, using the tools of SQL and Python and it’s constituted by the following steps:

:dart:  **1. Creation of the UML (uml.png file) and Relational Model (relational.txt):**
Based on the fields provided on the excel file, a UML model of the database was created and the related relation model. Several decisions were made like calculating the age based on the birth date of the runner, create a separated tables for certain details, like event type, age class, etc.


:gear:  **2. Creation of SQL script (races.sql):**
This script will create the tables in the database.


:hourglass_flowing_sand:  **3. Load the Data into the Data Base (load_races.py):**
To load the data form python into the SQL database several actions were done since the excel file was not compliant with the format of the database tables and contains many errors. Some of that actions were:

Conversion of the data types;
Remove duplicated lines;
Creation of a Age Class table with an automatic determination;
Treat the null entries
Check backlash cells;

:joystick:  **4. User Interface (races.py):**
An interface that allows to manage and interact with the races database. At the moment, a few functionalities were developed like:

Read, delete, update, insert a record for runners where validations were put in place to not allow the user to insert wrong information on the database,
FAQS: allows the user to consult some information from the database.

:chart_with_upwards_trend:  **5. Extra (extra.py):**
In order to extract some meaningful information from the database four plots were achieved:

- Relation between age and time
- Relation between distance and time
- Relation between event and sex
- Relation between event year and distance
![image](https://github.com/silviatvares/Database-Grades/assets/116115008/591397e4-755b-4ffb-ad25-325d2c7f507e)
