from rest_framework import serializers
from rasa_action.models import Calendar, Message2WhatApp, Appointment, CheckAppointment, GetAppointment,Feedback, Symptom, WhatApp, Visitor, Image
    

class CalendarSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Calendar
        fields = ('event_date','event_time','doctor_email')

class Message2WhatAppSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Message2WhatApp
        fields = ('to_number','message')

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Appointment
        fields = ('app_date','app_time','doctor_id','calendar_link','user_id')

class CheckAppointmentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = CheckAppointment
        fields = ('app_date',)

class GetAppointmentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GetAppointment
        fields = ('user_id',)

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Feedback
        fields = ('medical_staff','nursing_staff','admin_staff','comment','appointment_id','user_id')

class SymptomSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Symptom
        fields = ('keys','values','check_type','user_id')

class WhatAppSerializer(serializers.ModelSerializer):
    class Meta: 
        model = WhatApp
        fields = ('to_number','message')

class AddVisitorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Visitor
        fields = ('user_id','email','gender','dob','phone')

class ResetOTPSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Visitor
        fields = ('user_id',)

class GetVisitorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Visitor
        fields = ('user_id',)

class UpdateVisitorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Visitor
        fields = ('user_id',)

class ImageSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(required=False)
    
    class Meta: 
        model = Image
        fields = ('file','user_id', 'check_type')

class CheckLoginSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Visitor
        fields = ('user_id','login_date')