from io import BytesIO
from django.shortcuts import render, redirect
import pytz

from home.models import UserDetail
from home.models import UserContacts
from home.models import DoctorsMessage
from home.models import DoctorDetail
from home.models import bookappointment
from home.models import appointmenthistory
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import random
import threading
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


EMAIL_DOES_NOT_EXIST_MSG = "Email does not exist!"
FILL_ALL_DETAILS_MSG = "Fill all the details!"
DENTIST_EMAIL = "dentist.2407best@gmail.com"
INDIA_TIMEZONE = "Asia/Kolkata"

check_login=False
check_doclogin=False
useremail=""
doctoremail=""
uotp=""
ue=""
# --------------------------------Create your views here.-------------------------------------------------------------








# ----------------------------main homepage------------------------------
def homepage(request):
    if check_login==True:
        return redirect('userhp',useremail)
    return render(request,"index.html",{'check':check_login})


# ---------------------------contact page-----------------------------------
def contactus(request):
    
   
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('useremail')
        contact = request.POST.get('usercontact')
        message = request.POST.get('usermessage')
        
        if name == "" or email == "" or contact == "" or message == "":
            messages.warning(request,FILL_ALL_DETAILS_MSG)
            return redirect('contact')
        user_contact = UserContacts(name=name, email=email, contact=contact, message=message,date=datetime.today())
        user_contact.save()
        messages.success(request,"Message sent successfully")
        
        return redirect("contact")

    

    return render(request,"contactus.html",{'check':check_login,'uemail':useremail, 'dcheck':check_doclogin, 'email':doctoremail})


# -----------------------------------about page------------------------------------------
def about(request):
    return render(request,"aboutus.html",{'check':check_login,'uemail':useremail, 'dcheck':check_doclogin,'email':doctoremail})


# ------------------------------------doctor page----------------------------------------
def fordoctor(request):
    if check_login == True:
        return redirect('userhp', useremail)
    
    if request.method != 'POST':
        return render(request, "doctorpage.html", {'check': check_login})
    
    form_type = request.POST.get("form_type")
    
    if form_type == "contactOne":
        return handle_doctor_contact_form(request)
    elif form_type == "loginOne":
        return handle_doctor_login_form(request)
    
    return render(request, "doctorpage.html", {'check': check_login})


def handle_doctor_contact_form(request):
    name = request.POST.get('doctorname')
    email = request.POST.get('doctoremail')
    contact = request.POST.get('doctorcontact')
    message = request.POST.get('doctormessage')
    
    if not validate_contact_form_data(request, name, email, contact, message):
        return redirect('fordoctor')
    
    save_doctor_message(name, email, contact, message)
    messages.success(request, "Message sent successfully")
    return redirect("fordoctor")


def handle_doctor_login_form(request):
    demail = request.POST.get('docemail')
    dpassword = request.POST.get('docpassword')
    
    if not validate_login_form_data(request, demail, dpassword):
        return redirect('fordoctor')
    
    if not DoctorDetail.objects.filter(email=demail).exists():
        messages.warning(request, EMAIL_DOES_NOT_EXIST_MSG)
        return redirect("fordoctor")
    
    doctor = DoctorDetail.objects.get(email=demail)
    
    if doctor.password != dpassword:
        messages.warning(request, "Incorrect password!")
        return redirect("fordoctor")
    
    set_doctor_login_session(demail)
    messages.success(request, "Login successfully")
    return redirect("doctors", demail)


def validate_contact_form_data(request, name, email, contact, message):
    if name == "" or email == "" or contact == "" or message == "":
        messages.warning(request, FILL_ALL_DETAILS_MSG)
        return False
    return True


def validate_login_form_data(request, email, password):
    if email == "" or password == "":
        messages.warning(request, FILL_ALL_DETAILS_MSG)
        return False
    return True


def save_doctor_message(name, email, contact, message):
    user_contact = DoctorsMessage(
        name=name, 
        email=email, 
        contact=contact, 
        message=message,
        date=datetime.today()
    )
    user_contact.save()
    
    
def set_doctor_login_session(email):
    global check_doclogin, doctoremail
    check_doclogin = True
    doctoremail = email



