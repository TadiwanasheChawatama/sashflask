from flask import render_template,  request, session, redirect, url_for, flash, jsonify, abort
from mainapp import app, db, bcrypt, create_upload_folder, UPLOAD_FOLDER
from mainapp.Forms import AddUserForm, LoginForm,ReportDynamicForm, SessionForm,ForgottenPasswordForm,PasswordResetForm, AddClientForm, AddRoomForm, AddSchoolForm,  ContactForm, HelpArticleForm, ScheduleClientSessionForm, ScheduleSchoolSessionForm, EditUserForm, SchoolSessionReportForm, AddStudentForm, TimeTableForm, AssignTherapist
from mainapp.models import User, Client, School, SchoolStudent, Room, ClientSession, SchoolSession,ClientReport, SchoolStudentReport, SchoolSessionReport, SchoolStudentSession, SessionActivity, StudentSessionActivity,TimeTable, SchoolTimeTable, Contact, HelpArticle, Notifications
from datetime import datetime
from werkzeug.utils import secure_filename
import json , os, secrets
from PIL import Image
from flask_login import login_user, current_user , logout_user, login_required



# ################################ General Routes ##################################################

@app.route("/admin")
@login_required
def Home():
    current_date = datetime.now().strftime('%Y-%m-%d')
    profile_image = url_for("static", filename='images/' + current_user.profile_image)
    return render_template('admin.html', current_date=current_date, title='home', datetime=datetime, profile_image=profile_image)
  
@app.route("/")
def Index():
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('Home.html', datetime=datetime)


@app.route('/set_theme', methods =['POST'])
@login_required
def set_theme():
    print("Received set_theme request")
    try:
        theme = request.json['theme']
        print(f"Theme value: {theme}")
        session['theme'] = theme
        return 'Theme updated'
    except Exception as e:
        print(f"Error: {e}")
        return 'Error updating theme', 400


@app.route('/manage')
@login_required
def manage():
  return render_template('manage.html')


@app.route('/schools')
@login_required
def schools():
  schools = School.query.all()
  return render_template('schools.html', schools=schools)




@app.route('/students')
@login_required
def students():
  all_students = SchoolStudent.query.all()
  return render_template('students.html', all_students = all_students)



def check_client_timetable_conflict(client_id, day, start_time, end_time):
    existing_timetables = TimeTable.query.filter_by(client_id=client_id, day=day).all()
    for timetable in existing_timetables:
        if (start_time >= timetable.start_time and start_time < timetable.end_time) or \
           (end_time > timetable.start_time and end_time <= timetable.end_time):
            return False
    return True
  
@app.route('/timetable/<int:client_id>', methods=['GET', 'POST'])
@login_required
def timetable(client_id):
    form = TimeTableForm()
    client = Client.query.get_or_404(client_id)
    if form.validate_on_submit():
        if check_client_timetable_conflict(client_id, form.day.data, form.start_time.data, form.end_time.data):
            timetable = TimeTable(day=form.day.data, start_time=form.start_time.data, end_time=form.end_time.data)
            db.session.add(timetable)
            client.timetables.append(timetable)
            db.session.commit()
            flash(f'Timetable successfully added', 'success')
        else:
            flash(f'Timetable conflicts with existing timetable', 'danger')
    return render_template('timetable.html', form=form, client=client)
  
@app.route('/timetable/<int:client_id>/delete/<int:timetable_id>/', methods=['GET', 'POST'])
@login_required
def delete_timetable(timetable_id, client_id):
    client = Client.query.get_or_404(client_id)
    timetable = TimeTable.query.get_or_404(timetable_id)
    client.timetables.remove(timetable)
    db.session.commit()
    flash(f'Timetable successfully removed', 'success')
    return redirect(url_for("timetable", client_id=client.id))



@app.route('/users')
@login_required
def Users():
  all_users = User.query.all()
  return render_template('users.html', all_users=all_users)


@app.route('/clients')
@login_required
def clients():
  
  all_clients = Client.query.all()
  
  return render_template('clients.html', all_clients = all_clients)


