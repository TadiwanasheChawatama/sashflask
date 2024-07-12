from mainapp.models import User, Client, School, SchoolStudent, Room, ClientSession, SchoolSession,ClientReport, SchoolStudentReport, SchoolStudentSession, SessionActivity, StudentSessionActivity,TimeTable, SchoolTimeTable, Contact, HelpArticle, Notifications



    clientsession = ClientSession(date = form.date.data, start_time = form.start_time.data, end_time = form.end_time.data, location = form.location.data, therapist = form.therapist.data, diagnosis = form.diagnosis.data)
    
    
# users sample
user_1 = User(firstname="tadiwa", lastname="chawatama", gender="male", phonenumber="2356543543", email="admin@gmail.com",password="67tgyfn7fn7fbb", address="7750 nuitaujhd", role="admin", contract=3, academic_transcripts="gud sjaguvcds", personal_doc="dfghafghynx")

user_2 = User(firstname="john", lastname="Doe", gender="male", phonenumber="2356598863", email="jd@gmail.com",password="67tgyfn7fn7fbb", address="7750 nuitaujhd", role="therapist", contract=6, academic_transcripts="gud sjaguvcds", personal_doc="dfghafghynx")

user_3 = User(firstname="jane", lastname="smith", gender="female", phonenumber="263465543", email="sj@gmail.com",password="67tgyfn7fn7fbb", address="7750 nuitaujhd", role="admin", contract=9, academic_transcripts="gud sjaguvcds", personal_doc="dfghafghynx")

# clients sample
client_1 = Client(firstname="client1", lastname="one", gender="female", phonenumber="263465543", email="client1@gmail.com", address="7750 nuitaujhd", diagnosis="mental disorder")

client_2 = Client(firstname="client2", lastname="two", gender="male", phonenumber="263465543", email="client2@gmail.com", address="7750 nuitaujhd", diagnosis="mental disorder")

client_3 = Client(firstname="client3", lastname="three", gender="female", phonenumber="263465543", email="client3@gmail.com", address="7750 nuitaujhd", diagnosis="mental disorder")

# school sample
school_1 = School(school_name="school1", school_principal="shumba", contact_number="7858487449", email="school1@gmal.com",address="dcf ctf f gyhv")

school_2 = School(school_name="school2", school_principal="juumba", contact_number="7858487449", email="school2@gmal.com",address="dcf ctf f gyhv")

school_3 = School(school_name="school3", school_principal="zyumba", contact_number="7858487449", email="school3@gmal.com",address="dcf ctf f gyhv")

# students
student_1 = SchoolStudent(firstname="student1", lastname="one", gender="female", phonenumber="263465543", email="std1@gmail.com", address="7750 nuitaujhd", diagnosis="mental disorder")

student_2 = SchoolStudent(firstname="student2", lastname="one", gender="female", phonenumber="263465543", email="std2@gmail.com", address="7750 nuitaujhd", diagnosis="mental disorder")

student_3 = SchoolStudent(firstname="student3", lastname="one", gender="female", phonenumber="263465543", email="std3@gmail.com", address="7750 nuitaujhd", diagnosis="mental disorder")


# rooms
room_1 = Room(room_name="thpyRm1", room_number=1)

room_2 = Room(room_name="thpyRm2", room_number=2)

room_3 = Room(room_name="thpyRm3", room_number=3)

# client session
client_session_1 = ClientSession(diagnosis="hearing imparement")

client_session_2 = ClientSession(diagnosis="talking imparement")

client_session_3 = ClientSession(diagnosis="Learning imparement")


# school session
school_session_1 = SchoolSession("school hearing")

school_session_2 = SchoolSession("school talking")

school_session_3 = SchoolSession("school learning")

# 