# -----------------------------------login-------------------------------------------
def login(request):
    global check_login
    global useremail
                    
    if check_login==True:
        return redirect('userhp',useremail)
    
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        cyah=request.POST.get('cyah')
        if email == "" or password == "" or cyah == None:
                messages.warning(request,FILL_ALL_DETAILS_MSG)
                return redirect('login')
        if UserDetail.objects.filter(email=email).exists():
            user=UserDetail.objects.get(email=email)
            up=user.password

            if up==password:
                
                check_login=True
                
                useremail=email
                messages.success(request,"You have logged in successfully!")
                
                return redirect("userhp",email)
            else:
                messages.warning(request,"Incorrect password!")
                return redirect("login")
        else:
            messages.warning(request,EMAIL_DOES_NOT_EXIST_MSG)
            return redirect("login")


    return render(request,"login.html")



# ----------------------------------------------Registration---------------------------------------
def registeremail(name, email):
    time.sleep(2)

    send_mail(
    "Welcome to DENTIST World",
    f"Hi {name},\n\nThank you for registering with DENTIST. We look forward to helping you achieve a beautiful, healthy smile.\n\nBest regards,\nThe DENTIST Team",
    DENTIST_EMAIL,
    [email],
    fail_silently=False,
    )
    

def register(request):
    global check_login
    global useremail               
    if check_login==True:
        return redirect('userhp',useremail)
    
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('uemail')
        contact = request.POST.get('ucontact')
        dateofbirth = request.POST.get('udob')
        gender = request.POST.get('ugender')
        address = request.POST.get('uaddress')
        pincode = request.POST.get('upincode')
        password = request.POST.get('newpassword')
        cpassword =request.POST.get('confirmpassword')
        if name == "" or email == "" or contact == "" or dateofbirth == None or gender == None or address == "" or pincode == "" or password == ""or cpassword == "":
                messages.warning(request,FILL_ALL_DETAILS_MSG)
                return redirect('register')
        
        if password==cpassword:
            if UserDetail.objects.filter(email=email).exists():
                messages.warning(request,"Email already exists!")
                return redirect("register")
            elif UserDetail.objects.filter(contact=contact).exists():
                messages.warning(request,"Phone number already exists!")
                return redirect("register")
            else:
                user_detail = UserDetail(name=name, email=email, contact=contact, dateofbirth=dateofbirth, gender=gender, address=address, pincode=pincode, password=password)
                user_detail.save()
                
                check_login=True
                
                useremail=email
                
                # send_mail(
                # "Welcome to DENTIST World",
                # f"Hi {name},\n\nThank you for registering with DENTIST. We look forward to helping you achieve a beautiful, healthy smile.\n\nBest regards,\nThe DENTIST Team",
                # DENTIST_EMAIL,
                # [email],
                # fail_silently=False,
                # )

                
                thread = threading.Thread(target=registeremail, args=(name, email))
                thread.start()
                
                messages.success(request,"Registration successful!")
                return redirect("userhp",email)
        else:
            messages.warning(request,"Password does not match")
            return redirect("register")
   
    return render(request,"registrationpage.html")


    
    
# -------------------------------------------changepassword----------------------------------------------

def otp(request):
    if check_login == True:
        return redirect('userhp', useremail)
    
    global uotp
    global ue
    
    if request.method != 'POST':
        return render(request, 'otp.html')  # Assuming you have an OTP template
    
    form_type = request.POST.get("form_type")
    
    if form_type == "useremail":
        return handle_email_form(request)
    elif form_type == "changepassword":
        return handle_password_change_form(request)
    
    return redirect("otp")


def handle_email_form(request):
    global uotp, ue
    
    uemail = request.POST.get('emailid')
    
    if not UserDetail.objects.filter(email=uemail).exists():
        messages.warning(request, "Email does not exist!")
        return redirect("otp")
    
    udetail = UserDetail.objects.get(email=uemail)
    name = udetail.name
    otp = random.randint(10000, 99999)
    
    uotp = str(otp)
    ue = uemail
    
    send_otp_email(name, uemail, uotp)
    messages.warning(request, "OTP sent to your Email ID successfully")
    
    return render(request, 'otp.html')  # Return to OTP page


def handle_password_change_form(request):
    global uotp, ue
    
    eotp = request.POST.get('enterotp')
    password = request.POST.get('newpassword')
    cpassword = request.POST.get('cnewpassword')
    
    if not validate_password_form_data(request, eotp, password, cpassword):
        return redirect('otp')
    
    if eotp != uotp:
        messages.warning(request, "Enter correct OTP!")
        return redirect("otp")
    
    if password != cpassword:
        messages.warning(request, "Password does not match!")
        return redirect("otp")
    
    # Update password
    udetail = UserDetail.objects.get(email=ue)
    udetail.password = password
    udetail.save()
    
    uotp = ""  # Clear OTP after successful password change
    messages.success(request, "Password changed successfully")
    return redirect("login")


