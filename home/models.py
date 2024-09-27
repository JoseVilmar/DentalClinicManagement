
from django.db import models

# Create your models here.


#for patient user models

# registration model
class UserDetail(models.Model):
    name=models.CharField(max_length=200 )
    email=models.EmailField(max_length=200,primary_key=True)
    contact=models.CharField(max_length=12, unique=True,null=False)
    dateofbirth=models.CharField(max_length=200,null=False)
    gender=models.CharField( max_length=50,null=False)
    address=models.TextField(null=False)
    pincode=models.CharField(max_length=10,null=False)
    password=models.CharField(max_length=100,null=False)



# for user contact
class UserContacts(models.Model):
    name=models.CharField(max_length=200 )
    email=models.EmailField(max_length=200)
    contact=models.CharField(max_length=12)
    message=models.TextField(null=False)
    date=models.DateField()


# for doctor contact
class DoctorsMessage(models.Model):
    name=models.CharField(max_length=200 )
    email=models.EmailField(max_length=200)
    contact=models.CharField(max_length=12)
    message=models.TextField(null=False)
    date=models.DateField()



# doctor detail
class DoctorDetail(models.Model):
    name=models.CharField(max_length=200 )
    email=models.EmailField(max_length=200,primary_key=True)
    contact=models.CharField(max_length=12, unique=True,null=False)
    experience=models.CharField(max_length=100)
    clinicname=models.TextField(null=False)
    city=models.CharField(max_length=200)
    consultationfee=models.CharField(max_length=10)
    password=models.CharField(max_length=100,null=False)

# book appointment
class bookappointment(models.Model):
    username=models.CharField(max_length=200 )
    useremail=models.EmailField(max_length=200)
    
    doctorname=models.CharField(max_length=200 )
    doctoremail=models.EmailField(max_length=200)
    clinicname=models.TextField(null=False)
    city=models.CharField(max_length=200)
    appdate=models.CharField(max_length=200)
    apptime=models.CharField(max_length=100)
    consultationfee=models.CharField(max_length=10)
    payment=models.CharField(max_length=100)


#  appointment history
class appointmenthistory(models.Model):
    username=models.CharField(max_length=200 )
    useremail=models.EmailField(max_length=200)
    
    doctorname=models.CharField(max_length=200 )
    doctoremail=models.EmailField(max_length=200)
    
    appdate=models.CharField(max_length=200)
    apptime=models.CharField(max_length=100)
    consultationfee=models.CharField(max_length=10)
    payment=models.CharField(max_length=100)
    prescription=models.TextField(max_length=1000)
    
