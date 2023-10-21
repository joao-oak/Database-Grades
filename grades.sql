/****************************************************************************************************
*****************************************************************************************************

								DDL - Data Definition Language - Part I

*****************************************************************************************************
*****************************************************************************************************
*/


DROP SCHEMA IF EXISTS grades CASCADE; 
CREATE SCHEMA grades;

SET search_path = grades;

DROP TRIGGER IF EXISTS trigger_validate_exam_room_capacity ON attendance;
DROP TRIGGER IF EXISTS trigger_validate_exam_room_constraints ON attendance;

DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS attendance;


--Tables in which the primary key is referenced as foreign key in other tables
DROP TABLE IF EXISTS building CASCADE;
DROP TABLE IF EXISTS course CASCADE;
DROP TABLE IF EXISTS exam_type CASCADE;
DROP TABLE IF EXISTS exam CASCADE;
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS room CASCADE;


CREATE TABLE building (
  building_id SERIAL PRIMARY KEY,
  building_name VARCHAR(32) UNIQUE NOT NULL  
);

CREATE TABLE course (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(64) UNIQUE NOT NULL 
);

CREATE TABLE exam_type (
    type_id SERIAL PRIMARY KEY,
    exam_name VARCHAR(32) UNIQUE NOT NULL 
);

CREATE TABLE student (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    /*
    --email VARCHAR(100) GENERATED ALWAYS AS (
		--lower(first_name) || '.' || lower(last_name) || '@' || 'jsuniversity.edu') STORED, -- doesn't work in Postgre 9.4
	*/
    date_of_birth DATE,
    gpa NUMERIC(5,2)
    	CONSTRAINT gpa_range CHECK (gpa BETWEEN 0.00 and 4.00),
    state VARCHAR(32),
    needs_accessibility BOOLEAN DEFAULT FALSE
);

CREATE TABLE room (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(32) UNIQUE NOT NULL,
    capacity SMALLINT
        CONSTRAINT positive_capacity CHECK (capacity>0),
    has_projector BOOLEAN DEFAULT FALSE,
    has_computers BOOLEAN DEFAULT FALSE,
    is_accessible BOOLEAN DEFAULT FALSE,
    building_id INTEGER NOT NULL 
        REFERENCES building(building_id) 
            ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE exam (
    exam_id SERIAL PRIMARY KEY,
    exam_date DATE,
    start_time TIME,
    end_time TIME,
    course_id INTEGER NOT NULL 
        REFERENCES course(course_id) 
            ON DELETE CASCADE ON UPDATE CASCADE,
    type_id INTEGER NOT NULL 
        REFERENCES exam_type(type_id) 
            ON DELETE CASCADE ON UPDATE cascade,
    needs_projector BOOLEAN DEFAULT FALSE,
    needs_computers BOOLEAN DEFAULT FALSE
);

CREATE TABLE enrollment ( 
    student_id INTEGER 
    	REFERENCES student(student_id)
    		ON DELETE CASCADE ON UPDATE CASCADE,
    course_id INTEGER NOT NULL
    	REFERENCES course(course_id)  
    		ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(student_id,course_id)
);

CREATE TABLE attendance (
    student_id INTEGER
        REFERENCES student(student_id)
            ON DELETE CASCADE ON UPDATE CASCADE,
    exam_id INTEGER
        REFERENCES exam(exam_id)
            ON DELETE CASCADE ON UPDATE CASCADE,
    room_id INTEGER
        REFERENCES room(room_id) 
            ON DELETE SET NULL ON UPDATE CASCADE,
    grade NUMERIC(5,2)
    	CONSTRAINT grade_range CHECK (grade BETWEEN 0.00 and 100.00),
    has_attended BOOLEAN,
    PRIMARY KEY(student_id, exam_id)
);



/****************************************************************************************************
*****************************************************************************************************

				DDL - Data Definition Language - Part II: functions and triggers

*****************************************************************************************************
*****************************************************************************************************
*/


CREATE OR REPLACE FUNCTION validate_exam_room_capacity()
RETURNS TRIGGER AS $$
BEGIN
    -- Calculate the total number of students for the exam
    DECLARE
        total_students smallint;
    BEGIN
        SELECT COUNT(student_id)
        INTO total_students
        FROM attendance
        WHERE exam_id = NEW.exam_id;
        
        -- Check if the total_students exceeds the room capacity
        IF total_students > (SELECT capacity FROM room WHERE room_id = NEW.room_id) THEN
            RAISE EXCEPTION 'Total students exceed room capacity for exam_id %', NEW.exam_id;
        END IF;
    END;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_validate_exam_room_capacity
BEFORE INSERT OR UPDATE ON attendance
FOR EACH ROW
EXECUTE PROCEDURE validate_exam_room_capacity();


CREATE OR REPLACE FUNCTION validate_exam_room_constraints()
RETURNS TRIGGER AS $$
BEGIN
    -- Check needs_accessibility of the student
    IF EXISTS (
        SELECT 1 
        FROM student s 
        WHERE s.student_id = NEW.student_id AND (s.needs_accessibility IS TRUE OR s.needs_accessibility IS NULL)
    ) AND EXISTS (
        SELECT 1 
        FROM room r 
        WHERE r.room_id = NEW.room_id AND (r.is_accessible = FALSE OR r.is_accessible IS NULL)
    ) THEN
        RAISE EXCEPTION 'Student with needs_accessibility=true can only take exams in accessible rooms';
    END IF;
    
    -- Check needs_projector of the exam
    IF EXISTS (
        SELECT 1 
        FROM exam e 
        WHERE e.exam_id = NEW.exam_id AND (e.needs_projector IS TRUE OR e.needs_projector IS NULL)
    ) AND EXISTS (
        SELECT 1 
        FROM room r 
        WHERE r.room_id = NEW.room_id AND (r.has_projector = FALSE OR r.has_projector IS NULL)
    ) THEN
        RAISE EXCEPTION 'Exams with needs_projector=true can only take place in rooms with projectors';
    END IF;

    -- Check needs_computers of the exam
    IF EXISTS (
        SELECT 1 
        FROM exam e 
        WHERE e.exam_id = NEW.exam_id AND (e.needs_computers IS TRUE OR e.needs_computers IS NULL)
    ) AND EXISTS (
        SELECT 1 
        FROM room r 
        WHERE r.room_id = NEW.room_id AND (r.has_computers = FALSE OR r.has_computers IS NULL)
    ) THEN
        RAISE EXCEPTION 'Exams with needs_computers=true can only take place in rooms with computers';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_validate_exam_room_constraints
BEFORE INSERT OR UPDATE ON attendance
FOR EACH ROW
EXECUTE PROCEDURE validate_exam_room_constraints();