def validate_password_form_data(request, eotp, password, cpassword):
    if eotp == "" or password == "" or cpassword == "":
        messages.warning(request, "Fill all the details !")
        return False
    return True


def send_otp_email(name, email, otp):
    send_mail(
        "Verification for Changing Password",
        f"Hi {name},\n\nYour One-Time Password (OTP) for resetting your password is {otp}. Please do not share this OTP with anyone for security reasons.\n\nThank you,\nThe DENTIST Team",
        "dentist.2407best@gmail.com",
        [email],
        fail_silently=False,
    )


#-------------------------------------------userhp-------------------------------------------
def userhomepage(request,uemailid):
    
    if check_login==False:
        return redirect('home')
    
    return render(request,"userhomepage.html",{'email':uemailid})



# ----------------------------------------appointment page------------------------------------
def appointment(request,uemailid):
    
    if check_login==False:
        return redirect('home')
    doctordetail=DoctorDetail.objects.all().order_by('name')
    

    paginator=Paginator(doctordetail, 5)
    pagenumber=request.GET.get('page')
    doctordetailfinal=paginator.get_page(pagenumber)  
    totalpage=doctordetailfinal.paginator.num_pages
    

    if request.method == 'POST':
        
        
        if request.POST.get("form_type") == "search_location":
            dlocation=request.POST.get('dlocation')
            if dlocation!=None :
                doctordetailfinal=DoctorDetail.objects.filter(city__icontains=dlocation)

        elif request.POST.get("form_type") == "search_doctor":
            dname=request.POST.get('dname')
            if dname!=None :
                doctordetailfinal=DoctorDetail.objects.filter(name__icontains=dname)
                
        elif request.POST.get("form_type") == "email_doctor":
            demail=request.POST.get('doctoremail')
            return redirect('bookappointment',demail)
       

        
    doctorinfo={
        
        'email':uemailid,
        # 'doctordetail':doctordetail,
        'lastpage':totalpage,
        
        'doctordetailfinal':doctordetailfinal,
        'totalpagelist':[n+1 for n in range(totalpage)]
        
        
    }
    return render(request,"appointmentpage.html",doctorinfo)

# ---------------------------------------book appointment----------------------------------------------
def bookappmail(user_name,doctorname,apdate,aptime,clinicname,city,consultationfee,user_email):
    time.sleep(2)  
    
    send_mail(
    "Appointment Confirmation",
    f"Hi {user_name},\n\nYour appointment with {doctorname} has been confirmed for {apdate} at {aptime}. The appointment will take place at {clinicname}, {city}. The consultation fee is ₹{consultationfee}. Please make sure to arrive on time.\n\nThank you,\nThe DENTIST Team",
    DENTIST_EMAIL,
    [user_email],
    fail_silently=False,
    )

def bookuserappointment(request, demailid):
    if check_login == False:
        return redirect('home')
    
    if request.method != 'POST':
        return render(request, "bookappointment.html", {'demail': demailid})
    
    return process_appointment_booking(request, demailid)


def process_appointment_booking(request, demailid):
    appointment_data = get_appointment_data(request, demailid)
    
    if not validate_appointment_fields(request, appointment_data):
        return redirect('bookappointment', appointment_data['doctoremail'])
    
    if not is_valid_appointment_date(request, appointment_data):
        return redirect('bookappointment', appointment_data['doctoremail'])
    
    if has_conflicting_appointments(request, appointment_data):
        return redirect('bookappointment', appointment_data['doctoremail'])
    
    return create_appointment(request, appointment_data)


def get_appointment_data(request, demailid):
    doctordetail = DoctorDetail.objects.get(email=demailid)
    userdetail = UserDetail.objects.get(email=useremail)
    
    return {
        'user_name': userdetail.name,
        'user_email': userdetail.email,
        'doctorname': doctordetail.name,
        'doctoremail': doctordetail.email,
        'clinicname': doctordetail.clinicname,
        'city': doctordetail.city,
        'consultationfee': doctordetail.consultationfee,
        'apdate': request.POST.get('ad'),
        'aptime': request.POST.get('select_time'),
        'payment': request.POST.get('select_payment')
    }
    

def validate_appointment_fields(request, appointment_data):
    if (appointment_data['apdate'] is None or 
        appointment_data['aptime'] is None or 
        appointment_data['payment'] is None):
        messages.success(request, "Select all the fields!")
        return False
    return True
    

