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
    clients = db.relationship('Client', backref='therapist', lazy=True)
    clients_sessions = db.relationship('ClientSession', backref='therapist', lazy=True)
    schools = db.relationship('School', backref='therapist', lazy=True)
    
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
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reports = db.relationship('Report', backref='client', lazy=True)
    sessions = db.relationship('ClientSession', backref='client', lazy=True)
    timetables = db.relationship('TimeTable', backref='client', lazy=True)
    
    def __repr__(self):
        return f"Client {self.email}, firstname {self.firstname}"

class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String)
    date_of_registration = db.Column(db.DateTime, nullable=False)
    contact_number = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    students = db.relationship('Student', backref='school', lazy='dynamic')
    sessions = db.relationship('SchoolSession', backref='school', lazy='dynamic')
    timetables = db.relationship('TimeTable', backref='school', lazy='dynamic')
    
    def __repr__(self):
        return f"School {self.email}, name {self.school_name}"

class Student(db.Model):
    __tablename__ = 'students'
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
    reports = db.relationship('StudentReport', backref='student', lazy='dynamic')
    sessions = db.relationship('StudentSession', backref='student', foreign_keys='[ClientSession.student_id]', lazy='dynamic')

    def __repr__(self):
        return f"Student {self.email}, firstname {self.firstname}"

class TherapyRoom(db.Model):
    __tablename__ = 'therapy_rooms'
    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String, nullable=False)
    room_number = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Room {self.room_number}, name {self.room_name}"

class SchoolSession(db.Model):
    __tablename__ = 'school_sessions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    therapist = db.relationship('User', backref='school_sessions')
    students = db.relationship('Student', secondary='session_students')
    
    def __repr__(self):
        return f"school session {self.date}, diagnosis {self.diagnosis}"

class RoomBooking(db.Model):
    __tablename__ = 'room_bookings'
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('therapy_rooms.room_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('client_sessions.id'), unique=True)
    session = db.relationship('ClientSession', backref=db.backref('room_booking_relation', uselist=False))

    __table_args__ = (
        db.UniqueConstraint('room_id', 'start_time', 'end_time', name='unique_room_booking'),
    )
    
class ClientSession(db.Model):
    __tablename__ = 'client_sessions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # activities = db.relationship('SessionActivity', backref='session', lazy='dynamic')
    # room_booking_relation = db.relationship('RoomBooking', backref='client_session', uselist=False)

    def __repr__(self):
        return f"Client session {self.date}, diagnosis {self.diagnosis}"
    
class StudentSession(db.Model):
    __tablename__ = 'student_sessions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # activities = db.relationship('SessionActivity', backref='session', lazy='dynamic')
    # room_booking_relation = db.relationship('RoomBooking', backref='client_session', uselist=False)

    def __repr__(self):
        return f"Client session {self.date}, diagnosis {self.diagnosis}"

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    report_fields = db.relationship('ReportField', backref='report', lazy='dynamic')
    
    def __repr__(self):
        return f"Report {self.report_fields}"
    
class StudentReport(db.Model):
    __tablename__ = 'student_reports'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    report_fields = db.relationship('ReportField', backref='report', lazy='dynamic')
    
    def __repr__(self):
        return f"Report {self.report_fields}"

class ReportField(db.Model):
    __tablename__ = 'report_fields'
    id = db.Column(db.Integer, primary_key=True)
    field_name = db.Column(db.String, nullable=False)
    case_history = db.Column(db.Text, nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)

class SessionActivity(db.Model):
    __tablename__ = 'session_activities'
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String, nullable=False)
    activity_description = db.Column(db.Text, nullable=False)
    progress = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('client_sessions.id'), nullable=False)
    
    def __repr__(self):
        return f"Session activity {self.activity_name}, activity_description {self.activity_description}"

class SessionStudents(db.Model):
    __tablename__ = 'session_students'
    session_id = db.Column(db.Integer, db.ForeignKey('school_sessions.id'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)  
    
    def __repr__(self):
        return f"User {self.session_id}" 
    
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