@app.route('/sessionmenu')
@login_required
def sessionmenu():
  all_client_session = ClientSession.query.all()
  all_school_session = SchoolSession.query.all()
  return render_template('sessionmenu.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
  
  if form.validate_on_submit():
    message = Contact(firstname = form.firstname.data, lastname=form.lastname.data, email=form.email.data, subject = form.subject.data, message = form.message.data )
    db.session.add(message)
    db.session.commit()
    flash(f'Mail sent successfully', 'success')
    return redirect(url_for('contact'))
  else:
      return render_template('contact.html', datetime = datetime, form=form)






@app.route('/analytics')
@login_required
def analytics():
  return render_template('analytics.html')

@app.route('/messages')
@login_required
def messages():
  return render_template('messages.html')

@app.route('/help_center', methods=["POST", "GET"])
@login_required
def help_center():
  form = HelpArticleForm()
  if form.validate_on_submit():
    title = form.title.data
    subject = form.subject.data
    article = form.article.data
    
    if article != "":
        flash(f'{article} created', 'success')
        return redirect(url_for('help_center'))
    else:
        flash('Provide a valid article', 'danger')
        return render_template('help_center.html', form=form, title='help_center')
  else:
      return render_template('help_center.html', form=form, title='help_center')










# ################################## User Routes #################################################


@app.route('/login', methods=['POST', "GET"])
def login(): 
    if current_user.is_authenticated:
      return redirect(url_for('Home'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Home'))
        else:
            error_message = 'Invalid email or password'
            return jsonify({'error': error_message})
    return render_template('login.html', form=form, title='Login')



@app.route('/userprofile/<int:user_id>')
@login_required
def userprofile(user_id):
    user = User.query.get_or_404(user_id)
    schools = user.schools
    students = [student for school in user.schools for student in school.students]
    clients = user.clients
    schoolssessions = user.schoolssessions
    clientsessions = user.clientsessions
    profile_image = url_for("static", filename='images/' + user.profile_image)
    return  render_template('userprofile.html', user = user, profile_image=profile_image, schools=schools, clients=clients, students=students, schoolsession= schoolssessions, clientsessions=clientsessions)



@app.route('/userprofile/<int:user_id>/update', methods=['POST', "GET"])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AddUserForm()
    if form.validate_on_submit():
        create_upload_folder()

        # Handle file uploads
        academic_transcripts = request.files['academic_transcripts']
        personal_doc = request.files['personal_doc']

        email = user.email

        if academic_transcripts:
            academic_transcripts_filename = f"{email}_academic_transcripts.{academic_transcripts.filename.split('.')[-1]}"
            academic_transcripts.save(os.path.join(UPLOAD_FOLDER, academic_transcripts_filename))
            user.academic_transcripts = academic_transcripts_filename
        if personal_doc:
            personal_doc_filename = f"{email}_personal_doc.{personal_doc.filename.split('.')[-1]}"
            personal_doc.save(os.path.join(UPLOAD_FOLDER, personal_doc_filename))
            user.personal_doc = personal_doc_filename

        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.date_of_birth = form.date_of_birth.data
        user.gender = form.gender.data
        user.phonenumber = form.phonenumber.data
        user.address = form.address.data
        user.role = form.role.data
        user.contract = form.contract.data

        db.session.commit()
        flash(f'User {form.email.data} successfully updated', 'success')
        return redirect(url_for('Users'))

    elif request.method == "GET":
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.date_of_birth.data = user.date_of_birth
        form.gender.data = user.gender
        form.phonenumber.data = user.phonenumber
        form.contract.data = user.contract
        form.email.data = user.email
        form.address.data = user.address
        form.role.data = user.role
        form.academic_transcripts.data = user.academic_transcripts
        form.personal_doc.data = user.personal_doc

    return render_template('adduser.html', form=form, title='Update User', password=False)


@app.route('/adduser', methods=['POST', "GET"])
@login_required
def adduser():
  form = AddUserForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    create_upload_folder()
    
       # Handle file uploads
    academic_transcripts = request.files['academic_transcripts']
    personal_doc = request.files['personal_doc']
    
    # Create unique filenames for each file
    email = form.email.data
    academic_transcripts_filename = f"{email}_academic_transcripts.{academic_transcripts.filename.split('.')[-1]}"
    personal_doc_filename = f"{email}_personal_doc.{personal_doc.filename.split('.')[-1]}"
    
    # Save files to disk
    academic_transcripts.save(os.path.join(UPLOAD_FOLDER, academic_transcripts_filename))
    personal_doc.save(os.path.join(UPLOAD_FOLDER, personal_doc_filename))
    
    
    
    user = User(firstname = form.firstname.data,lastname = form.lastname.data,date_of_birth = form.date_of_birth.data,gender = form.gender.data,phonenumber = form.phonenumber.data,email = form.email.data,password =hashed_password ,address = form.address.data,role = form.role.data,contract = form.contract.data, academic_transcripts=academic_transcripts_filename, personal_doc=personal_doc_filename)
    
    db.session.add(user)
    db.session.commit()
    flash(f'User {form.email.data} successfully added', 'success')
    return redirect(url_for('Users'))
  else:
      return render_template('adduser.html', form=form, title='Add User' ,password=True)




@app.route('/forgotten_password', methods=['GET', 'POST'])
@login_required
def forgotten_password():
  form= ForgottenPasswordForm()
  if form.validate_on_submit():
    email = form.email.data
    
    if email != "":
        flash(f'user {email} password reset code sent to your email', 'success')
        return redirect(url_for('forgotten_password'))
    else:
        flash('Provide a valid email', 'danger')
        return render_template('forgotten_password.html', form=form, title='forgotten_password')
  else:
      return render_template('forgotten_password.html', form=form, title='forgotten_password')



@app.route("/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
  form=PasswordResetForm()
  if form.validate_on_submit():
    email = form.email.data
    
    if email != "":
      flash(f'user {email} password reset code sent to your email', 'success')
      return redirect(url_for('Home'))
    else:
      flash('Provide a valid email', 'danger')
      return render_template('change_password.html', form=form, title='change_password')
  else:
      return render_template('change_password.html', form=form, title='change_password')

def save_picture(form_pic):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_pic.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/images/' , picture_fn)
  
  output_size = (125, 125)
  i = Image.open(form_pic)
  i.thumbnail(output_size)
  i.save(picture_path)
  delete_picture_prev()
  return picture_fn

def delete_picture_prev():
    prev_pic = os.path.join(app.root_path, 'static/images/', current_user.profile_image)
    if os.path.exists(prev_pic):
        os.remove(prev_pic)
        return True

@app.route("/edit_user_info", methods=["POST", "GET"])
@login_required
def edit_user_info():
    form = EditUserForm()

    if form.validate_on_submit():
        if form.profile_image.data:
            picture_file = save_picture(form.profile_image.data)
            current_user.profile_image = picture_file
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            try:
                current_user.email = form.email.data
                current_user.address = form.address.data
                db.session.commit()
                flash(f'User info successfully updated', 'uccess')
                return redirect(url_for('Home'))
            except Exception as e:
                flash(f'Error updating user info: {e}', 'danger')
        else:
            flash('Invalid password', 'danger')
    elif request.method == "GET":
        form.email.data = current_user.email
        form.address.data = current_user.address
        return render_template('edit_user_info.html', edit_user_form=form, title='Edit User Info')





#  ######################### Therapy Rooms ###############################################
@app.route('/addroom', methods=['POST', 'GET'])
@login_required
def addroom():
    form = AddRoomForm()
    if form.validate_on_submit():
        room = Room(room_name = form.room_name.data, room_number = form.room_number.data)
        db.session.add(room)
        db.session.commit()
        flash(f'Room {form.room_name.data} successfully added', 'success')
        return redirect(url_for('manage'))
    return render_template('addroom.html', form=form)




#  ######################### Client Routes ###############################################


@app.route('/addclient', methods=["POST", "GET"])
@login_required
def addclient():
  form=AddClientForm()
  if form.validate_on_submit():
    client = Client(firstname = form.firstname.data, lastname = form.lastname.data, date_of_birth = form.date_of_birth.data, gender = form.gender.data, phonenumber = form.phonenumber.data, email = form.email.data, address = form.address.data, diagnosis = form.diagnosis.data)
    db.session.add(client)
    db.session.commit()
    flash(f'client {form.email.data} successfully added', 'success')
    return redirect(url_for('clients'))
  else:
      return render_template('addclient.html', form=form, title='AddClient')



@app.route('/scheduleclientsession/<int:client_id>', methods=['GET', 'POST'])
@login_required
def scheduleclientsession(client_id):
  form=ScheduleClientSessionForm()
  client = Client.query.get_or_404(client_id)
  if form.validate_on_submit():
    therapist = client.user_therapist
    clientsession = ClientSession(date = form.date.data, start_time = form.start_time.data, end_time = form.end_time.data, diagnosis = form.diagnosis.data, client_id=client_id, therapist_id = therapist.id)
    db.session.add(clientsession)
    db.session.commit()
    
    flash(f'Client Session successfully added', 'success')
    return redirect(url_for('scheduleclientsession', client_id=client.id))
  else:
      return render_template('scheduleclientsession.html', form=form, title='AddClientSession')



@app.route('/clientprofile/<int:client_id>')
@login_required
def clientprofile(client_id):
  client = Client.query.get_or_404(client_id)
  return render_template('clientprofile.html', client=client)

@app.route('/clientprofile/<int:client_id>/info')
@login_required
def clientprofileinfo(client_id):
    client = Client.query.get_or_404(client_id)
    report = db.session.query(ClientReport).filter_by(client_id=client_id).order_by(ClientReport.id.desc()).first()
    if report:
        report_data = {
            'id': report.id,
            'date': report.date,
            'report_text': json.loads(report.report_text)
        }
    else:
        report_data = None
    return render_template('clientprofileinfo.html', client=client, report=report_data)



@app.route('/assign-client-therapist/<int:client_id>/', methods=['GET', 'POST'])
@login_required
def assign_client_therapist(client_id):
  form = AssignTherapist()
  if form.validate_on_submit():  
    client = Client.query.get_or_404(client_id)
    therapist = User.query.get_or_404(form.therapist.data)
    therapist.clients.append(client)
    db.session.commit()
  return render_template('assign_school_therapist.html', form=form)



@app.route('/addreport/<int:client_id>', methods=['POST', 'GET'])
@login_required
def addreport(client_id):
    form = ReportDynamicForm()
    if form.validate_on_submit():
        client = Client.query.get_or_404(client_id)
        report_text = [
                {
                    report_form.field_name.data : report_form.report_case.data,
                }
                for report_form in form.report_cases.entries
            ]        
        new_report = json.dumps(report_text)
        new_report = ClientReport(report_text=json.dumps(report_text))
        db.session.add(new_report)
        client.reports.append(new_report)
        db.session.commit()
        flash("Report Generated", 'success')
        return redirect(url_for('Home'))
    else:
        flash("Report Not Generated", 'Danger')
    return render_template('addreport.html', form=form)


@app.route('/updatereport/<int:client_id>/<int:report_id>', methods=['POST', 'GET'])
@login_required
def updatereport(client_id, report_id):
    report = ClientReport.query.get_or_404(report_id)
    report_data = json.loads(report.report_text)
    form = ReportDynamicForm()
    if request.method == 'GET':
        for report_case in report_data:
            if report_case:  # Check if report_case is not None
                field_name = next(iter(report_case.keys()))
                report_case_value = next(iter(report_case.values()))
                form.report_cases.append_entry({
                    'field_name': field_name,
                    'report_case': report_case_value
                })
    if form.validate_on_submit():
        report.report_text = json.dumps([
            {
                report_form.field_name.data: report_form.report_case.data,
            }
            for report_form in form.report_cases.entries
        ])
        db.session.commit()
        flash("Report Updated", 'success')
        return redirect(url_for('Home'))
    else:
        flash("Report Not Updated", 'Danger')
    return render_template('updatereport.html', form=form, client_id=client_id, report_id=report_id)


@app.route('/sessionactivity/<int:client_id>/<int:session_id>', methods=['GET', 'POST'])
@login_required
def sessionactivity(client_id, session_id):
    form = SessionForm()
    client = Client.query.get_or_404(client_id)
    session = ClientSession.query.get_or_404(session_id)
    if form.validate_on_submit():
      
        session_data = [
                {
                    'activity_name': activity_form.activity_name.data,
                    'activity_description': activity_form.activity_description.data,
                    'progress': activity_form.progress.data
                }
                for activity_form in form.activities.entries
            ]
        new_activities = json.dumps(session_data)
        sessionactivity = SessionActivity(session_date= form.session_date.data, overview= form.overview.data, goals= form.goals.data, activity_text= new_activities, notes= form.notes.data, recommendations= form.recommendations.data)
        db.session.add(sessionactivity)
        session.activities.append(sessionactivity)
        db.session.commit()
        flash("Activity Generated", 'success')
        return redirect(url_for('sessiondetails', client_id=client.id, session_id=session.id))
    else:
      
      return render_template('sessionactivity.html', form=form)
    

@app.route('/sessiondetails/<int:client_id>/<int:session_id>')
@login_required
def sessiondetails(client_id, session_id):
    client = Client.query.get_or_404(client_id)
    session = ClientSession.query.get_or_404(session_id)
    
    activity = db.session.query(SessionActivity).filter_by(client_session_id=session_id).first()
    if activity:
        activities = json.loads(activity.activity_text) if activity.activity_text else []
        goals = activity.goals.split(", ") if activity.goals else []
        recommendations = activity.recommendations.split(", ") if activity.recommendations else []
    else:
        activities = []
        goals = []
        recommendations = []
        flash("No activity found for this session", 'warning')
    
    return render_template('sessiondetails.html', client_id=client.id, session_id=session.id, activity=activity, activities=activities, goals=goals, recommendations=recommendations)
  
  
#  ######################### Schools Routes ###############################################

@app.route('/addschool', methods=['GET', 'POST'])
@login_required
def addschool():
    form = AddSchoolForm()
    if form.validate_on_submit():

        school =School(school_name = form.school_name.data, school_principal = form.school_principal.data, date_of_registration = form.date_of_registration.data, contact_number = form.contact_number.data, email = form.email.data, address = form.address.data)
        db.session.add(school)
        db.session.commit()
        flash(f'School {form.school_name.data} successfully added', 'success')
        return redirect(url_for('addschool'))
    return render_template('addschool.html', form=form, title='addSchool')


@app.route('/specific-school/<int:school_id>')
@login_required
def specificschool(school_id):
  school = School.query.get_or_404(school_id)
  therapists = User.query.all()
  students = school.students
  return render_template('specific-school.html', school=school, therapists=therapists, students=students)

@app.route('/schoolsessioninfo/<int:school_id>/<int:session_id>')
@login_required
def schoolsessioninfo(school_id, session_id):
    school = School.query.get_or_404(school_id)
    sessions = SchoolSession.query.get_or_404(session_id)
    sessions_report = db.session.query(SchoolSessionReport).filter_by(school_session_id=session_id).first()
    sessions_students = sessions.students_sessions
    return render_template('schoolsessioninfo.html', school=school, schoolsession=sessions, session_report=sessions_report,session_students=sessions_students)


def check_timetable_conflict(school_id, day, start_time, end_time):
    existing_timetables = SchoolTimeTable.query.filter_by(school_id=school_id, day=day).all()
    for timetable in existing_timetables:
        if (start_time >= timetable.start_time and start_time < timetable.end_time) or \
           (end_time > timetable.start_time and end_time <= timetable.end_time):
            return False
    return True

@app.route('/school_timetable/<int:school_id>', methods=['GET', 'POST'])
@login_required
def school_timetable(school_id):
    form = TimeTableForm()
    school = School.query.get_or_404(school_id)
    if form.validate_on_submit():
        if check_timetable_conflict(school_id, form.day.data, form.start_time.data, form.end_time.data):
            timetable = SchoolTimeTable(day=form.day.data, start_time=form.start_time.data, end_time=form.end_time.data, therapist_id=school.school_therapist.id, school_id=school.id)
            db.session.add(timetable)
            school.timetables.append(timetable)
            db.session.commit()
            flash(f'Timetable successfully added', 'success')
        else:
            flash(f'Timetable conflicts with existing timetable', 'danger')
    return render_template('school_timetable.html', form=form, school=school)


@app.route('/school_timetable/<int:school_id>/delete/<int:timetable_id>/', methods=['GET', 'POST'])
@login_required
def delete_school_timetable(timetable_id, school_id):
    school = School.query.get_or_404(school_id)
    school_timetable = SchoolTimeTable.query.get_or_404(timetable_id)
    school.timetables.remove(school_timetable)
    db.session.commit()
    flash(f'Timetable successfully removed', 'success')
    return redirect(url_for("school_timetable", school_id=school.id))



@app.route('/scheduleschoolsession/<int:school_id>', methods=['GET', 'POST'])
@login_required
def scheduleschoolsession(school_id):
  form=ScheduleSchoolSessionForm()
  if form.validate_on_submit():
    school = School.query.get_or_404(school_id)
    therapist = school.school_therapist
    schoolsession = SchoolSession(date = form.date.data, start_time = form.start_time.data, end_time = form.end_time.data,  diagnosis = form.diagnosis.data)
    db.session.add(schoolsession)
    therapist.schoolssessions.append(schoolsession)
    school.sessions.append(schoolsession)
    db.session.commit()
    flash(f'School Session successfully added', 'success')
    return redirect(url_for('specificschool', school_id=school_id))
  else:
      return render_template('scheduleschoolsession.html', form=form, title='AddSchoolSession')



@app.route('/assign-school-therapist/<int:school_id>/', methods=['GET', 'POST'])
@login_required
def assign_school_therapist(school_id):
  form = AssignTherapist()
  if form.validate_on_submit():  # Call the method
    school = School.query.get_or_404(school_id)
    therapist = User.query.get_or_404(form.therapist.data)
    therapist.schools.append(school)
    db.session.commit()
  return render_template('assign_school_therapist.html', form=form)




#  ######################### Student Routes ###############################################
@app.route('/studentprofile/<int:student_id>')
@login_required
def studentprofile(student_id):
  student = SchoolStudent.query.get_or_404(student_id)
  return render_template('studentprofile.html', student=student)


@app.route('/studentprofileinfo/<int:student_id>/info')
@login_required
def studentprofileinfo(student_id):
    student = SchoolStudent.query.get_or_404(student_id)
    report = db.session.query(SchoolStudentReport).filter_by(school_student_id=student_id).order_by(SchoolStudentReport.id.desc()).first()
    report_data = {}
    if report:
        report_data = {
            'id': report.id,
            'date': report.date,
            'report_text': json.loads(report.report_text)
        }
    return render_template('studentprofileinfo.html', student=student, report=report_data)



# Dashboard Routes
@app.route('/addstudent/<int:school_id>/', methods=['GET', 'POST'])
@login_required
def addstudent(school_id):
  form = AddStudentForm()
  if form.validate_on_submit():
    school = School.query.get_or_404(school_id)
    student = SchoolStudent(firstname = form.firstname.data,lastname = form.lastname.data,date_of_birth = form.date_of_birth.data,gender = form.gender.data,phonenumber = form.phonenumber.data,diagnosis = form.diagnosis.data,guardian_name = form.guardian_name.data, email = form.email.data ,address = form.address.data)
    db.session.add(student)
    school.students.append(student)
    db.session.commit()
    flash(f'Student {form.email.data} successfully added', 'success')
    return redirect(url_for('specificschool', school_id=school_id))
  return render_template('addstudent.html', form=form)
    


@app.route('/addreport/<int:student_id>', methods=['POST', 'GET'])
@login_required
def addstudentreport(student_id):
    form = ReportDynamicForm()
    if form.validate_on_submit():
        student = SchoolStudent.query.get_or_404(student_id)
        report_text = [
                {
                    report_form.field_name.data : report_form.report_case.data,
                }
                for report_form in form.report_cases.entries
            ]        
        new_report = json.dumps(report_text)
        new_report = SchoolStudentReport(report_text=json.dumps(report_text))
        db.session.add(new_report)
        student.reports.append(new_report)
        db.session.commit()
        flash("Report Generated", 'success')
        return redirect(url_for('studentprofileinfo'))
      
    return render_template('addreport.html', form=form)


@app.route('/updatestudentreport/<int:student_id>/<int:report_id>', methods=['POST', 'GET'])
@login_required
def updatestudentreport(student_id, report_id):
    report = SchoolStudentReport.query.get_or_404(report_id)
    report_data = json.loads(report.report_text)
    form = ReportDynamicForm()
    if request.method == 'GET':
        for report_case in report_data:
            if report_case:  # Check if report_case is not None
                field_name = next(iter(report_case.keys()))
                report_case_value = next(iter(report_case.values()))
                form.report_cases.append_entry({
                    'field_name': field_name,
                    'report_case': report_case_value
                })
    if form.validate_on_submit():
        report.report_text = json.dumps([
            {
                report_form.field_name.data: report_form.report_case.data,
            }
            for report_form in form.report_cases.entries
        ])
        db.session.commit()
        flash("Report Updated", 'success')
        return redirect(url_for('Home'))

    return render_template('updatestudentreport.html', form=form, student_id=student_id, report_id=report_id)




@app.route('/studentsessionactivity/<int:student_id>/<int:session_id>', methods=['GET', 'POST'])
@login_required
def studentsessionactivity(student_id, session_id):
    form = SessionForm()
    student = SchoolStudent.query.get_or_404(student_id)
    session = SchoolStudentSession.query.get_or_404(session_id)
    if form.validate_on_submit():
        session_data = [
                {
                    'activity_name': activity_form.activity_name.data,
                    'activity_description': activity_form.activity_description.data,
                    'progress': activity_form.progress.data
                }
                for activity_form in form.activities.entries
            ]
        new_activities = json.dumps(session_data)
        sessionactivity = StudentSessionActivity(session_date= form.session_date.data, overview= form.overview.data, goals= form.goals.data, activity_text= new_activities, notes= form.notes.data, recommendations= form.recommendations.data)
        db.session.add(sessionactivity)
        session.activities.append(sessionactivity)
        db.session.commit()
        flash("Activity Generated", 'success')
        return redirect(url_for('studentsessiondetails', student_id=student.id, session_id=session.id))
    else:
      return render_template('sessionactivity.html', form=form)
    

@app.route('/studentsessiondetails/<int:student_id>/<int:session_id>')
@login_required
def studentsessiondetails(student_id, session_id):
    student = SchoolStudent.query.get_or_404(student_id)
    session = SchoolStudentSession.query.get_or_404(session_id)
    
    activity = db.session.query(StudentSessionActivity).filter_by(session_id=session_id).first()
    if activity:
        activities = json.loads(activity.activity_text) if activity.activity_text else []
        goals = activity.goals.split(", ") if activity.goals else []
        recommendations = activity.recommendations.split(", ") if activity.recommendations else []
    else:
        activities = []
        goals = []
        recommendations = []
        flash("No activity found for this session", 'warning')
    
    return render_template('studentsessiondetails.html', student_id=student.id, session_id=session.id, activity=activity, activities=activities, goals=goals, recommendations=recommendations)
  






@app.route('/school_session_report/<int:school_id>/<int:session_id>/', methods=["POST", "GET"])
@login_required
def school_session_report(school_id, session_id):
  form = SchoolSessionReportForm()
  school = School.query.get_or_404(school_id)
  schoolsession = SchoolSession.query.get_or_404(session_id)
  if form.validate_on_submit():
    report = SchoolSessionReport(title = form.title.data, date=form.date.data, session_notes=form.session_notes.data, session_outcome = form.session_outcome.data)
    schoolsession.report.append(report)
    db.session.commit()
    flash(f'school session report success', 'success')
    return redirect(url_for('specificschool'))
  else:
      return render_template('school_session_report.html', form=form, title='school_session_report')


@app.route('/logout')
@login_required
def logout(): 
  logout_user()
  return redirect(url_for('Index'))