def is_valid_appointment_date(request, appointment_data):
    current_date = str(datetime.now(pytz.timezone(INDIA_TIMEZONE)))
    
    if appointment_data['apdate'] <= current_date:
        messages.success(request, "Select valid date!")
        return False
    return True


def has_conflicting_appointments(request, appointment_data):
    # Check if doctor is available at the requested time
    if bookappointment.objects.filter(
        doctoremail=appointment_data['doctoremail'],
        appdate=appointment_data['apdate'],
        apptime=appointment_data['aptime']
    ).exists():
        messages.warning(request, "Please change date or time. Doctor is not available")
        return True

    # Check if user already has an appointment on the same date
    if bookappointment.objects.filter(
        appdate=appointment_data['apdate'],
        useremail=appointment_data['user_email']
    ).exists():
        messages.warning(request, "Please change date. You had already booked an appointment on the selected date.")
        return True
        
    return False
    

def create_appointment(request, appointment_data):
    user_appoint = bookappointment(
        username=appointment_data['user_name'],
        useremail=appointment_data['user_email'],
        doctorname=appointment_data['doctorname'],
        doctoremail=appointment_data['doctoremail'],
        clinicname=appointment_data['clinicname'],
        city=appointment_data['city'],
        appdate=appointment_data['apdate'],
        apptime=appointment_data['aptime'],
        consultationfee=appointment_data['consultationfee'],
        payment=appointment_data['payment']
    )
    user_appoint.save()
    
    send_appointment_confirmation_email(appointment_data)
    messages.success(request, "Appointment booked successfully!")
    return redirect('appointment', useremail)


def send_appointment_confirmation_email(appointment_data):
    thread = threading.Thread(
        target=bookappmail,
        args=(
            appointment_data['user_name'],
            appointment_data['doctorname'],
            appointment_data['apdate'],
            appointment_data['aptime'],
            appointment_data['clinicname'],
            appointment_data['city'],
            appointment_data['consultationfee'],
            appointment_data['user_email']
        )
    )
    thread.start()


# ----------------------------------emergency appointment page----------------------------------------------
def emergencyappointment(request,uemailid):
    
    if check_login==False:
        return redirect('home')
    doctordetail=DoctorDetail.objects.all().order_by('name')
    

    paginator=Paginator(doctordetail, 5)
    pagenumber=request.GET.get('page')
    doctordetailfinal=paginator.get_page(pagenumber)  
    totalpage=doctordetailfinal.paginator.num_pages
    

    if request.method == 'POST':
        
        
        if request.POST.get("form_type") == "search_location":
            dlocation=request.POST.get('dlocation')
            if dlocation!=None :
                doctordetailfinal=DoctorDetail.objects.filter(city__icontains=dlocation)

        elif request.POST.get("form_type") == "search_doctor":
            dname=request.POST.get('dname')
            if dname!=None :
                doctordetailfinal=DoctorDetail.objects.filter(name__icontains=dname)
                
        elif request.POST.get("form_type") == "email_doctor":
            demail=request.POST.get('doctoremail')
            return redirect('bookemergencyappointment',demail)
       

        
    doctorinfo={
        
        'email':uemailid,
        # 'doctordetail':doctordetail,
        'lastpage':totalpage,
        'doctordetailfinal':doctordetailfinal,
        'totalpagelist':[n+1 for n in range(totalpage)]
        
        
    }
    return render(request,"emergencyappointmentpage.html",doctorinfo)

# -------------------------------------book emergency appointment--------------------------------------------------
def bookemergappmail(cuser_name,doctorname,todaysdate,aptime1,t,clinicname,city,consultationfee,cuser_email):
    time.sleep(2)

    send_mail(
    "Appointment Delayed!",
    f"Hi {cuser_name},\n\nWe regret to inform you that your appointment with {doctorname} on {todaysdate} at {aptime1} has been rescheduled due to an emergency. The new appointment time is {t}. The appointment will take place at {clinicname}, {city}. The consultation fee remains ₹{consultationfee}. We apologize for the inconvenience and appreciate your understanding.\n\nThank you,\nThe DENTIST Team",
    DENTIST_EMAIL,
    [cuser_email],
    fail_silently=False,
    )


