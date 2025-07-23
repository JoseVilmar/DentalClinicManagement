from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("",views.homepage,name="home"),
    path("contactus/",views.contactus,name="contact"),
    path("about/",views.about,name="about"),
    path("fordoctor/",views.fordoctor,name="fordoctor"),
    path("login/",views.login,name="login"),
    path("register/",views.register,name="register"),
    path("otp/",views.otp,name="otp"),
    path("userhp/<uemailid>/",views.userhomepage,name="userhp"),
    path("appoitment/<uemailid>/",views.appointment,name="appointment"),
    path("emergencyappoitment/<uemailid>/",views.emergencyappointment,name="emergencyappointment"),
    path("applist/<uemailid>/",views.appointmentlist,name="applist"),
    path("history/<uemailid>/",views.history,name="history"),
    path("userdetail/<uemailid>/",views.userdetail,name="userdetail"),
    path("doctorschedule/<demail>/",views.doctorschedule,name="doctors"),
    path("prescriptionpage/<uemail>/",views.prescription,name="prescription"),
    path("userlogout/",views.userlogout,name="userlogout"),
    path("bookappoitment/<demailid>",views.bookuserappointment,name="bookappointment"),
    path("bookemergencyappoitment/<demailid>",views.bookemergencyappointment,name="bookemergencyappointment"),
    path("doctorappoitmenthistory/<demailid>",views.doctorappoitmenthistory,name="doctorappoitmenthistory"),
    path("feedback/<int:app_id>/", views.salvar_feedback, name="salvar_feedback"),
    path("consulta/<int:app_id>/", views.detalhe_consulta, name="detalhe_consulta"),


]
