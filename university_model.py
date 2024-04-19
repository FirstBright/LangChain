from sqlalchemy import Column, String, Numeric, ForeignKey, CheckConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Classroom(Base):
    __tablename__ = 'classroom'
    building = Column(String(15), primary_key=True)
    room_number = Column(String(7), primary_key=True)
    capacity = Column(Numeric(4, 0))
    
class Department(Base):
    __tablename__ = 'department'
    dept_name = Column(String(20), primary_key=True)
    building = Column(String(15))
    budget = Column(Numeric(12, 2), CheckConstraint('budget > 0'))
    
class Course(Base):
    __tablename__ = 'course'
    course_id = Column(String(8), primary_key=True)
    title = Column(String(50))
    dept_name = Column(String(20), ForeignKey('department.dept_name', ondelete='SET NULL'))
    credits = Column(Numeric(2, 0), CheckConstraint('credits > 0'))
    department = relationship('Department', back_populates='courses')
    
Department.courses = relationship('Course', order_by=Course.course_id, back_populates='department')

class Instructor(Base):
    __tablename__ = 'instructor'
    ID = Column(String(5), primary_key=True)
    name = Column(String(20), nullable=False)
    dept_name = Column(String(20), ForeignKey('department.dept_name', ondelete='SET NULL'))
    salary = Column(Numeric(8, 2), CheckConstraint('salary > 29000'))
    department = relationship('Department', back_populates='instructors')

Department.instructors = relationship('Instructor', order_by=Instructor.ID, back_populates='department')

class Section(Base):
    __tablename__ = 'section'
    course_id = Column(String(8), ForeignKey('course.course_id', ondelete='CASCADE'), primary_key=True)
    sec_id = Column(String(8), primary_key=True)
    semester = Column(String(6), CheckConstraint("semester in ('Fall', 'Winter', 'Spring', 'Summer')"), primary_key=True)
    year = Column(Numeric(4, 0), CheckConstraint('year > 1701 and year < 2100'), primary_key=True)
    building = Column(String(15), ForeignKey('classroom.building', ondelete='SET NULL'))
    room_number = Column(String(7), ForeignKey('classroom.room_number', ondelete='SET NULL'))
    time_slot_id = Column(String(4))
    course = relationship('Course', back_populates='sections')
    classroom = relationship('Classroom')

Course.sections = relationship('Section', order_by=Section.sec_id, back_populates='course')

class Teaches(Base):
    __tablename__ = 'teaches'
    ID = Column(String(5), ForeignKey('instructor.ID', ondelete='CASCADE'), primary_key=True)
    course_id = Column(String(8), primary_key=True)
    sec_id = Column(String(8), primary_key=True)
    semester = Column(String(6), primary_key=True)
    year = Column(Numeric(4, 0), primary_key=True)
    instructor = relationship('Instructor', back_populates='teaches')
    section = relationship('Section')

Instructor.teaches = relationship('Teaches', order_by=Teaches.course_id, back_populates='instructor')
Section.teaches = relationship('Teaches', uselist=False, back_populates='section')

class Student(Base):
    __tablename__ = 'student'
    ID = Column(String(5), primary_key=True)
    name = Column(String(20), nullable=False)
    dept_name = Column(String(20), ForeignKey('department.dept_name', ondelete='SET NULL'))
    tot_cred = Column(Numeric(3, 0), CheckConstraint('tot_cred >= 0'))
    department = relationship('Department', back_populates='students')

Department.students = relationship('Student', order_by=Student.ID, back_populates='department')

class Takes(Base):
    __tablename__ = 'takes'
    ID = Column(String(5), ForeignKey('student.ID', ondelete='CASCADE'), primary_key=True)
    course_id = Column(String(8), primary_key=True)
    sec_id = Column(String(8), primary_key=True)
    semester = Column(String(6), primary_key=True)
    year = Column(Numeric(4, 0), primary_key=True)
    grade = Column(String(2))
    student = relationship('Student', back_populates='takes')
    section = relationship('Section')

Student.takes = relationship('Takes', order_by=Takes.course_id, back_populates='student')
Section.takes = relationship('Takes', back_populates='section')

class Advisor(Base):
    __tablename__ = 'advisor'
    s_ID = Column(String(5), ForeignKey('student.ID', ondelete='CASCADE'), primary_key=True)
    i_ID = Column(String(5), ForeignKey('instructor.ID', ondelete='SET NULL'))
    student = relationship('Student', back_populates='advisor')
    instructor = relationship('Instructor', back_populates='advisor')

Student.advisor = relationship('Advisor', uselist=False, back_populates='student')
Instructor.advisor = relationship('Advisor', back_populates='instructor')

class TimeSlot(Base):
    __tablename__ = 'time_slot'
    time_slot_id = Column(String(4), primary_key=True)
    day = Column(String(1), primary_key=True)
    start_hr = Column(Numeric(2), CheckConstraint('start_hr >= 0 and start_hr < 24'), primary_key=True)
    start_min = Column(Numeric(2), CheckConstraint('start_min >= 0 and start_min < 60'), primary_key=True)
    end_hr = Column(Numeric(2), CheckConstraint('end_hr >= 0 and end_hr < 24'))
    end_min = Column(Numeric(2), CheckConstraint('end_min >= 0 and end_min < 60'))

class Prereq(Base):
    __tablename__ = 'prereq'
    course_id = Column(String(8), ForeignKey('course.course_id', ondelete='CASCADE'), primary_key=True)
    prereq_id = Column(String(8), ForeignKey('course.course_id'), primary_key=True)
    course = relationship('Course', foreign_keys=[course_id], back_populates='prereq_course')
    prereq_course = relationship('Course', foreign_keys=[prereq_id], back_populates='course')

Course.prereq_course = relationship('Prereq', foreign_keys=[Prereq.prereq_id], back_populates='prereq_course')
Course.course = relationship('Prereq', foreign_keys=[Prereq.course_id], back_populates='course')