def bookemergencyappointment(request,demailid):
    if check_login==False:
        return redirect('home')
    
    
    
    date = str(datetime.now(pytz.timezone(INDIA_TIMEZONE)))
  
    
    
    todaysdate=date[0:10]
    currenttime=date[11:16]
    
        
    if request.method == 'POST':
        
        
        doctordetail=DoctorDetail.objects.get(email=demailid)
        userdetail=UserDetail.objects.get(email=useremail)
        
        user_name=userdetail.name
        user_email=userdetail.email
        doctorname=doctordetail.name
        doctoremail=doctordetail.email
        clinicname=doctordetail.clinicname
        city=doctordetail.city
        consultationfee=doctordetail.consultationfee
        consultfee=consultationfee+" + 150"
        aptime1 = request.POST.get('select_time')
        payment = request.POST.get('select_payment')
        
        aptime =""
        if aptime1 == "01:00 Pm":
            aptime = "13:00 Pm"
        elif aptime1 == "02:00 Pm":
            aptime = "14:00 Pm"
        elif aptime1 == "03:00 Pm":
            aptime = "15:00 Pm"
        elif aptime1 == "04:00 Pm":
            aptime = "16:00 Pm"
        elif aptime1 == "05:00 Pm":
            aptime = "17:00 Pm"
        elif aptime1 == "06:00 Pm":
            aptime = "18:00 Pm"

        
        
        if aptime!=None and payment!=None:
            if aptime > currenttime:
                if bookappointment.objects.filter(appdate=todaysdate,useremail=user_email).exists():
                    messages.warning(request,"You cannot take an appointment. You had already booked an appointment on the selected date.")
                    return redirect('bookemergencyappointment',doctoremail)
                if bookappointment.objects.filter(doctoremail=demailid,appdate=todaysdate,apptime=aptime1).exists():
                    appdetail=bookappointment.objects.get(doctoremail=demailid,appdate=todaysdate,apptime=aptime1)
                    cuser_name=appdetail.username
                    cuser_email=appdetail.useremail
                    consultationfee=appdetail.consultationfee
                    t=aptime1[0:2]+":30 "+aptime1[6:8]
                    upayment=appdetail.payment
                    user_appoint = bookappointment(username=cuser_name, useremail=cuser_email, doctorname=doctorname, doctoremail=doctoremail,clinicname=clinicname,city=city, appdate=todaysdate, apptime=t, consultationfee=consultationfee, payment=upayment)
                    user_appoint.save()   
                    appdetail.delete()
                    # send_mail(
                    # "Appointment Delayed!",
                    # f"Hi {cuser_name},\n\nWe regret to inform you that your appointment with {doctorname} on {todaysdate} at {aptime1} has been rescheduled due to an emergency. The new appointment time is {t}. The appointment will take place at {clinicname}, {city}. The consultation fee remains ₹{consultationfee}. We apologize for the inconvenience and appreciate your understanding.\n\nThank you,\nThe DENTIST Team",
                    # DENTIST_EMAIL,
                    # [cuser_email],
                    # fail_silently=False,
                    # )
                    
                    thread = threading.Thread(target=bookemergappmail, args=(cuser_name,doctorname,todaysdate,aptime1,t,clinicname,city,consultationfee,cuser_email))
                    thread.start()
                
                    
                user_appoint = bookappointment(username=user_name, useremail=user_email, doctorname=doctorname, doctoremail=doctoremail,clinicname=clinicname,city=city, appdate=todaysdate, apptime=aptime1, consultationfee=consultfee, payment=payment)
                user_appoint.save()
                # send_mail(
                # "Appointment Confirmation",
                # f"Hi {user_name}, Your appointment is confirmed with Dentist {doctorname} on {todaysdate} at {aptime1}. Address: {clinicname}, {city} and the consultation fees is ₹{consultfee}. Please be on time. Thank you.",
                # DENTIST_EMAIL,
                # [user_email],
                # fail_silently=False,
                # )
                thread = threading.Thread(target=bookappmail, args=(user_name,doctorname,todaysdate,aptime1,clinicname,city,consultfee,user_email))
                thread.start()
                
                messages.success(request,"Appointment booked successfully")
                
                return redirect('userhp',useremail)
            else:
                messages.success(request,"Select valid time!")
            
                return redirect('bookemergencyappointment',doctoremail)
            
        else:
            messages.success(request,"Select all the fields!")
            
            return redirect('bookemergencyappointment',doctoremail)
    return render(request,"bookemergencyappointment.html",{'demail':demailid,'date':todaysdate})



# -----------------------------------user current appointment list----------------------------------------------

