from datetime import datetime, date
from mainapp import db, login_manager
from flask_login import UserMixin

 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    gender = db.Column(db.String(60), nullable=False)
    phonenumber = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(60), nullable=False)  
    contract = db.Column(db.Integer, nullable=False, default=3)
    academic_transcripts = db.Column(db.String(20), nullable=False,  default="user.png")
    personal_doc = db.Column(db.String(20), nullable=False, default="user.png")
    profile_image = db.Column(db.String(20), nullable=False, default="user.png")
    clients = db.relationship('Client', backref='user_therapist', lazy=True)
    schools = db.relationship('School', backref='school_therapist', lazy=True)
    schoolssessions = db.relationship('SchoolSession', backref='session_therapist', lazy=True)
    clientsessions = db.relationship('ClientSession', backref='session_therapist', lazy=True)
    notification = db.relationship('Notifications', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User {self.email}, role {self.role}"
    
    def get_uid(self):
        return self.id

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    gender = db.Column(db.String(60), nullable=False)
    phonenumber = db.Column(db.String(60), nullable=False)
    # occupation = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    reports = db.relationship('ClientReport', backref='report_client', lazy=True)
    sessions = db.relationship('ClientSession', backref='session_client', lazy=True)
    timetables = db.relationship('TimeTable', backref='timetable_client', lazy=True)
    
    def __repr__(self):
        return f"Client {self.email}, firstname {self.firstname}"

class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String, unique=True)
    school_principal = db.Column(db.String)
    date_of_registration = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contact_number = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    students = db.relationship('SchoolStudent', backref='student_school', lazy=True)
    sessions = db.relationship('SchoolSession', backref='session_school', lazy=True)
    timetables = db.relationship('SchoolTimeTable', backref='timetable_school', lazy=True)
    
    def __repr__(self):
        return f"School {self.email}, name {self.school_name}"

class SchoolStudent(db.Model):
    __tablename__ = 'school_students'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(60), nullable=False)
    lastname = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    gender = db.Column(db.String(60), nullable=False)
    phonenumber = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    diagnosis = db.Column(db.String, nullable=False)
    guardian_name = db.Column(db.String, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    reports = db.relationship('SchoolStudentReport', backref='report_student', lazy=True)
    sessions = db.relationship('SchoolStudentSession', backref='session_student', lazy=True)
    
    def __repr__(self):
        return f"Student {self.email}, firstname {self.firstname}"

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String, nullable=False, unique=True)
    room_number = db.Column(db.Integer, nullable=False, unique=True)
    def __repr__(self):
        return f"Room {self.room_number}, name {self.room_name}"

class ClientSession(db.Model):
    __tablename__ = 'client_sessions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    start_time = db.Column(db.Time, nullable=False,default=datetime.utcnow)
    end_time = db.Column(db.Time, nullable=False,default=datetime.utcnow)
    diagnosis = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    activities = db.relationship('SessionActivity', backref='activity_session', lazy=True )

    __table_args__ = (
        # ensure a room cannot have multiple sessions at the same time
        db.UniqueConstraint('room_id', 'start_time', 'end_time', name='unique_room_session'),
    )
    def __repr__(self):
        return f"Client session {self.date}, diagnosis {self.diagnosis}"

class SchoolSession(db.Model):
    __tablename__ = 'school_sessions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    start_time = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    diagnosis = db.Column(db.Text, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    students_sessions = db.relationship('SchoolStudentSession', backref='school_session', lazy=True)
    report = db.relationship('SchoolSessionReport', backref='school_session', lazy=True)
    
    
    def __repr__(self):
        return f"school session {self.date}, diagnosis {self.diagnosis}"

class ClientReport(db.Model):
    __tablename__ = 'client_reports'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    report_text = db.Column(db.String)
    
    def __repr__(self):
        return f"Client Report {self.report_text}"

class SchoolStudentReport(db.Model):
    __tablename__ = 'school_student_reports'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    school_student_id = db.Column(db.Integer, db.ForeignKey('school_students.id'))
    report_text = db.Column(db.String)
    
    def __repr__(self):
        return f"Student Report {self.report_text}"
    
class SchoolSessionReport(db.Model):
    __tablename__ = 'school_session_reports'
    id = db.Column(db.Integer, primary_key=True)
    school_session_id = db.Column(db.Integer, db.ForeignKey('school_sessions.id'))
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime)
    session_notes = db.Column(db.Text)
    session_outcome = db.Column(db.Text)
    
    
    def __repr__(self):
        return f"Student Report {self.session_notes}"

class SchoolStudentSession(db.Model):
    __tablename__ = 'school_student_sessions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    diagnosis = db.Column(db.Text, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('school_students.id'))
    school_session_id = db.Column(db.Integer, db.ForeignKey('school_sessions.id'))
    activities = db.relationship('StudentSessionActivity', backref='school_student_session', lazy=True)
    
    def __repr__(self):
        return f"Client session {self.date}, diagnosis {self.diagnosis}"

class SessionActivity(db.Model):
    __tablename__ = 'session_activities'
    id = db.Column(db.Integer, primary_key=True)
    session_date = db.Column(db.DateTime)
    overview = db.Column(db.Text)
    goals = db.Column(db.Text)
    notes = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    activity_text = db.Column(db.String)
    client_session_id = db.Column(db.Integer, db.ForeignKey('client_sessions.id'))
    
    def __repr__(self):
        return f"Session activity {self.id}, activity_description {self.activity_text}"
    
class StudentSessionActivity(db.Model):
    __tablename__ = 'student_session_activities'
    id = db.Column(db.Integer, primary_key=True)
    session_date = db.Column(db.DateTime)
    overview = db.Column(db.Text)
    goals = db.Column(db.Text)
    notes = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    activity_text = db.Column(db.String)
    school_session_id = db.Column(db.Integer, db.ForeignKey('school_sessions.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('school_student_sessions.id'))

class Notifications(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.String(255), db.ForeignKey("users.id"))
    note_type = db.Column(db.String(40), default="normal")
    note_body = db.Column(db.String(255), default="")
    date_generated = db.Column(db.DateTime,default=datetime.utcnow)
    # user = db.relationship("User", back_populates="notifications")
    
class TimeTable(db.Model):
    __tablename__ = 'timetables'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Time, nullable=False,default=datetime.utcnow)
    end_time = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f"timetable {self.day}, start_time {self.start_time}"
    

    
class SchoolTimeTable(db.Model):
    __tablename__ = 'school_timetables'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    start_time = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
 
    
    def __repr__(self):
        return f"timetable {self.day}, start_time {self.start_time}"
    
class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
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
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    article = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"Article {self.title}, role {self.subject}"