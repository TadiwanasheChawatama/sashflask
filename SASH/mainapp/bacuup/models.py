from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, date


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sash.db'


db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    gender = db.Column(db.String(60), nullable=False)
    phonenumber = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(60), nullable=False)  # either 'admin' or 'therapist'
    contract = db.Column(db.Integer, nullable=False, default=3)
    academic_transcripts = db.Column(db.String(20), nullable=False)
    personal_doc = db.Column(db.String(20), nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default="static/images/user.png")
    client_assignments = db.relationship('Client', secondary='user_clients', backref=db.backref('assigned_therapists', lazy='dynamic'), lazy='dynamic')
    schools = db.relationship('School', secondary='user_schools', backref=db.backref('school_users', lazy='dynamic'), lazy='dynamic')
    
    def __repr__(self):
        return f"User {self.email}, role {self.role}"

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(60), nullable=False)
    phonenumber = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    diagnosis = db.Column(db.String, nullable=False)
    therapist = db.relationship('User', secondary='user_clients', backref=db.backref('client_assignments', lazy='dynamic'), lazy='dynamic')
    reports = db.relationship('ClientReport', backref='client', lazy='dynamic')
    sessions = db.relationship('ClientSession', backref='client', lazy='dynamic')

class UserClient(db.Model):
    __tablename__ = 'user_clients'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), primary_key=True)

class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String)
    date_of_registration = db.Column(db.DateTime, nullable=False)
    contact_number = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    therapists = db.relationship('User', secondary='user_schools', backref=db.backref('schools', lazy='dynamic'), lazy='dynamic')
    students = db.relationship('SchoolStudent', backref='school', lazy='dynamic')
    sessions = db.relationship('SchoolSession', backref='school', lazy='dynamic')
    timetables = db.relationship('TimeTable', backref='school', lazy='dynamic')

class UserSchool(db.Model):
    __tablename__ = 'user_schools'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), primary_key=True)

class SchoolStudent(db.Model):
    __tablename__ = 'school_students'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(60), nullable=False)
    phonenumber = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    diagnosis = db.Column(db.String, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    reports = db.relationship('SchoolStudentReport', backref='school_student', lazy='dynamic')
    sessions = db.relationship('SchoolStudentSession', backref='school_student', lazy='dynamic')

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String, nullable=False)
    room_number = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Room {self.room_number}, name {self.room_name}"

class ClientSession(db.Model):
    __tablename__ = 'client_sessions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    therapist = db.relationship('User', backref=db.backref('client_sessions', lazy='dynamic'))
    client = db.relationship('Client', backref=db.backref('client_sessions', lazy='dynamic'))
    room = db.relationship('Room', backref=db.backref('client_sessions', lazy='dynamic'))
    activities = db.relationship('SessionActivity', backref='client_session', lazy='dynamic')

    __table_args__ = (
        # ensure a room cannot have multiple sessions at the same time
        db.UniqueConstraint('room_id', 'start_time', 'end_time', name='unique_room_session'),
    )

class SchoolSession(db.Model):
    __tablename__ = 'school_sessions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    therapist = db.relationship('User', backref=db.backref('school_sessions', lazy='dynamic'))
    school = db.relationship('School', backref=db.backref('school_sessions', lazy='dynamic'))
    room = db.relationship('Room', backref=db.backref('school_sessions', lazy='dynamic'))
    students = db.relationship('SchoolSessionStudent', backref='school_session', lazy='dynamic')

class SchoolSessionStudent(db.Model):
    __tablename__ = 'school_session_students'
    id = db.Column(db.Integer, primary_key=True)
    school_session_id = db.Column(db.Integer, db.ForeignKey('school_sessions.id'))
    school_student_id = db.Column(db.Integer, db.ForeignKey('school_students.id'))
    school_session = db.relationship('SchoolSession', backref=db.backref('school_session_students', lazy='dynamic'))
    school_student = db.relationship('SchoolStudent', backref=db.backref('school_session_students', lazy='dynamic'))
    activities = db.relationship('SessionActivity', backref='school_session_student', lazy='dynamic')

class ClientReport(db.Model):
    __tablename__ = 'client_reports'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    report_text = db.Column(db.String)

class SchoolStudentReport(db.Model):
    __tablename__ = 'school_student_reports'
    id = db.Column(db.Integer, primary_key=True)
    school_student_id = db.Column(db.Integer, db.ForeignKey('school_students.id'))
    report_text = db.Column(db.String)

class SchoolStudentSession(db.Model):
    __tablename__ = 'school_student_sessions'
    id = db.Column(db.Integer, primary_key=True)
    school_student_id = db.Column(db.Integer, db.ForeignKey('school_students.id'))
    school_session_id = db.Column(db.Integer, db.ForeignKey('school_sessions.id'))
    activities = db.relationship('SessionActivity', backref='school_student_session')

class SessionActivity(db.Model):
    __tablename__ = 'session_activities'
    id = db.Column(db.Integer, primary_key=True)
    activity_text = db.Column(db.String)
    client_session_id = db.Column(db.Integer, db.ForeignKey('client_sessions.id'))
    school_student_session_id = db.Column(db.Integer, db.ForeignKey('school_student_sessions.id'))
    client_session = db.relationship('ClientSession', backref=db.backref('session_activities', lazy='dynamic'))
    school_session_student = db.relationship('SchoolSessionStudent', backref=db.backref('session_activities', lazy='dynamic'))
    
    
class TimeTable(db.Model):
    __tablename__ = 'timetables'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f"timetable {self.day}, start_time {self.start_time}"
    
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"contact {self.email}, subject {self.subject}"

class HelpArticle(db.Model):
    __tablename__ = 'help_articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    article = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"Article {self.title}, role {self.subject}"