def cancelappmail(user_name,doctorname,date,atime,uemailid):
    
    time.sleep(2)
    
    send_mail(
    "Appointment Cancelled",
    f"Hi {user_name},\n\nYour appointment with {doctorname} on {date} at {atime} has been successfully cancelled.\n\nThank you,\nThe DENTIST Team",
    DENTIST_EMAIL,
    [uemailid],
    fail_silently=False,
    )

def appointmentlist(request,uemailid):
    if check_login==False:
        return redirect('home')
    
    cdate=str(datetime.today())
    date = str(datetime.now(pytz.timezone(INDIA_TIMEZONE)))

    todaysdate=date[0:10]
    currenttime=date[11:16]
    
    appdetail=bookappointment.objects.filter(useremail=uemailid).order_by('appdate')
    noappointment=True
    if not appdetail:
        noappointment=False
    
    info={
        'noappointment':noappointment,
        'email':uemailid,
        'appdetail':appdetail,
        'currentdate':cdate
        
    }
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctorname = request.POST.get('doctorname')
        appdetail= bookappointment.objects.get(useremail=uemailid,appdate=date,apptime=time,doctorname=doctorname)
        user_name=appdetail.username
        
        appdetail.delete()
        # send_mail(
        # "Appointment Cancelled",
        # f"Hi {user_name},\n\nYour appointment with {doctorname} on {date} at {atime} has been successfully cancelled.\n\nThank you,\nThe DENTIST Team",
        # DENTIST_EMAIL,
        # [uemailid],
        # fail_silently=False,
        # )
        
        thread = threading.Thread(target=cancelappmail, args=(user_name,doctorname,date,time,uemailid))
        thread.start()
        messages.success(request,"Appointment cancelled successfully!")
        return redirect('applist',uemailid)
    return render(request,"appointmentlist.html",info)


# ---------------------------------------------user history list------------------------------------------------------
def history(request,uemailid):
    if check_login==False:
        return redirect('home')
    userdetail=appointmenthistory.objects.filter(useremail=uemailid)
    noappointment=True
    if not userdetail:
        noappointment=False
    userinfo={
        'noappointment':noappointment,
        'email':uemailid,
        'userdetail':userdetail
    }

    return render(request,"userhistory.html",userinfo)


# -------------------------------------------user detail----------------------------------------------------------
def userdetail(request,uemailid):
    if check_login==False:
        return redirect('home')
    userdetail=UserDetail.objects.get(email=uemailid)
    userinfo={

        'email':uemailid,
        'userdetail':userdetail
    }
    
    return render(request,"userdetail.html",userinfo)


# -----------------------------------------doctor schedule page----------------------------------------------------
def doctorcancelapp(user_name,doctorname,date,atime,user_email):
    time.sleep(2)

    send_mail(
    "Appointment Cancelled",
    f"Hi {user_name},\n\nYour appointment with {doctorname} on {date} at {atime} has been cancelled due to your absence at the scheduled time.\n\nThank you,\nThe DENTIST Team",
    DENTIST_EMAIL,
    [user_email],
    fail_silently=False,
    )

def doctorschedule(request,demail):
    if check_doclogin==False:
        return redirect('home')
    
    
    date = str(datetime.now(pytz.timezone(INDIA_TIMEZONE)))
    todaysdate=date[0:10]
    
    userdetail=bookappointment.objects.filter(doctoremail=demail,appdate=todaysdate).order_by('apptime')
    noappointment=True
    if not userdetail:
        noappointment=False
    userinfo={
        'noappointment':noappointment,
        'email':demail,
        'userdetail':userdetail
    }

    if request.method == 'POST':
        if request.POST.get("form_type") == "email_user":
            date = request.POST.get('date')
            time = request.POST.get('time')
            useremail = request.POST.get('useremail')
            doctorname = request.POST.get('doctorname')
            
            appdetail= bookappointment.objects.get(useremail=useremail,appdate=date,apptime=time,doctorname=doctorname)
            user_name=appdetail.username
            appdetail.delete()
            # send_mail(
            # "Appointment Cancelled",
            # f"Hi {user_name},\n\nYour appointment with {doctorname} on {date} at {atime} has been cancelled due to your absence at the scheduled time.\n\nThank you,\nThe DENTIST Team",
            # DENTIST_EMAIL,
            # [useremail],
            # fail_silently=False,
            # )
            
            thread = threading.Thread(target=doctorcancelapp, args=(user_name,doctorname,date,time,useremail))
            thread.start()      
            messages.success(request,"Appointment cancelled successfully!")
            return redirect('doctors',demail)
        
        elif request.POST.get("form_type") == "prescription":
            uemail=request.POST.get('useremail')
            
            
            return redirect('prescription',uemail)

    
    return render(request,"doctorschedule.html",userinfo)

