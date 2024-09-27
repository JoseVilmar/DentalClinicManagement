from django.contrib import admin
from home.models import UserDetail
from home.models import UserContacts, appointmenthistory
from home.models import DoctorsMessage, DoctorDetail, bookappointment
# Register your models here.
# user detail
class userdetailadmin(admin.ModelAdmin):
    list_display=('name', 'email', 'contact','gender')
admin.site.register(UserDetail,userdetailadmin)


# for user contact
class usercontactadmin(admin.ModelAdmin):
    list_display=('name', 'email', 'contact','message','date')
admin.site.register(UserContacts,usercontactadmin)

# for doctor contact
class doctorscontactadmin(admin.ModelAdmin):
    list_display=('name', 'email', 'contact','message','date')
admin.site.register(DoctorsMessage,doctorscontactadmin)


# for doctor detail
class doctordetailadmin(admin.ModelAdmin):
    list_display=('name', 'email', 'contact','experience','clinicname','city','consultationfee')
admin.site.register(DoctorDetail,doctordetailadmin)

# for appointment detail
class appointmentadmin(admin.ModelAdmin):
    list_display=('username', 'useremail', 'doctorname','doctoremail','appdate','apptime','consultationfee','payment')
admin.site.register(bookappointment,appointmentadmin)


# for appointment history
class appointmenthistoryadmin(admin.ModelAdmin):
    list_display=('username', 'useremail', 'doctorname','doctoremail','appdate','apptime','consultationfee','payment','prescription')
admin.site.register(appointmenthistory,appointmenthistoryadmin)