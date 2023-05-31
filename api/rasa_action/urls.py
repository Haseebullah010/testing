from django.urls import path

from . import views
from .views import CalendarView, Message2WhatAppView, ListDoctorView, AddAppointentView, CheckAppointentView, UploadImageView, CheckLoginView
from .views import GetAppointentView, AddFeedbackView, AddSymptomView, MessageWhatAppView, AddVisitorView, GetVisitorView, UpdateVisitorView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('addEvent', CalendarView.as_view(), name="addEvent"),
    path('message2whatapp', Message2WhatAppView.as_view(), name="message2whatapp"),
    path('listDoctor', ListDoctorView.as_view(), name="listDoctor"),
    path('addAppointent', AddAppointentView.as_view(), name="addAppointent"),
    path('checkAppointent', CheckAppointentView.as_view(), name="checkAppointent"),
    path('getAppointent', GetAppointentView.as_view(), name="getAppointent"),
    path('addFeedback', AddFeedbackView.as_view(), name="addFeedback"),
    path('addSymptom', AddSymptomView.as_view(), name="addSymptom"),
    path('messageWhatApp', MessageWhatAppView.as_view(), name="messageWhatApp"),
    path('addVisitor', AddVisitorView.as_view(), name="addVisitor"),
    path('getVisitor', GetVisitorView.as_view(), name="getVisitor"),
    path('updateVisitor', UpdateVisitorView.as_view(), name="updateVisitor"),
    path('uploadImage', UploadImageView.as_view(), name="uploadImage"),
    path('checkIsLogin', CheckLoginView.as_view(), name="checkIsLogin"),
]