# ----------------------------------------------------pdf_mail_receipt--------------------------------------------------

def invoice_pdf(doctoremail,useremail):
   
    userdetail=UserDetail.objects.get(email=useremail)
    doctordetail=DoctorDetail.objects.get(email=doctoremail)
    clinic_name = doctordetail.clinicname
    clinic_address = doctordetail.city
    doctor_name = doctordetail.name
    doctor_contact = f"Phone: {doctordetail.contact}"
    patient_name = userdetail.name
    patient_phone = userdetail.contact
    consultation = doctordetail.consultationfee
    date_str = datetime.now().strftime("%Y-%m-%d")
    userprescription = appointmenthistory.objects.filter(useremail=useremail, doctoremail=doctoremail, appdate=date_str).order_by('-appdate', '-apptime').first()

    payment_details = [
        {"description": "Consultation Fee", "amount": consultation},
        
    ]

    payment_mode = userprescription.payment
    total_amount = consultation
    date_str = datetime.now().strftime("%Y-%m-%d")

    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 50, clinic_name)
    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2, height - 80, clinic_address)
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 120, f"Doctor: {doctor_name}")
    p.drawString(50, height - 135, doctor_contact)
    p.drawRightString(width - 50, height - 120, f"Date: {date_str}")
    p.line(50, height - 150, width - 50, height - 150)
    
    
    y_position = height - 170
    p.drawString(50, y_position, f"Patient Name: {patient_name}")
    y_position -= 15
    p.drawString(50, y_position, f"Phone Number: {patient_phone}")
    
    
    y_position -= 30
    p.drawString(50, y_position, "Payment Details:")
    y_position -= 20
    for detail in payment_details:
        description = detail["description"]
        amount = detail['amount']
        p.drawString(50, y_position, description)
        p.drawRightString(width - 50, y_position, amount)
        y_position -= 20
    
    
    p.line(50, y_position, width - 50, y_position)
    y_position -= 20
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y_position, "Total:")
    p.drawRightString(width - 50, y_position, total_amount)
    
    y_position -= 20
    p.setFont("Helvetica", 10)
    p.drawString(50, y_position, f"Payment Mode: {payment_mode}")

    p.showPage()
    p.save()

    pdf_data = buffer.getvalue()
    buffer.close()
   

    return pdf_data



# -----------------------------------------------prescription_pdf------------------------------------------------------



def prescription_pdf(doctoremail,useremail):
    userdetail=UserDetail.objects.get(email=useremail)
    doctordetail=DoctorDetail.objects.get(email=doctoremail)
    clinic_name = doctordetail.clinicname
    clinic_address = doctordetail.city
    doctor_name = doctordetail.name
    doctor_contact = f"Phone: {doctordetail.contact}"
    patient_name = userdetail.name
    patient_phone = userdetail.contact
    date_str = datetime.now().strftime("%Y-%m-%d")
    userprescription = appointmenthistory.objects.filter(useremail=useremail, doctoremail=doctoremail, appdate=date_str).order_by('-appdate', '-apptime').first()
    
    prescription = userprescription.prescription
   

    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

   
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 50, f"{clinic_name} - Prescription")
    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2, height - 80, clinic_address)
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 120, f"Doctor: {doctor_name}")
    p.drawString(50, height - 135, doctor_contact)
    p.drawRightString(width - 50, height - 120, f"Date: {date_str}")
    p.line(50, height - 150, width - 50, height - 150)
    
   
    y_position = height - 170
    p.drawString(50, y_position, f"Patient Name: {patient_name}")
    y_position -= 15
    p.drawString(50, y_position, f"Phone Number: {patient_phone}")
    

    y_position -= 30
    p.drawString(50, y_position, "Prescription Details:")
    
    y_position -= 30  
    paragraph_text = (
       prescription
    )

    
    box_x = 50
    box_y = y_position - 130  
    box_width = width - 100
    box_height = 150  

   
    p.setStrokeColorRGB(0, 0, 0)  
    p.setLineWidth(1)
    p.rect(box_x, box_y, box_width, box_height)

    
    
    text_object = p.beginText()
    text_object.setTextOrigin(box_x + 10, box_y + box_height - 15)
    text_object.setFont("Helvetica", 10)
    
    for line in paragraph_text.split('. '):
        text_object.textLine(line.strip() + ".")
        if text_object.getY() < box_y:
            break
        
    p.drawText(text_object)

    
    p.showPage()
    p.save()

    
    pdf_data = buffer.getvalue()
    buffer.close()
    

   
    return pdf_data










