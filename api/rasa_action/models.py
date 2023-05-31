from django.db import models
from rest_framework import serializers

# Create your models here.

class Calendar(models.Model):
    event_date = models.CharField(max_length=14)
    event_time = models.CharField(max_length=10)
    doctor_email = models.CharField(max_length=255)
       
    def __str__(self):
        return self.event_date
                
    class Meta:
        db_table = 'Calendar'

class Message2WhatApp(models.Model):
    to_number = models.CharField(max_length=50)
    message = models.CharField(max_length=1024)
       
    def __str__(self):
        return self.to_number
                
    class Meta:
        db_table = 'Message2WhatApp'

class Appointment(models.Model):
    app_date = models.CharField(max_length=10)
    app_time = models.CharField(max_length=8)
    doctor_id = models.CharField(max_length=11)
    calendar_link = models.CharField(max_length=1024)
    user_id = models.CharField(max_length=50)  
    def __str__(self):
        return self.doctor_id
                
    class Meta:
        db_table = 'Appointment'

class CheckAppointment(models.Model):
    app_date = models.CharField(max_length=10)
       
    def __str__(self):
        return self.app_date
                
    class Meta:
        db_table = 'CheckAppointment'

class GetAppointment(models.Model):
    user_id = models.CharField(max_length=50)
       
    def __str__(self):
        return self.user_id
                
    class Meta:
        db_table = 'GetAppointment'

class Feedback(models.Model):
    medical_staff = models.CharField(max_length=10)
    nursing_staff = models.CharField(max_length=10)
    admin_staff = models.CharField(max_length=10)
    comment = models.CharField(max_length=4086,default="")
    appointment_id = models.CharField(max_length=11)  
    user_id = models.CharField(max_length=50)  
    def __str__(self):
        return self.appointment_id
                
    class Meta:
        db_table = 'Feedback'

class Symptom(models.Model):
    keys = models.TextField()
    values = models.TextField()
    check_type = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)  
    def __str__(self):
        return self.user_id
                
    class Meta:
        db_table = 'Symptom'

class WhatApp(models.Model):
    auth_token = models.CharField(max_length=220, default="")
    url = models.CharField(max_length=60, default="")
    to_number = models.CharField(max_length=12)
    message = models.CharField(max_length=2048)  
    def __str__(self):
        return self.user_id
                
    class Meta:
        db_table = 'WhatApp'

class Image(models.Model):
    title = models.CharField(max_length=200)
    file = models.ImageField(upload_to="", blank=True, null=True)
    user_id = models.CharField(max_length=50)  
    check_type = models.CharField(max_length=50)  
    def __str__(self):
        return self.title

class Visitor(models.Model):
    email = models.CharField(max_length=255)
    dob = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=7)
    user_id = models.CharField(max_length=50)  
    login_date = models.CharField(max_length=25)
    def __str__(self):
        return self.user_id
                
    class Meta:
        db_table = 'Visitor'