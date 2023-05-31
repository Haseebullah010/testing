from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rasa_action.serializers import WhatAppSerializer,SymptomSerializer, CalendarSerializer, Message2WhatAppSerializer, UpdateVisitorSerializer, ImageSerializer
from rasa_action.serializers import FeedbackSerializer, AppointmentSerializer, CheckAppointmentSerializer, GetAppointmentSerializer, GetVisitorSerializer, AddVisitorSerializer
from rasa_action.serializers import ResetOTPSerializer, CheckLoginSerializer
from django.core.cache import cache
from rasa_action.postgres import PostgresDBMSCLS

import datetime
import time
import os.path
from twilio.rest import Client 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rasa_action.mysql import DB
import requests
import base64
import json

db = DB(host='dev-mysql-1.cfkoabf1oytj.ap-southeast-1.rds.amazonaws.com', user='admin', password='UzuS8nvBL!$4wgzu', database='apnamd')

class CalendarView(APIView):

    def post(self, request):
        serializer = CalendarSerializer(data=request.data)
        if serializer.is_valid():
            event_date = serializer.validated_data['event_date']
            doctor_email = serializer.validated_data['doctor_email']
            event_time = serializer.validated_data['event_time']
            event_time = event_time.split("-")
            SCOPES = ['https://www.googleapis.com/auth/calendar']
            creds = None

            token_path = os.path.abspath(os.getcwd())+'\\rasa_action\\token.json'
            credentials_path = os.path.abspath(os.getcwd())+'\\rasa_action\\credentials.json'

            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            try:
                service = build('calendar', 'v3', credentials=creds)

                event = {
                  'summary': 'Hi, you have an appointment with a patient',
                  'description': 'Appointment Date:'+event_date,
                  'start': {
                    'dateTime': event_date+'T00:00:00-'+str(int(event_time[0])-7).zfill(2)+':00'
                  },
                  'end': {
                    'dateTime': event_date+'T00:00:00-'+str(int(event_time[1])-7).zfill(2)+':00'
                  },
                  'attendees': [
                    {'email': doctor_email},
                  ],
                  'reminders': {
                    'useDefault': False,
                    'overrides': [
                      {'method': 'email', 'minutes': 1}
                    ],
                  },
                }

                event = service.events().insert(calendarId='primary', body=event).execute()
                print('Event created: %s' % (event.get('htmlLink')))

            except HttpError as error:
                print('An error occurred: %s' % error)
            
            return JsonResponse({
                'message': 'successful!',
                'htmlLink': event.get('htmlLink')
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class Message2WhatAppView(APIView):

    def post(self, request):
        serializer = Message2WhatAppSerializer(data=request.data)
        if serializer.is_valid():
            to_number = serializer.validated_data['to_number']
            message = serializer.validated_data['message']
            account_sid = 'ACb4107148ef597cdaf80e0fe44211fd2b' 
            auth_token = '6e44a59cff591fdd005fa5ab43e17d46' 
            client = Client(account_sid, auth_token) 

            from_number = "whatsapp:+14155238886"
            if "whatsapp" not in to_number:
                to_number = "whatsapp:"+to_number
            message = client.messages.create(  
                                          body=message,      
                                          from_=from_number,
                                          to=to_number
                                      ) 
            print(message.sid)
            
            return JsonResponse({
                'message': 'successful!',
                'id': message.sid
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class ListDoctorView(APIView):

    def get(self, request):
        listDoctor = db.callStore("get_docters",())
        return JsonResponse({
            'message': 'successful!',
            'data': listDoctor
        }, status=status.HTTP_200_OK)

class AddAppointentView(APIView):

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            selected_date = serializer.validated_data['app_date']
            selected_time = serializer.validated_data['app_time']
            selected_docter_id = serializer.validated_data['doctor_id']
            calendarLink = serializer.validated_data['calendar_link']
            user_id = serializer.validated_data['user_id']
            appointmentObjs = db.callStore("add_appointment",(selected_date,selected_time,selected_docter_id,calendarLink,user_id))
            return JsonResponse({
                'message': 'successful!',
                'id': appointmentObjs[0]["id"]
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)
        
class CheckAppointentView(APIView):

    def get(self, request):
        serializer = CheckAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            selected_date = serializer.validated_data['app_date']
            appointmentObjs = db.callStore("check_appointment",(selected_date,))
            return JsonResponse({
                'message': 'successful!',
                'data': appointmentObjs
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class GetAppointentView(APIView):

    def get(self, request):
        serializer = GetAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            uset_id = serializer.validated_data['user_id']
            appointmentObjs = db.callStore("get_appointment",(uset_id,))
            return JsonResponse({
                'message': 'successful!',
                'data': appointmentObjs
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class AddFeedbackView(APIView):

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            medical_staff = serializer.validated_data['medical_staff']
            nursing_staff = serializer.validated_data['nursing_staff']
            admin_staff = serializer.validated_data['admin_staff']
            comment = serializer.validated_data['comment'] if 'comment' in serializer.validated_data else ""
            appointment_id = serializer.validated_data['appointment_id']
            user_id = serializer.validated_data['user_id']
            feedbackObjs = db.callStore("add_feedback",(medical_staff,nursing_staff,admin_staff,comment,appointment_id,user_id))
            return JsonResponse({
                'message': 'successful!',
                'id': feedbackObjs[0]["id"]
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class AddSymptomView(APIView):

    def post(self, request):
        serializer = SymptomSerializer(data=request.data)
        if serializer.is_valid():
            keys = serializer.validated_data['keys']
            values = serializer.validated_data['values']
            user_id = serializer.validated_data['user_id']
            check_type = serializer.validated_data['check_type']
            keys = keys.split(";")
            values = values.split(";")
            createdtime = time.strftime('%Y-%m-%d %H:%M:%S')
            for i in range(0,len(keys)):
                db.callStore("add_symptom",(keys[i],values[i],createdtime,check_type,user_id))
                        
            return JsonResponse({
                'message': 'successful!'
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class MessageWhatAppView(APIView):

    def post(self, request):
        serializer = WhatAppSerializer(data=request.data)
        if serializer.is_valid():
            to_number = serializer.validated_data['to_number']
            to_number = to_number.replace("+","")
            message = serializer.validated_data['message']            
            #auth_token='EAAQnEEctZCWIBALJTpzrvotOVeWOgz9zILZCk4u35L8jtQzJvYUpfvn10bhVGVaOoABeC8ZBG0QZBRddJw2Pa6AV6sbXjLvv89iOuX7pJyIkXFZAhoUk5TK68YYWQXncmQ4oppXvmGe20L6ClwAHyTvB9fnuxLyt11SXoIXMipsnQFBmHlJKWupHbqrZBzCtj4kOgzyfZAtAwZDZD'
            auth_token='EAALeylZBzdRgBABbtnozxy8TRQr5FxUhtd1SLmvVuRTcQzEGUNwAW5rZBsuhGK74ucHDVBlAAAMVrsUS7He02K9UNzhGoRhg8hqxmkZAnKDcyBHgmHlNKuuiyaZAAg36pxPohvqToY8xrcvw2QTLkEVsKt6pbRk6rPIFLL25sNuHZAdCBdmtC'
            hed = {'Authorization': 'Bearer ' + auth_token}
            data = {"messaging_product": "whatsapp", "to": to_number, "type": "template", "template": { "name": "medibot", "language": { "code": "en_US" },"components": [{
                        "type": "body",
                        "parameters": [
                            {
                            "type": "text",
                            "text": message
                            }
                        ]
                    }] }}
            #url = 'https://graph.facebook.com/v15.0/112821074967407/messages'
            url = 'https://graph.facebook.com/v15.0/101617459447437/messages'
            response = requests.post(url, json=data, headers=hed)
            print(response)
            return JsonResponse({
                'message': 'successful!'
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
class AddVisitorView(APIView):

    def post(self, request):
        serializer = AddVisitorSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            dob = serializer.validated_data['dob']
            user_id = serializer.validated_data['user_id']
            phone = serializer.validated_data['phone']
            gender = serializer.validated_data['gender']
            createdtime = time.strftime('%Y-%m-%d %H:%M:%S')
            visitor = db.callStore("add_visitor",(user_id,email,gender,dob,phone,createdtime))         
            return JsonResponse({
                'message': 'successful!',
                'data': visitor
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class ResetOTPView(APIView):

    def post(self, request):
        serializer = ResetOTPSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            visitor = db.callStore("reset_otp",(user_id,))         
            return JsonResponse({
                'message': 'successful!',
                'data': visitor
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)
        
class GetVisitorView(APIView):

    def post(self, request):
        serializer = GetVisitorSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']  
            visitor = db.callStore("get_visitor",(user_id,))        
            return JsonResponse({
                'message': 'successful!',
                'data': visitor
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class CheckLoginView(APIView):

    def post(self, request):
        serializer = CheckLoginSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']  
            login_date = serializer.validated_data['login_date'] 
            visitor = db.callStore("check_login",(user_id,login_date))        
            return JsonResponse({
                'message': 'successful!',
                'data': visitor
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateVisitorView(APIView):

    def post(self, request):
        serializer = UpdateVisitorSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            visitor = db.callStore("update_visitor",(user_id,))         
            return JsonResponse({
                'message': 'successful!',
                'data': visitor
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)

class UploadImageView(APIView):
    
    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        
        if serializer.is_valid():     
            file = serializer.validated_data['file']
            image_content = base64.b64encode(file.read()).decode('utf-8')
            image_name = file.name
            user_id = serializer.validated_data['user_id']
            check_type = serializer.validated_data['check_type']
            createdtime = time.strftime('%Y-%m-%d %H:%M:%S')
            image = db.callStore("add_image",(user_id,image_name,check_type,image_content,createdtime))
            return JsonResponse({
                'message': 'successful!',
                'image_name': image_name
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            'message': 'Unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)