# ---------------------------------------------------prescription---------------------------------------------------------
def send_pdf_email(doctoremail,useremail,patient_name):
   
    time.sleep(2)

    subject = "Invoice and Prescription"
    body = f"Dear {patient_name},\n\nPlease find attached the prescription and invoice for your recent appointment. Thank you for choosing our services.\n\nBest regards,\nThe DENTIST Team"
    from_email = DENTIST_EMAIL
    to_email = [useremail]
    email = EmailMessage(subject, body, from_email, to_email)

    pdf_invoice_data=invoice_pdf(doctoremail,useremail)
    pdf_prescription_data=prescription_pdf(doctoremail,useremail)
    email.attach("invoice.pdf", pdf_invoice_data, "application/pdf")
    email.attach("prescription.pdf", pdf_prescription_data, "application/pdf")
    email.send(fail_silently=False)


def prescription(request,uemail):
    if check_doclogin==False:
        return redirect('home')
    userdetail=UserDetail.objects.get(email=uemail)

    tdate = str(datetime.now(pytz.timezone(INDIA_TIMEZONE)))
    todaysdate=tdate[0:10]
    
    todate=tdate[0:4]
    
    
    dob=userdetail.dateofbirth
    doy=dob[0:4]
    
    age=int(todate) - int(doy)
    userdetail1=appointmenthistory.objects.filter(useremail=uemail)
    noappointment=True
    if not userdetail:
        noappointment=False
    
    userinfo={
        'age':age,
        'email':uemail,
        'userdetail':userdetail,
        'userdetail1':userdetail1,
        'noappointment':noappointment,
    }
    

    if request.method == 'POST':
        prescription=request.POST.get('pres')
        if prescription == "":
            messages.warning(request,"Please write prescription!")
            return redirect('prescription',uemail)
        doctordetail=DoctorDetail.objects.get(email=doctoremail)
        userdetail=UserDetail.objects.get(email=uemail)
        appdetail=bookappointment.objects.get(useremail=uemail,doctoremail=doctoremail,appdate=todaysdate)
        user_name=userdetail.name
        user_email=userdetail.email
        doctorname=doctordetail.name
        docemail=doctordetail.email
        date=appdetail.appdate
        time=appdetail.apptime
        payment=appdetail.payment
        consultationfee=doctordetail.consultationfee

        user_appoint = appointmenthistory(username=user_name, useremail=user_email, doctorname=doctorname, doctoremail=docemail,appdate=date, apptime=time, consultationfee=consultationfee, payment=payment,prescription=prescription)
        user_appoint.save()
        appdetail= bookappointment.objects.get(useremail=user_email,appdate=date,doctorname=doctorname)

        appdetail.delete()
        thread = threading.Thread(target=send_pdf_email, args=(docemail,user_email,user_name))
        thread.start()
        
        messages.success(request,"Appointment completed! ")
        
        return redirect('doctors',docemail)

    return render(request,"prescription.html",userinfo)

# -------------------------------------------logout---------------------------------------------------
def userlogout(request):
    global check_login
    check_login=False
    global check_doclogin
    check_doclogin=False
    messages.success(request,"You have been logged out successfully!")
    
    return redirect("home")





#-----------------------------------------doctorbookappoitmenthistory-----------------------------------------------

def doctorappoitmenthistory(request,demailid):
    if check_doclogin==False:
        return redirect('home')
    

    date = str(datetime.now(pytz.timezone(INDIA_TIMEZONE)))
    todaysdate=date[0:10]
    userdetail=appointmenthistory.objects.filter(doctoremail=demailid, appdate=todaysdate)
    noappointment=True
    if request.method == 'POST':
        
        apdate = request.POST.get('ad')
        userdetail=appointmenthistory.objects.filter(doctoremail=demailid, appdate=apdate)
    

    
    if not userdetail:
        noappointment=False
    userinfo={
        'noappointment':noappointment,
        'email':demailid,
        'userdetail':userdetail,
        'dcheck':check_doclogin
    }


    return render(request,"doctorappointmenthistory.html",userinfo)





