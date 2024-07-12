from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, StringField, PasswordField, EmailField, SubmitField, DateField, SelectField, TextAreaField, IntegerField, FileField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from mainapp.models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()], render_kw={'required': False})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')
    

    
class ForgottenPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
  
    
class PasswordResetForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')
    
    
class AddUserForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    role = SelectField('User Role', choices=[('admin', 'Admin'), ('therapist', 'Therapist')], validators=[DataRequired()])
    contract = IntegerField('Contract', validators=[DataRequired()])
    academic_transcripts = FileField('Academic Transcripts', validators=[
        FileAllowed(['pdf'], 'Only PDF files are allowed for academic transcripts')
    ])
    personal_doc = FileField('Personal Document', validators=[
        FileAllowed(['pdf'], 'Only PDF files are allowed for personal documents')
    ])
    submit = SubmitField('Add User')
    
    
    def validate_email(self, email):
        user  = User.query.filter_by(email=email.data).first()
 
        if user: 
            raise ValidationError('That Email Already Exists')
    
class EditUserForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    address = TextAreaField('Address')
    profile_image = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Only images are allowed')
    ])
    password = PasswordField('Current Password', validators=[DataRequired()])
    submit = SubmitField("Update")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user  = User.query.filter_by(email=email.data).first()
    
            if user: 
                raise ValidationError('That Email Already Exists')
    
class AddClientForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired()])
    submit = SubmitField('Add Client')
    
class AddStudentForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired()])
    guardian_name = StringField("Guardian", validators=[DataRequired()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Add Client')
    
    
class AddRoomForm(FlaskForm):
    room_name = StringField('Room Name', validators=[DataRequired()])
    room_number = IntegerField('Room Number', validators=[DataRequired()])
    submit = SubmitField('Add Room')
    
    
class AddSchoolForm(FlaskForm):
    school_name = StringField('School Name', validators=[DataRequired()])
    school_principal = StringField('Principal', validators=[DataRequired()])
    date_of_registration = DateField('Date of Reg', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Add School')
    
    
class ContactForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={'placeholder': 'Enter your firstname'})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={'placeholder': 'Enter your lastname'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Enter your email'})
    subject = StringField('Subject', validators=[DataRequired()], render_kw={'placeholder': 'Enter the subject'})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={'placeholder': 'Enter your message'})
    submit = SubmitField('Submit')
    
class HelpArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    article = TextAreaField('Article Content', validators=[DataRequired()])
    submit = SubmitField('Create Article')
    
    
location_choices = {
    'room_1': 'Room 1',
    'room_2': 'Room 2',
    'room_3': 'Room 3'
}



class ScheduleClientSessionForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    location = SelectField('Location', choices=[(key, value) for key, value in location_choices.items()], validators=[DataRequired()])
    # therapist = SelectField('Therapist', choices=[], validators=[DataRequired()])
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired()])
    submit = SubmitField('Schedule Session')
    


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.therapist.choices = [(t.id, f"{t.firstname} {t.lastname}") for t in User.query.all()]
    
    
class ScheduleSchoolSessionForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    # therapist = SelectField('Therapist', choices=[], validators=[DataRequired()])
    diagnosis = TextAreaField('Diagnosis', validators=[DataRequired()])
    submit = SubmitField('Schedule Session')
    

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.therapist.choices = [(t.id, f"{t.firstname} {t.lastname}") for t in User.query.all()]

class ReportForm(FlaskForm):
    field_name = StringField('Field Name', validators=[DataRequired()])
    report_case = TextAreaField('Report Case', validators=[DataRequired()])

class ReportDynamicForm(FlaskForm):
    report_cases = FieldList(FormField(ReportForm), min_entries=1)
    submit = SubmitField('Submit')
    
class SchoolSessionReportForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    session_notes = TextAreaField('Session Notes', validators=[DataRequired()])
    session_outcome = TextAreaField('Session Outcome', validators=[DataRequired()]) 
    submit = SubmitField('Submit')

class ActivityForm(FlaskForm):
    activity_name = StringField('Activity Name')
    activity_description = TextAreaField('Description')
    progress = TextAreaField('Progress')

class SessionForm(FlaskForm):
    session_date = DateField('Date')
    overview = TextAreaField('Overview')
    goals = TextAreaField('Goals')
    activities = FieldList(FormField(ActivityForm), min_entries=1)
    notes = TextAreaField('Notes')
    recommendations = TextAreaField('Recommendations')
    submit = SubmitField('Submit')
    

class TimeTableForm(FlaskForm):
    day = SelectField('Day', choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    
class AssignTherapist(FlaskForm):
    therapist = SelectField('Therapist', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.therapist.choices = [(t.id, f"{t.firstname} {t.lastname}") for t in User.query.all()]