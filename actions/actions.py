from typing import Any, Text, Dict, List
import requests
import json
import datetime
from datetime import date
from datetime import timedelta
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
import time
import urllib

from rasa_sdk.events import SlotSet,EventType
from pickle import TRUE
from typing import Any, Text, Dict, List
import requests
import json
import datetime
from datetime import date
from datetime import timedelta
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,EventType
from rasa_sdk.events import FollowupAction
from rasa_sdk.forms import FormValidationAction
# from twilio.twiml.messaging_response import MessagingResponse



# from werkzeug.utils import secure_filename
import os

import requests
from io import BytesIO
from PIL import Image

from datetime import datetime, timedelta
import base64

import random
import string

from telegram import Bot
from telegram import Bot, Update

#API_ENDPOINT = "http://localhost:8000/api"
# API_ENDPOINT = "http://172.21.0.5:8001/api"
API_ENDPOINT = "https://api.medibot.com.au/api"

NH_data={}
User_age=0
selected_symptom= []



class ActionLatestMessage_medication(Action):

    def name(self) -> Text:
        return "check_latest_message_MedDetails"

    def run(self, 
    
    dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[EventType]:
            intent= tracker.latest_message['intent'].get('name')
            print ("intent in first j",intent)
            global latest_message
            latest_message = 0
            latest_message = tracker.latest_message.get('text')
            print ("latest_messagen jk in message_doctor",latest_message)

############### Telegram ###############
            user_id = tracker.sender_id
            print(" user id",user_id)

            # get the user's phone number from the message metadata
            # initialize a Telegram bot with the bot token
            bot_token = "6073213402:AAHVmy76yqQvxvgp74KlOQIc5VOMa0ZiDgk"
            bot = Bot(token=bot_token)
            
            # get the user's phone number using the bot object
            Telegram_phone_number = bot.get_chat(user_id).contact.phone_number
            print("Telegram_phone_number", Telegram_phone_number)

            
              

            try:
                twilio_response = MessagingResponse().message(latest_message)
                phone_number = twilio_response.to.phone_number
                print("phone_number",phone_number)
            except:
                phone_number = None
                print("phone_number",phone_number)

            return []

class ActionUserInfoMedication(Action):

    def name(self) -> Text:
        return "med_details_form"

    def run(self, 
    
    dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict) -> List[EventType]:
            
            required_slots=["userdob_med","useremail_med","medCondition_med","medName_med" ,"doctordetails_med"]
            intent= tracker.latest_message['intent'].get('name')
            print ("intent in first med_details_form",intent)
            print("In med_details_form")

            # Get the value of an entity associated with the intent
           
            for slot_name in required_slots: 
                latest_message = tracker.latest_message.get('text')
                print ("latest_message",latest_message)

                if (tracker.slots.get(slot_name)) is None:
                    return[SlotSet("requested_slot", slot_name)]
                else:
                    return [SlotSet("requested_slot",None)]


class Validate_med_details_form(FormValidationAction):
    def name(self) -> Text:
        print("In validate_med_details_form")
        return "validate_med_details_form"


    def validate_diseasename(self, 
    slot_value: Any,
    
    dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict)->Dict[Text, Any]:
            
            # Get the value of an entity associated with the intent
            entity_value = tracker.latest_message.entities[0]['value']
            print ("intent in second",entity_value)
            return []    

class Submitmed_details_form(Action):
    print( "You have entered get event details")
    global uniqueid
    def name(self) ->Text:
        return "action_submit_med_details_form"
    def run(self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker, 
        domain: "DomainDict") -> List[Dict[Text, Any]]:
        print ("here we can call api...")
        intent= tracker.latest_message['intent'].get('name')
        print ("intent in third",intent)
        # discussion_point=tracker.get_slot("discussion_point")
     
        userdob_med=tracker.get_slot("userdob_med")
        useremail_med=tracker.get_slot("useremail_med")
        medCondition_med=tracker.get_slot("medCondition_med")
        medName_med=tracker.get_slot("medName_med")
        doctordetails_med=tracker.get_slot("doctordetails_med")
      
        from_number = tracker.current_state()['sender_id']
        print ("from_number jk",from_number)
        data1={}
        global latest_message
        
        data1["latest_message"]=latest_message
        data1["from_number"]=from_number
        data1["email"]=useremail_med  
        data1["dob"]=userdob_med  
        data1["Suffered_medical_condition"]=medCondition_med  
        data1["Mediaction_name"]=medName_med 
        data1["doctorDetails"]=doctordetails_med  
        
        
        
        # url = "http://13.215.220.190/whatsapp/data/"
        url1 = "https://www.apnamd.in/whatsapp/data/"
  
        # x = requests.post(url, json = data)
        y = requests.post(url1, json = data1)
        # print (x)
        dispatcher.utter_message(text="Thank you for the information. One of our service team members will contact you to discuss further.")
        
        # return [SlotSet("discussion_point",None),SlotSet("user7",None),SlotSet("useremail",None),SlotSet("user5",None),SlotSet("user6",None)]
        return [SlotSet("userdob_med",None),SlotSet("useremail_med",None),SlotSet("medCondition_med",None),SlotSet("medName_med",None),SlotSet("doctordetails_med",None)]   



class ActionaSubmitNHPatients(Action):
  def name(self) -> Text:
    return "action_submit_NH_patients"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    global User_age
    NH_data = {}
    global selected_symptom
    
    has_NH_ask_symptom = tracker.get_slot('has_NH_ask_symptom')
    print("selected symptom value is", has_NH_ask_symptom)
    NH_data["has_NH_ask_symptom"] = tracker.get_slot('has_NH_ask_symptom')
    selected_symptom = has_NH_ask_symptom.split(',')
    print("list of selected symptom is",selected_symptom)
   

    

    # birthday = next(tracker.get_latest_entity_values(entity_type="birthday"), "")
    birthday =tracker.get_slot('birthday')
    gender =tracker.get_slot('gender')
    NH_data["gender"]= tracker.get_slot('gender')
    NH_data["dob"]= tracker.get_slot('birthday')
    # gender = next(tracker.get_latest_entity_values(entity_type="gender"), "")
    print ("has birthday",birthday)
    print ("has gender",gender)
    try:
        x = birthday.split("-")
        
        print ("x",x)
        def ageCalculator(years, months, days,year,month,date):
            
            import datetime
            today = datetime.date(years,months,days)
            dob = datetime.date(year, month, date)
            years= ((today-dob).total_seconds()/ (365.242*24*3600))
            yearsInt=int(years)
            months=(years-yearsInt)*12
            monthsInt=int(months)
            days=(months-monthsInt)*(365.242/12)
            daysInt=int(days)
            print('You are {0} years, {1} months, {2} days old.'.format(yearsInt,monthsInt,daysInt))
            age = str(yearsInt) 
            return age
        b_year = int(x[0])
        b_month = int(x[1])
        b_date = int(x[2])
        now = datetime.datetime.now()
        # get year from date
        c_year = int(now.strftime("%Y"))
        # get month from date
        c_month = int(now.strftime("%m"))
        # get day from date
        c_date =int( now.strftime("%d"))
        age = ageCalculator(c_year,c_month,c_date,b_year,b_month,b_date)
    except Exception as e:
        print ("Error is",e)
        pass
    try :
      birthday = int(age)
    except Exception as e:
      print ("error is",e)
      birthday = 0
    # birthday = next(tracker.get_latest_entity_values(entity_type="birthday"), "")
    User_age=birthday
    print ("age is",birthday)
   
   
    NH_data["duration"] = tracker.get_slot('duration')
    NH_data["has_NH_organ_heart_disease"] = tracker.get_slot('has_NH_organ_heart_disease')
    NH_data["has_NH_organ_stroke"] = tracker.get_slot('has_NH_organ_stroke')
    NH_data["has_NH_organ_dementia"] = tracker.get_slot('has_NH_organ_dementia')
    NH_data["has_NH_organ_kidney_disease"] = tracker.get_slot('has_NH_organ_kidney_disease')
    NH_data["has_NH_organ_poor_mobility"] = tracker.get_slot('has_NH_organ_poor_mobility')
    NH_data["has_NH_organ_depression"] = tracker.get_slot('has_NH_organ_depression')
    NH_data["has_NH_organ_Previous_malignancy"] = tracker.get_slot('has_NH_organ_Previous_malignancy')
  
    NH_data["NH_patients_hospitalize"] = tracker.get_slot('NH_patients_hospitalize')
    NH_data["NH_patients_covid"] = tracker.get_slot('NH_patients_covid')
    NH_data["NH_patients_smoker"] = tracker.get_slot('NH_patients_smoker')
    NH_data["NH_patients_fever"] = tracker.get_slot('NH_patients_fever')
    NH_data["NH_patients_dark_urine"] = tracker.get_slot('NH_patients_dark_urine')
    NH_data["NH_patients_U_incontinence"] = tracker.get_slot('NH_patients_U_incontinence')
    NH_data["NH_patients_appetite"] = tracker.get_slot('NH_patients_appetite')
    NH_data["NH_patients_Cough"] = tracker.get_slot('NH_patients_Cough')
    NH_data["NH_patients_Weight_loss"] = tracker.get_slot('NH_patients_Weight_loss')
    NH_data["NH_patients_gait"] = tracker.get_slot('NH_patients_gait')
    NH_data["NH_patients_speech"] = tracker.get_slot("NH_patients_speech")
    NH_data["NH_patients_food"] = tracker.get_slot("NH_patients_food")
    NH_data["NH_patients_strength"] = tracker.get_slot("NH_patients_strength")
  
    keys = []
    values = []
    for key, value in NH_data.items():
        if value is None:
            continue
        if key in NH_data:
            keys.append(key)
            values.append(value)       
    data = {
        "keys":';'.join([str(elem) for elem in keys]),
        "values":';'.join([str(elem) for elem in values]),
        "check_type":"NH patients", 
        "user_id": tracker.sender_id
    }

    print("Nh dictionary is",NH_data )

    for i in selected_symptom:
      print("i value is",i)
      if i == "Chest Pain":
        print("you have entered in if  condition")
        return [FollowupAction("utter_ask_NH_chestPain_qn_set1")]
    else:
      print("you have entered in else  condition")
      return [FollowupAction("action_submit_NH_patients_data")]

   
class ActionaSubmitNHPatients_data1(Action):
  def name(self) -> Text:
    return "action_submit_NH_patients_data"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    global NH_data 
    global User_age
    global selected_symptom
    print("selected symptom value in second class is", selected_symptom)

    NH_data["gender"]= tracker.get_slot('gender')
    NH_data["dob"]= tracker.get_slot('birthday')
    NH_data["has_NH_ask_symptom"] = tracker.get_slot('has_NH_ask_symptom')
    NH_data["age"] = User_age
    NH_data["duration"] = tracker.get_slot('duration')
    NH_data["has_NH_organ_heart_disease"] = tracker.get_slot('has_NH_organ_heart_disease')
    NH_data["has_NH_organ_stroke"] = tracker.get_slot('has_NH_organ_stroke')
    NH_data["has_NH_organ_dementia"] = tracker.get_slot('has_NH_organ_dementia')
    NH_data["has_NH_organ_kidney_disease"] = tracker.get_slot('has_NH_organ_kidney_disease')
    NH_data["has_NH_organ_poor_mobility"] = tracker.get_slot('has_NH_organ_poor_mobility')
    NH_data["has_NH_organ_depression"] = tracker.get_slot('has_NH_organ_depression')
    NH_data["has_NH_organ_Previous_malignancy"] = tracker.get_slot('has_NH_organ_Previous_malignancy')
  
    NH_data["NH_patients_hospitalize"] = tracker.get_slot('NH_patients_hospitalize')
    NH_data["NH_patients_covid"] = tracker.get_slot('NH_patients_covid')
    NH_data["NH_patients_smoker"] = tracker.get_slot('NH_patients_smoker')
    NH_data["NH_patients_fever"] = tracker.get_slot('NH_patients_fever')
    NH_data["NH_patients_dark_urine"] = tracker.get_slot('NH_patients_dark_urine')
    NH_data["NH_patients_U_incontinence"] = tracker.get_slot('NH_patients_U_incontinence')
    NH_data["NH_patients_appetite"] = tracker.get_slot('NH_patients_appetite')
    NH_data["NH_patients_Cough"] = tracker.get_slot('NH_patients_Cough')
    NH_data["NH_patients_Weight_loss"] = tracker.get_slot('NH_patients_Weight_loss')
    NH_data["NH_patients_gait"] = tracker.get_slot('NH_patients_gait')
    NH_data["NH_patients_speech"] = tracker.get_slot("NH_patients_speech")
    NH_data["NH_patients_food"] = tracker.get_slot("NH_patients_food")
    NH_data["NH_patients_strength"] = tracker.get_slot("NH_patients_strength")
  
    NH_data["NH_patients_blood_test"] = tracker.get_slot('NH_patients_blood_test')
    NH_data["NH_patients_CXR"] = tracker.get_slot('NH_patients_CXR')
    NH_data["NH_patients_aspirin"] = tracker.get_slot('NH_patients_aspirin')
    NH_data["NH_patients_ECG"] = tracker.get_slot('NH_patients_ECG')
    gender= NH_data["gender"]
    dob=NH_data["dob"]
    keys = []
    values = []
    for key, value in NH_data.items():
        if value is None:
            continue
        if key in NH_data:
            keys.append(key)
            values.append(value)       
    data = {
        "keys":';'.join([str(elem) for elem in keys]),
        "values":';'.join([str(elem) for elem in values]),
        "check_type":"NH patients", 
        "user_id": tracker.sender_id
    }

    pdfdata = [
       ["Selected symptom", NH_data["has_NH_ask_symptom"]],
       ["duration of your symptoms", NH_data["duration"]],
       ["Heart Disease", NH_data["has_NH_organ_heart_disease"]],
       ["Strokes", NH_data["has_NH_organ_stroke"]],
       ["Dementia", NH_data["has_NH_organ_dementia"]],
       ["Kidney Disease", NH_data["has_NH_organ_kidney_disease"]],
       ["Poor mobility",NH_data["has_NH_organ_poor_mobility"]],
       ["Depression", NH_data["has_NH_organ_depression"]],
       ["Previous malignancy", NH_data["has_NH_organ_Previous_malignancy"]],
       ["Have you had recent Hospital admission?", NH_data["NH_patients_hospitalize"]],
       ["Have you had recent COVID?", NH_data["NH_patients_covid"]],
       ["Do you smoke?",  NH_data["NH_patients_smoker"]],
       ["Fever", NH_data["NH_patients_fever"]],
       ["Dark urine",NH_data["NH_patients_dark_urine"]],
       ["Urinary incontinence", NH_data["NH_patients_U_incontinence"]],
       ["Reduced appetite", NH_data["NH_patients_appetite"]],
       ["Cough", NH_data["NH_patients_Cough"]],
        
       ["Weight loss", NH_data["NH_patients_Weight_loss"]],
       ["Unsteady gait", NH_data["NH_patients_gait"]],
       ["Slurred speech", NH_data["NH_patients_speech"]],
       ["Chocking on food", NH_data["NH_patients_food"]],
       ["Reduced arm strength",NH_data["NH_patients_strength"]],

       ["Do you have blood test results?", NH_data["NH_patients_blood_test"]],
       ["Do you have CXR?", NH_data["NH_patients_CXR"]],
       ["Is the patient on aspirin?", NH_data["NH_patients_aspirin"]],
       ["Have you taken an ECG?", NH_data["NH_patients_ECG"]]
       
    ]


    

    print("Nh dictionary in second function is is",NH_data )

    url = "http://13.215.220.190/NH/Patients"
    myobj ={
        "uniqueid":"ea5555laa9722",
        "user_id": tracker.sender_id,
        
        "Qn1":NH_data["age"],
        "selected symptom":selected_symptom,
        "Qn2":NH_data["duration"],
        "Qn3a":NH_data["has_NH_organ_heart_disease"],
        "Qn3b":NH_data["has_NH_organ_stroke"],
        "Qn3c":NH_data["has_NH_organ_dementia"],
        "Qn3d":NH_data["has_NH_organ_kidney_disease"],
        "Qn3e":NH_data["has_NH_organ_poor_mobility"],
        "Qn3f":NH_data["has_NH_organ_depression"],
        "Qn3g":NH_data["has_NH_organ_Previous_malignancy"],
        "Qn4":NH_data["NH_patients_hospitalize"],
        "Qn5":NH_data["NH_patients_covid"],
        "Qn6":NH_data["NH_patients_smoker"],
        "Qn7a":NH_data["NH_patients_fever"],
        "Qn7b":NH_data["NH_patients_dark_urine"],
        "Qn7c":NH_data["NH_patients_U_incontinence"],
        "Qn7d":NH_data["NH_patients_appetite"],
        "Qn7e":NH_data["NH_patients_Cough"],
        "Qn7f":NH_data["NH_patients_Weight_loss"],
        "Qn8a":NH_data["NH_patients_gait"],
        "Qn8b":NH_data["NH_patients_speech"],
        "Qn8c":NH_data["NH_patients_food"],
        "Qn8d":NH_data["NH_patients_strength"],
        "Qn10a":NH_data["NH_patients_blood_test"],
        "Qn10b":NH_data["NH_patients_CXR"],
        "Qn10c":NH_data["NH_patients_aspirin"],
        "Qn10d":NH_data["NH_patients_ECG"],
        
      
    }
    x = requests.post(url, json = myobj)
    data = x.json()
    details =  data['status']

    # send message to Telegram bot
    bot_token = '6073213402:AAHVmy76yqQvxvgp74KlOQIc5VOMa0ZiDgk'
    chat_id = '796769115' # you can get this from the bot by sending a message to it
    message = details
 
    data2={}
    data2 = {
        "dob": dob,
        "gender":gender,
        "result":data,
        "module":"NH Patients"
      }
   
   
 
    # construct contact us message with Telegram link
    telegram_bot_username = 'apnamdBot'
    contact_us = 'Contact us to discuss options for investigations and treatment. '

    # message = f"My recent analysis shows ({details}). Please help me understand further options for investigations and treatment."
    # encoded_message = urllib.parse.quote(message)

    
    # contact_us += '<a href="https://t.me/{}?start=start">Message us on Telegram</a>'.format(telegram_bot_username)
    # contact_us += '<a href="https://t.me/{}?start=diagnosis%3A%20{}">Message us on Telegram</a>'.format(telegram_bot_username, urllib.parse.quote(details))
    contact_us += '<a href="https://t.me/{}?start=diagnosis%20{}">Message us on Telegram</a>'.format(telegram_bot_username, urllib.parse.quote(": " + details))

    


    telegram_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(bot_token, chat_id, message)
    response = requests.get(telegram_url)
    print("response is",response.json())

    
    # telegram_url = 'https://api.telegram.org/bot{}/sendMessage'.format(bot_token)
    # payload = {'chat_id': chat_id, 'text': message}
    # response = requests.post(telegram_url, json=payload)
    # print("response is",response.json())

    # # Get the response message from the Telegram bot
    # response_message = response.json()['result']['text']
    # print("msg from telegram to webbot is",response_message)

    try:
        print("You have entered in NH patients try")
        details1 = data['status1']
        payload = {
        'data1': json.dumps(pdfdata),
        'data2': json.dumps(data2),
        "Sender_id":tracker.sender_id
        }
        print("payload is",payload)
        url="http://13.215.220.190/report/generate/"
        x = requests.post(url, json = payload)  
        print (x)
        return [SlotSet("has_NH_ask_symptom", None), SlotSet("current_result", details), SlotSet("current_result1", details1), SlotSet("contact_us_on_whatsapp", contact_us), FollowupAction('action_show_result')]
    
    except Exception as e:
        print("Error in current result2 is", e)
        payload = {
        'data1': json.dumps(pdfdata),
        'data2': json.dumps(data2),
        "Sender_id":tracker.sender_id
    }
        print("payload is",payload)
        url="http://13.215.220.190/report/generate/"
        x = requests.post(url, json = payload)

        return [SlotSet("has_NH_ask_symptom", None), SlotSet("current_result", details), SlotSet("current_result1", None), SlotSet("contact_us_on_whatsapp", contact_us), FollowupAction('action_show_result')]

   
   
 

def ageCal(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

class ActionCheckAbdomen(Action):
     def name(self) -> Text:
         return "action_check_abdomen"

     async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        has_abdomen = next(tracker.get_latest_entity_values(entity_type="has_abdomen"), False)
        return [SlotSet("has_abdomen", has_abdomen)] 
        
class ActionFeedback(Action):
  def name(self) -> Text:
    return "action_feedback"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    data = {
        "user_id": tracker.sender_id
    }
    responses = requests.get(url=API_ENDPOINT+"/getAppointent", data = data) 
    listDate = responses.json()["data"]
    date = []
    for row in listDate:
      tmp = row['app_date'].split("-")
      date.append({"id": row["id"],"datetime": tmp[2]+"/"+tmp[1]+"/"+tmp[0]+" ("+row['app_time']+")"})
    data = []
    data.append({"title": "Medical Staff","entity": 'medical_staff'})
    data.append({"title": "Nursing Staff","entity": 'nursing_staff'})
    data.append({"title": "Administrative Staff","entity": 'admin_staff'})
        
    message={"type": 'feedback',"payload":"/submit_feedback","data":data,"date":date}
    dispatcher.utter_message(text="Please select the scores that best match your experience at the practice:",json_message=message)
    return [] 
        
class ActionAddFeedback(Action):
  def name(self) -> Text:
    return "action_submit_feedback"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
    medical_staff = next(tracker.get_latest_entity_values(entity_type="medical_staff"), "")
    nursing_staff = next(tracker.get_latest_entity_values(entity_type="nursing_staff"), "")
    admin_staff = next(tracker.get_latest_entity_values(entity_type="admin_staff"), "")
    comment = next(tracker.get_latest_entity_values(entity_type="comment"), "")
    appointment_id = next(tracker.get_latest_entity_values(entity_type="appointment_id"), "")
    
    data = {
        "medical_staff":medical_staff,
        "nursing_staff":nursing_staff,
        "admin_staff":admin_staff,
        "comment":comment,
        "appointment_id": appointment_id,
        "user_id": tracker.sender_id
    }
    responses = requests.post(url=API_ENDPOINT+"/addFeedback", data = data)
    dispatcher.utter_message(text="&#x1F44D; Thank you for exploring the features on medibot. Please contact us to discuss deploying the AI chatbot on your website.")
    return []

class ActionCheckLogin(Action):
     def name(self) -> Text:
         return "action_check_login"

     async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        otp_valid = tracker.get_slot('otp_valid')
        if otp_valid:
          return [] 
        data = {
            "user_id": tracker.sender_id
        }
        responses = requests.post(url=API_ENDPOINT+"/getVisitor", data = data)
        visitors = responses.json()["data"]
        visitor = []
        if len(visitors) > 0:
            visitor = visitors[0]
        is_login = False;
        if "id" in visitor:
            print(visitor)
            is_login = True;
            otp = visitor['otp'];
            phone = visitor['phone'];
            gender = visitor['gender'];
            dob = visitor['dob'];
            data = {
                "to_number":phone,
                "message":otp
            }
            requests.post(url=API_ENDPOINT+"/messageWhatApp", data = data)
            return [SlotSet("is_login", is_login),SlotSet("current_otp", otp),SlotSet("gender", gender),SlotSet("birthday", dob)] 
        else:
          return [SlotSet("is_login", False)]
          
class ActionCheckWebLogin(Action):
     def name(self) -> Text:
         return "action_check_web_login"

     async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        login_date = next(tracker.get_latest_entity_values(entity_type="login_date"), "")
        user_id = next(tracker.get_latest_entity_values(entity_type="user_id"), "")
        data = {
            "user_id":user_id,
            "login_date":login_date
        }
        print(data)
        responses = requests.post(url=API_ENDPOINT+"/checkIsLogin", data = data)
        visitors = responses.json()["data"]
        visitor = []
        if len(visitors) > 0:
            visitor = visitors[0]
        is_login = False;
        if "id" in visitor:
            print(visitor)
            is_login = True;
            otp = visitor['otp'];
            phone = visitor['phone'];
            gender = visitor['gender'];
            dob = visitor['dob'];
            return [SlotSet("otp_valid", True),SlotSet("is_login", is_login),SlotSet("current_otp", otp),SlotSet("gender", gender),SlotSet("birthday", dob)] 
        return []

class ActionAddUserInfo(Action):
     def name(self) -> Text:
         return "action_submit_user_info"

     async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = next(tracker.get_latest_entity_values(entity_type="email"), "")
        birthday = next(tracker.get_latest_entity_values(entity_type="birthday"), "")
        phone = next(tracker.get_latest_entity_values(entity_type="phone"), "")
        gender = next(tracker.get_latest_entity_values(entity_type="gender"), "")
        # birthday = birthday.split("-")
        # birthday = birthday[0]+"-"+birthday[1]+"-"+birthday[2]
        data = {
            "user_id": tracker.sender_id,
            "email":"email@jhd.com",
            "phone":phone,
            "gender":"gender",
            "dob": "1220-12-12"
        }
        try:
            url = "http://13.215.220.190/General/basic/details/"
            myobj ={
                "user_id": tracker.sender_id,
                "gender":"gender",
                "DOB":"12-12-",
                "email" : "a@x.com",
                "phone" : phone
            }
            print ("myobj",myobj)
            x = requests.post(url, json = myobj)   
        except Exception as e:
            print ("Error is ",e)
            pass
        responses = requests.post(url=API_ENDPOINT+"/addVisitor", data = data)
        visitors = responses.json()["data"]
        print("visitors are" , visitors)
        visitor = []
        if len(visitors) > 0:
            visitor = visitors[0]
            print("visitor is" , visitor)
        otp = ''
        
        if "id" in visitor:
            otp = visitor['otp']
            gender = visitor['gender']
            dob = visitor['dob']
            data = {
                "to_number":phone,
                "message":otp
            }
            print("when id is in visitor data is" , data)
            requests.post(url=API_ENDPOINT+"/messageWhatApp", data = data)
        return [SlotSet("current_otp", otp),SlotSet("gender", gender),SlotSet("birthday", dob)] 
        
class ActionResetOTP(Action):
     def name(self) -> Text:
         return "action_reset_otp"

     async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data = {
                "user_id": tracker.sender_id
            }
        responses = requests.post(url=API_ENDPOINT+"/resetOTP", data = data)
        visitors = responses.json()["data"]
        visitor = []
        if len(visitors) > 0:
            visitor = visitors[0]
        otp = '';
        if "id" in visitor:
            otp = visitor['otp'];
            data = {
                "to_number":phone,
                "message":otp
            }
            requests.post(url=API_ENDPOINT+"/messageWhatApp", data = data)
        return [SlotSet("current_otp", otp)] 
        
class ActionCheckOTP(Action):
     def name(self) -> Text:
         return "action_check_otp"

     async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_otp = next(tracker.get_latest_entity_values(entity_type="user_otp"), "")
        current_otp = tracker.get_slot('current_otp')
        otp_valid = False
        if str(user_otp) == str(current_otp):
            otp_valid = True
            data = {
                "user_id": tracker.sender_id
            }
            responses = requests.post(url=API_ENDPOINT+"/updateVisitor", data = data)
        return [SlotSet("otp_valid", otp_valid),SlotSet("is_login", otp_valid)] 
        
class ActionSelectDoctor(Action):
    def name(self) -> Text:
      return "action_select_doctor"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
      responses = requests.get(url=API_ENDPOINT+"/listDoctor")
      listDoctor = responses.json()["data"]
      
      buttons = []
      for row in listDoctor:
        buttons.append({"title": "&#x1F449; "+row["doctor_name"],"payload": '/select_date{"selected_docter": "'+str(row["doctor_name"])+'","selected_docter_id": "'+str(row["id"])+'","selected_docter_email": "'+str(row["doctor_email"])+'"}'})
          
      message={"type": 'buttonList',"data":buttons}
      dispatcher.utter_message(text="Select a doctor:",json_message=message)
      return []

class ActionShowTime(Action):
    def name(self) -> Text:
      return "action_show_time"
     
    def listTime(self, listApp, date):
       result = []
       for app in listApp:
          if app['app_date'] == date:
            result.append(app['app_time'].replace(" AM","").replace(" PM",""))
       return result
         
    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      selected_date = next(tracker.get_latest_entity_values(entity_type="selected_date"), "")
      date = selected_date.split("-")
      data = {
        "app_date":date[0] +"-"+date[1]+"-"+date[2],
      }
      responses = requests.get(url=API_ENDPOINT+"/checkAppointent", data = data)
      listApp = responses.json()["data"]
      data= []
      now = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
      for x in range(0, 6):
        now = now + timedelta(days=x)
        listTime = self.listTime(listApp,now.strftime("%Y-%m-%d"))
        data.append({"title":"&#x2795; "+now.strftime("%A"), "items":[{ "title": "07-08 AM "+('(&#x26D4;)' if "07-08" in listTime else ''), "payload": '' if "07-08" in listTime else '/select_time{"selected_time":"07-08 AM","selected_date":"'+now.strftime("%Y-%m-%d")+'"}'}, {"title": "08-09 AM "+('(&#x26D4;)' if "08-09" in listTime else ''), "payload": '' if "08-09" in listTime else '/select_time{"selected_time":"08-09 AM","selected_date":"'+now.strftime("%Y-%m-%d")+'"}'}, {"title": "09-10 AM "+('(&#x26D4;)' if "09-10" in listTime else ''), "payload": '' if "09-10" in listTime else '/select_time{"selected_time":"09-10 AM","selected_date":"'+now.strftime("%Y-%m-%d")+'"}'}, {"title": "10-11 AM "+('(&#x26D4;)' if "10-11" in listTime else ''), "payload": '' if "10-11" in listTime else '/select_time{"selected_time":"10-11 AM","selected_date":"'+now.strftime("%Y-%m-%d")+'"}'}, {"title": "13-14 PM "+('(&#x26D4;)' if "13-14" in listTime else ''), "payload": '' if "13-14" in listTime else '/select_time{"selected_time":"13-14 PM","selected_date":"'+now.strftime("%Y-%m-%d")+'"}'}, {"title": "14-15 PM "+('(&#x26D4;)' if "14-15" in listTime else ''), "payload": '' if "14-15" in listTime else '/select_time{"selected_time":"14-15 PM","selected_date":"'+now.strftime("%Y-%m-%d")+'"}'}, {"title": "15-16 PM "+('(&#x26D4;)' if "15-16" in listTime else ''), "payload": '' if "15-16" in listTime else '/select_time{"selected_time":"15-16 PM","selected_date":"'+now.strftime("%Y-%m-%d")+'"}'}, {"title": "16-17 PM "+('(&#x26D4;)' if "16-17" in listTime else ''), "payload":'' if "16-17" in listTime else '/select_time{"selected_time":"16-17 PM","selected_date":"'+now.strftime("%Y-%m-%d")+'"}'}]})
      message={ "type": "collapsible", "data": data }
      dispatcher.utter_message(text="&#x1F553; Please select appointment time:",json_message=message)
      return [SlotSet("selected_date", selected_date)]
      

class ActionAddAppointment(Action):
     def name(self) -> Text:
         return "action_submit_appointment"

     async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        selected_date = tracker.get_slot('selected_date')
        selected_date_ = selected_date.split("-")
        selected_date = selected_date_[2] +"/"+selected_date_[1]+"/"+selected_date_[0]
        selected_time = next(tracker.get_latest_entity_values(entity_type="selected_time"), "")
        selected_docter = tracker.get_slot('selected_docter')
        selected_docter_id = tracker.get_slot('selected_docter_id')
        selected_docter_email = tracker.get_slot('selected_docter_email')
        data = {
            "event_date":selected_date_[0] +"-"+selected_date_[1]+"-"+selected_date_[2],
            "event_time":selected_time.replace("AM","").replace("PM","").strip(),
            "doctor_email": ("duonghoastg@gmail.com" if selected_docter_email is None else selected_docter_email)
        }
        # responses = requests.post(url=API_ENDPOINT+"/addEvent", data = data)
        # calendarLink = responses.json()["htmlLink"]
        #print(responses.json()["htmlLink"])
        selected_date_ = selected_date_[0] +"-"+selected_date_[1]+"-"+selected_date_[2]
        
        data = {
            "app_date":selected_date_,
            "app_time":selected_time,
            "doctor_id":("0" if selected_docter_id is None else selected_docter_id),
            # "calendar_link":calendarLink,
            "user_id": tracker.sender_id
        }
        # responses = requests.post(url=API_ENDPOINT+"/addAppointent", data = data)        
        message = "Your clinic appointment #selected_docter# is booked for #selected_date# at #selected_time#. Please ensure that you present to the reception desk 15 minutes before the appointment. Thank you!"
        message = message.replace("#selected_date#",selected_date).replace("#selected_time#",selected_time)
        if selected_docter is not None:
            message = message.replace("#selected_docter#"," with "+selected_docter)
        else:
            message = message.replace("#selected_docter#","")
        dispatcher.utter_message(text=message)
        return [SlotSet("selected_date", None),SlotSet("selected_docter", None),SlotSet("selected_docter_id", None),SlotSet("selected_docter_email", None),FollowupAction('utter_check_symptom_again')] 

class ActionAddDepression(Action):
    def name(self) -> Text:
      return "action_submit_depression"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      dataSet = {}
      no_interesting = tracker.get_slot('no_interesting')
      falling_asleep = tracker.get_slot('falling_asleep')
      felt_tired = tracker.get_slot('felt_tired')
      overeating = tracker.get_slot('overeating')
      felt_failure = tracker.get_slot('felt_failure')
      trouble_concentrating = tracker.get_slot('trouble_concentrating')
      spoken_softly = tracker.get_slot('spoken_softly')
      hurting_yourself = tracker.get_slot('hurting_yourself')
      depressed = tracker.get_slot('depressed')
      
      dataSet['no_interesting'] = no_interesting
      dataSet['falling_asleep'] = falling_asleep
      dataSet['felt_tired'] = felt_tired
      dataSet['overeating'] = overeating
      dataSet['trouble_concentrating'] = trouble_concentrating
      dataSet['spoken_softly'] = spoken_softly
      dataSet['hurting_yourself'] = hurting_yourself
      dataSet['depressed'] = depressed
      
      keys = []
      values = []
      for key, value in dataSet.items():
          if value is None:
              continue
          if key in dataSet:
              keys.append(key)
              values.append(value)       
      data = {
          "keys":';'.join([str(elem) for elem in keys]),
          "values":';'.join([str(elem) for elem in values]),
          "check_type":"Depression", 
          "user_id": tracker.sender_id
      }
      responses = requests.post(url=API_ENDPOINT+"/addSymptom", data = data)
      
      url = "http://13.215.220.190/depression/updated/rasa/"
      myobj ={
          "uniqueid":"ea5555laa9722",
          "user_id": tracker.sender_id,
          "1":no_interesting,
          "2":falling_asleep,
          "3":felt_tired,
          "4":overeating,
          "5":felt_failure,
          "6":trouble_concentrating,
          "7":spoken_softly,
          "8":hurting_yourself,
          "9": depressed
          
      }
      x = requests.post(url, json = myobj)
      data = x.json()
      details =  data['status']
      return [SlotSet("current_result", details)]
  
class ActionAddAnxiety(Action):
    def name(self) -> Text:
      return "action_submit_anxiety"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      dataSet = {}
      dataSet['felt_nervous'] = tracker.get_slot('felt_nervous')
      dataSet['worrying'] = tracker.get_slot('worrying')
      dataSet['worried_things'] = tracker.get_slot('worried_things')
      dataSet['trouble_relaxing'] = tracker.get_slot('trouble_relaxing')
      dataSet['felt_restless'] = tracker.get_slot('felt_restless')
      dataSet['felt_annoyed'] = tracker.get_slot('felt_annoyed')
      dataSet['afraid_something'] = tracker.get_slot('afraid_something')
   
      keys = []
      values = []
      for key, value in dataSet.items():
          if value is None:
              continue
          if key in dataSet:
              keys.append(key)
              values.append(value)       
      data = {
          "keys":';'.join([str(elem) for elem in keys]),
          "values":';'.join([str(elem) for elem in values]),
          "check_type":"Anxiety", 
          "user_id": tracker.sender_id
      }
      responses = requests.post(url=API_ENDPOINT+"/addSymptom", data = data)
      
      url = "http://13.215.220.190/anxiety/updated/rasa/"
      myobj ={
          "uniqueid":"ea5555laa9722",
          "user_id": tracker.sender_id,
          "1":dataSet['felt_nervous'],
          "2":dataSet['worrying'],
          "3":dataSet['worried_things'],
          "4":dataSet['trouble_relaxing'],
          "5":dataSet['felt_restless'],
          "6":dataSet['felt_annoyed'],
          "7":dataSet['afraid_something']
      }
      x = requests.post(url, json = myobj)
      data = x.json()
      details =  data['status']
      return [SlotSet("current_result", details)]

class ActionaShowResult(Action):
  def name(self) -> Text:
    return "action_show_result"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    current_result = tracker.get_slot('current_result')
    contact_us_on_whatsapp= tracker.get_slot('contact_us_on_whatsapp')
    dispatcher.utter_message(text=current_result)
    dispatcher.utter_message(text=contact_us_on_whatsapp)
    return [SlotSet("current_result", None), SlotSet("contact_us_on_whatsapp", None)]
    
class ActionaSubmitRespiratory(Action):
  def name(self) -> Text:
    return "action_submit_respiratory"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    dataSet = {}
    dataSet["runny_nose"] = tracker.get_slot('runny_nose')
    dataSet["fever"] = tracker.get_slot('fever')
    dataSet["phlegm"] = tracker.get_slot('phlegm')
    dataSet["breathless"] = tracker.get_slot('breathless')
    dataSet["coughing_blood"] = tracker.get_slot('coughing_blood')
    dataSet["chest_pain"] = tracker.get_slot('chest_pain')
    dataSet["hurt_deep_breath"] = tracker.get_slot('hurt_deep_breath')
    dataSet["hurt_press_chest"] = tracker.get_slot('hurt_press_chest')
    dataSet["lost_weigth"] = tracker.get_slot('lost_weigth')
    dataSet["sound_breath_out"] = tracker.get_slot('sound_breath_out')
    dataSet["legs_swell_up"] = tracker.get_slot('legs_swell_up')
    dataSet["duration"] = tracker.get_slot('duration')
    dataSet["bmi"] = tracker.get_slot('bmi')
    dataSet["chest_smoke"] = tracker.get_slot("chest_smoke")
    dataSet["chest_alcohol"] = tracker.get_slot("chest_alcohol")
    dataSet["chest_recent_covid"] = tracker.get_slot("chest_recent_covid")
    dataSet["chest_diagnose_diabetes"] = tracker.get_slot("chest_diagnose_diabetes")
    dataSet["chest_diagnose_Hypertension"] = tracker.get_slot("chest_diagnose_Hypertension")
    dataSet["chest_diagnose_Asthma"] = tracker.get_slot("chest_diagnose_Asthma")
    dataSet["chest_diagnose_High_Cholesterol"] = tracker.get_slot("chest_diagnose_High_Cholesterol")
    
    keys = []
    values = []
    for key, value in dataSet.items():
        if value is None:
            continue
        if key in dataSet:
            keys.append(key)
            values.append(value)       
    data = {
        "keys":';'.join([str(elem) for elem in keys]),
        "values":';'.join([str(elem) for elem in values]),
        "check_type":"Respiratory", 
        "user_id": tracker.sender_id
    }
    responses = requests.post(url=API_ENDPOINT+"/addSymptom", data = data)
      
    gender = tracker.get_slot('gender')
    dob = tracker.get_slot('birthday')
    age = 30
    if dob is not None:
      tmp = dob.split("-")
      age = ageCal(date(int(tmp[0]), int(tmp[1]), int(tmp[2])))
      
    url = "http://13.215.220.190/updated/Respiratory/"
    myobj ={
        "Medibot_Module": "Respiratory",
        "uniqueid":"ea5555laa9722",
        "user_id": tracker.sender_id,
        "age":age,
        "asthma":dataSet["chest_diagnose_Asthma"],
        "duration":dataSet["duration"],
        "smoke8":dataSet["chest_smoke"],
        "covid10":dataSet["chest_recent_covid"],
        "run53":dataSet["runny_nose"],
        "F54":dataSet["fever"],
        "c55":dataSet["phlegm"],
        "b56":dataSet["breathless"],
        "d57":dataSet["sound_breath_out"],
        "c58":dataSet["coughing_blood"],
        "C59":dataSet["chest_pain"],
        "p59A":dataSet["hurt_deep_breath"],
        "p59B":dataSet["hurt_press_chest"],
        "w60":dataSet["lost_weigth"],
        "s61":dataSet["legs_swell_up"]
    }
    x = requests.post(url, json = myobj)
    data = x.json()
    details =  data['status']

    try:
      print("You have entered in respi try")

      details1 =  data['status1']  
      
      return [SlotSet("hurt_deep_breath",None),SlotSet("hurt_press_chest",None), SlotSet("current_result", details)]
    except Exception as e:
      print("Error in current result2 is",e)
     
      
      return [SlotSet("hurt_deep_breath",None),SlotSet("hurt_press_chest",None), SlotSet("current_result", details), SlotSet("current_result1", None)]



  

class ActionCheckAbdominalPain(Action):
  def name(self) -> Text:
    return "action_check_abdominal_pain"
  
  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    abdominal_pain = next(tracker.get_latest_entity_values(entity_type="abdominal_pain"), False)
    return [SlotSet("abdominal_pain", abdominal_pain)] 

class ActionSubmitFever(Action):
  def name(self) -> Text:
    return "action_submit_fever"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    dataSet = {}
    dataSet["skin_wounds"] = tracker.get_slot('skin_wounds')
    dataSet["headache"] = tracker.get_slot('headache')
    dataSet["drowsy_confused"] = tracker.get_slot('drowsy_confused')
    dataSet["pain_passing_urine"] = tracker.get_slot('pain_passing_urine')
    dataSet["fever_lost_weight"] = tracker.get_slot('fever_lost_weight')
    dataSet["fever_chest_pain"] = tracker.get_slot('fever_chest_pain')
    dataSet["sore_throat"] = tracker.get_slot('sore_throat')
    dataSet["cough_phlegm"] = tracker.get_slot('cough_phlegm')
    dataSet["abdominal_pain"] = tracker.get_slot('abdominal_pain')
    dataSet["bmi"] = tracker.get_slot('bmi')
    dataSet["chest_smoke"] = tracker.get_slot('chest_smoke')
    dataSet["chest_alcohol"] = tracker.get_slot('chest_alcohol')
    dataSet["chest_recent_covid"] = tracker.get_slot('chest_recent_covid')
    dataSet["chest_diagnose_diabetes"] = tracker.get_slot('chest_diagnose_diabetes')
    dataSet["chest_diagnose_Hypertension"] = tracker.get_slot('chest_diagnose_Hypertension')
    dataSet["chest_diagnose_Asthma"] = tracker.get_slot('chest_diagnose_Asthma')
    dataSet["chest_diagnose_High_Cholesterol"] = tracker.get_slot('chest_diagnose_High_Cholesterol')
    dataSet["duration"] = tracker.get_slot("duration")
    dataSet["fever_F3L1"] = tracker.get_slot('fever_F3L1')
    dataSet["fever_F3R1"] = tracker.get_slot('fever_F3R1')
    print ("data set is ",dataSet)
    keys = []
    values = []
    for key, value in dataSet.items():
      if value is None:
        continue
      if key in dataSet:
        keys.append(key)
        values.append(value)
            
    data = {
      "keys":';'.join([str(elem) for elem in keys]),
      "values":';'.join([str(elem) for elem in values]),
      "check_type":"Fever", 
      "user_id": tracker.sender_id
    }
    responses = requests.post(url=API_ENDPOINT+"/addSymptom", data = data)
    
    gender = tracker.get_slot('gender')
    dob = tracker.get_slot('birthday')
    age = 30
    if dob is not None:
      tmp = dob.split("-")
      age = ageCal(date(int(tmp[0]), int(tmp[1]), int(tmp[2])))
        
    url = "http://13.215.220.190/fever/updated/rasa"
    myobj ={
        "uniqueid":"ea5555laa9722",
        "user_id": tracker.sender_id,
        "duration":dataSet["duration"],
        "age":age,
        "smoke8":dataSet["chest_smoke"],
        "covid10":dataSet["chest_recent_covid"],
        "BMI":dataSet["bmi"],
        "f15":dataSet["sore_throat"],
        "f16":dataSet["cough_phlegm"],
        "f17":dataSet["abdominal_pain"],
        "f18":dataSet["skin_wounds"],
        "f19":dataSet["headache"],
        "f20":dataSet["drowsy_confused"],
        "f21":dataSet["pain_passing_urine"],
        "f22":dataSet["fever_lost_weight"],
        "f23":dataSet["fever_chest_pain"],
        "RUQ":dataSet["fever_F3L1"],
        "RLQ":dataSet["fever_F3R1"]
    }
    x = requests.post(url, json = myobj)
    data = x.json()         
    details =  data['status']

    try:
      print("You have entered in fever try")

      details1 =  data['status1']  
     
      return [SlotSet("skin_wounds",None),SlotSet("headache",None),
              SlotSet("drowsy_confused",None),SlotSet("fever_lost_weight", None),
              SlotSet("pain_passing_urine",None),SlotSet("fever_chest_pain", None),
              SlotSet("sore_throat",None),SlotSet("current_result", details),
              SlotSet("bmi",None),SlotSet("chest_recent_covid", None),
              SlotSet("chest_smoke",None),SlotSet("chest_diagnose_diabetes", None),
              SlotSet("chest_alcohol",None),SlotSet("chest_diagnose_Hypertension", None),
              SlotSet("chest_diagnose_Asthma",None),SlotSet("chest_diagnose_High_Cholesterol", None),
              SlotSet("duration",None),SlotSet("fever_F3L1", None),
              SlotSet("fever_F3R1",None),SlotSet("current_result1", None)
              
              
              ]
    except Exception as e:
      print("Error in current result2 is",e)
     
      return [SlotSet("skin_wounds",None),SlotSet("headache",None),
              SlotSet("drowsy_confused",None),SlotSet("fever_lost_weight", None),
              SlotSet("pain_passing_urine",None),SlotSet("fever_chest_pain", None),
              SlotSet("sore_throat",None),SlotSet("current_result", details),
              SlotSet("bmi",None),SlotSet("chest_recent_covid", None),
              SlotSet("chest_smoke",None),SlotSet("chest_diagnose_diabetes", None),
              SlotSet("chest_alcohol",None),SlotSet("chest_diagnose_Hypertension", None),
              SlotSet("chest_diagnose_Asthma",None),SlotSet("chest_diagnose_High_Cholesterol", None),
              SlotSet("duration",None),SlotSet("fever_F3L1", None),
              SlotSet("fever_F3R1",None),SlotSet("current_result1", None)
              
              
              ]



 
class ActionSubmitChest(Action):
  def name(self) -> Text:
    return "action_submit_chestpain"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    chest_data = {}
    chest_right = tracker.get_slot('chest_right')
    chest_data["chest_right"] = chest_right
    chest_center = tracker.get_slot("chest_center")
    chest_data["chest_center"] = chest_center
    chest_left = tracker.get_slot("chest_left")
    chest_data["chest_left"] = chest_left
    chest_blood = tracker.get_slot("chest_blood")
    chest_data["chest_blood"] = chest_blood
    chest_breath = tracker.get_slot("chest_breath")
    chest_data["chest_breath"] = chest_breath
    chest_heart = tracker.get_slot("chest_heart")
    chest_data["chest_heart"] = chest_heart
    chest_hurt = tracker.get_slot("chest_hurt")
    chest_data["chest_hurt"] = chest_hurt
    chest_arm = tracker.get_slot("chest_arm")
    chest_data["chest_arm"] = chest_arm
    chest_runny_nose = tracker.get_slot("chest_runny_nose")
    chest_data["chest_runny_nose"] = chest_runny_nose
    chest_phlegm = tracker.get_slot("chest_phlegm")
    chest_data["phlegm"] = chest_phlegm
    duration = tracker.get_slot("duration")
    chest_data["duration"] = duration
    chest_smoke = tracker.get_slot("chest_smoke")
    chest_data["chest_smoke"] = chest_smoke
    chest_alcohol = tracker.get_slot("chest_alcohol")
    chest_data["chest_alcohol"] = chest_alcohol
    chest_recent_covid = tracker.get_slot("chest_recent_covid")
    chest_data["chest_recent_covid"] = chest_recent_covid
    chest_diagnose_diabetes = tracker.get_slot("chest_diagnose_diabetes")
    chest_data["chest_diagnose_diabetes"] = chest_diagnose_diabetes
    chest_diagnose_Hypertension = tracker.get_slot("chest_diagnose_Hypertension")
    chest_data["chest_diagnose_Hypertension"] = chest_diagnose_Hypertension
    chest_diagnose_Asthma = tracker.get_slot("chest_diagnose_Asthma")
    chest_data["chest_diagnose_Asthma"] = chest_diagnose_Asthma
    chest_diagnose_High_Cholesterol = tracker.get_slot("chest_diagnose_High_Cholesterol")
    chest_data["chest_diagnose_High_Cholesterol"] = chest_diagnose_High_Cholesterol
    
    if chest_right == "true":
        chest_data['7'] = "7B"
    elif chest_center == "true":
        chest_data['7'] = "7A"
    elif chest_left == "true":
        chest_data['7'] = "7C"
    else:
        chest_data["7"]=""
    chest_data['8'] = chest_runny_nose
    chest_data['9'] = chest_phlegm
    chest_data['10'] = chest_blood
    chest_data['11'] = chest_breath
    chest_data['12'] = chest_heart
    chest_data['13'] = chest_hurt
    chest_data['14'] = chest_arm
    print ("chest data is",chest_data)
    keys = []
    values = []
    for key, value in chest_data.items():
        if value is None:
            continue
        if key in chest_data:
            keys.append(key)
            values.append(value)       
    data = {
        "keys":';'.join([str(elem) for elem in keys]),
        "values":';'.join([str(elem) for elem in values]),
        "check_type":"Chestpain", 
        "user_id": tracker.sender_id
    }
    responses = requests.post(url=API_ENDPOINT+"/addSymptom", data = data)
    
    url = "http://13.215.220.190/rasa/chestpain/"
    myobj ={
        "uniqueid":"ea5555laa9722",
        "user_id": tracker.sender_id,
        "duration":duration,
        "7":chest_data["7"],
        "8":chest_data["8"],
        "9":chest_data["9"],
        "10":chest_data["10"],
        "11":chest_data["11"],
        "12":chest_data["12"],
        "13":chest_data["13"],
        "14":chest_data["14"],
        "smoking":chest_smoke,
        "Diabetes":chest_diagnose_diabetes,
        "hyper":chest_diagnose_Hypertension,
        "highchlos":chest_diagnose_High_Cholesterol,
        "bmi":0
    }
    x = requests.post(url, json = myobj)
    data = x.json()
    details =  data['status']

    try:
      print("You have entered in chest try")
      details1 =  data['status1']  
      return [SlotSet("chest_right",None),SlotSet("chest_center",None),SlotSet("chest_left",None), SlotSet("current_result", details)]
    except Exception as e:
      print("Error in current result2 is",e)
     
      return [SlotSet("chest_right",None),SlotSet("chest_center",None),SlotSet("chest_left",None), SlotSet("current_result", details), SlotSet("current_result1", None)]



class ActionSubmitDiabetes(Action):
    def name(self) -> Text:
        return "action_submit_diabetes"

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      dataSet = {}

      dia_family = tracker.get_slot("dia_family")
      dataSet["dia_family"] = dia_family
      dia_glucose = tracker.get_slot("dia_glucose")
      dataSet["dia_glucose"] = dia_glucose
      dia_blood = tracker.get_slot("dia_blood")
      dataSet["dia_blood"] = dia_blood
      dia_smoking = tracker.get_slot("dia_smoking")
      dataSet["dia_smoking"] = dia_smoking
      dia_fruits = tracker.get_slot("dia_fruits")
      dataSet["dia_fruits"] = dia_fruits
      dia_activity = tracker.get_slot("dia_activity")
      dataSet["dia_activity"] = dia_activity
      has_origin = tracker.get_slot("has_origin")
      dataSet["has_origin"] = has_origin
      has_waist = tracker.get_slot("has_waist")
      dataSet["has_waist"] = has_waist
      
      keys = []
      values = []
      for key, value in dataSet.items():
          if value is None:
              continue
          if key in dataSet:
              keys.append(key)
              values.append(value)       
      data = {
          "keys":';'.join([str(elem) for elem in keys]),
          "values":';'.join([str(elem) for elem in values]),
          "check_type":"Diabetes", 
          "user_id": tracker.sender_id
      }
      responses = requests.post(url=API_ENDPOINT+"/addSymptom", data = data)
    
      gender = tracker.get_slot('gender')
      dob = tracker.get_slot('birthday')
      age = 30
      if dob is not None:
        tmp = dob.split("-")
        age = ageCal(date(int(tmp[0]), int(tmp[1]), int(tmp[2])))
      
      url = "http://13.215.220.190/rasa/diabets/"
      myobj ={
          "uniqueid":"ea5555laa9722",
          "user_id": tracker.sender_id,
          "1":int(age),
          "2":gender,
          "3":has_origin,
          "4":dia_family,
          "5":dia_glucose,
          "6":dia_blood,
          "7":dia_smoking,
          "8":dia_fruits,
          "9":dia_activity,
          "10":has_waist
      }
      x = requests.post(url, json = myobj)
      data = x.json()
      details = data['status'][0]['data'] + " " + data['status'][0]['data1']
      return [SlotSet("current_result", details)]

class ActionSubmitCVDRisk(Action):
  def name(self) -> Text:
    return "action_submit_cvd_risk"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    dataSet = {}
    dataSet["cvd_smoker"] = tracker.get_slot('cvd_smoker')
    dataSet["cvd_blood"] = tracker.get_slot('cvd_blood')
    dataSet["cvd_blood_1"] = tracker.get_slot('cvd_blood_1')
    dataSet["cvd_blood_2"] = tracker.get_slot('cvd_blood_2')
    dataSet["cvd_blood_3"] = tracker.get_slot('cvd_blood_3')
    dataSet["cvd_blood_4"] = tracker.get_slot('cvd_blood_4')

    dataSet["cvd_cholestrol"] = tracker.get_slot('cvd_cholestrol')
    dataSet["cvd_cholestrol_1"] = tracker.get_slot('cvd_cholestrol_1')
    dataSet["cvd_cholestrol_2"] = tracker.get_slot('cvd_cholestrol_2')
    dataSet["cvd_cholestrol_3"] = tracker.get_slot('cvd_cholestrol_3')
    dataSet["cvd_cholestrol_4"] = tracker.get_slot('cvd_cholestrol_4')
    dataSet["cvd_cholestrol_5"] = tracker.get_slot('cvd_cholestrol_5')

    dataSet["cvd_hdl"] = tracker.get_slot('cvd_hdl')
    dataSet["cvd_hdl_1"] = tracker.get_slot('cvd_hdl_1')
    dataSet["cvd_hdl_2"] = tracker.get_slot('cvd_hdl_2')
    dataSet["cvd_hdl_3"] = tracker.get_slot('cvd_hdl_3')
    dataSet["cvd_hdl_4"] = tracker.get_slot('cvd_hdl_4')

    
    keys = []
    values = []
    for key, value in dataSet.items():
        if value is None:
            continue
        if key in dataSet:
            keys.append(key)
            values.append(value)       
    data = {
        "keys":';'.join([str(elem) for elem in keys]),
        "values":';'.join([str(elem) for elem in values]),
        "check_type":"CVDRisk", 
        "user_id": tracker.sender_id
    }
    responses = requests.post(url=API_ENDPOINT+"/addSymptom", data = data)
      
    gender = tracker.get_slot('gender')
    dob = tracker.get_slot('birthday')
    age = 30
    if dob is not None:
      tmp = dob.split("-")
      age = ageCal(date(int(tmp[0]), int(tmp[1]), int(tmp[2])))
    
    url = "http://13.215.220.190/rasa/cvd/"
    myobj ={
        "uniqueid":"ea5555laa9722",
        "user_id": tracker.sender_id,
        "age":int(age),
        "gender":gender,
        "smoker":dataSet["cvd_smoker"],
        "cvd_blood_1":dataSet["cvd_blood_1"],
        "cvd_blood_2":dataSet["cvd_blood_2"],
        "cvd_blood_3":dataSet["cvd_blood_3"],
        "cvd_blood_4":dataSet["cvd_blood_4"],
        "cvd_cholestrol_1":dataSet["cvd_cholestrol_1"],
        "cvd_cholestrol_2":dataSet["cvd_cholestrol_2"],
        "cvd_cholestrol_3":dataSet["cvd_cholestrol_3"],
        "cvd_cholestrol_4":dataSet["cvd_cholestrol_4"],
        "cvd_cholestrol_5":dataSet["cvd_cholestrol_5"],
        "cvd_hdl_1":dataSet["cvd_hdl_1"],
        "cvd_hdl_2":dataSet["cvd_hdl_2"],
        "cvd_hdl_3":dataSet["cvd_hdl_3"],
        "cvd_hdl_4":dataSet["cvd_hdl_4"]
    }
    x = requests.post(url, json = myobj)
    data = x.json()
    details =  data['Status']['detail']
                
    return [SlotSet("cvd_hdl_1", None),SlotSet("cvd_hdl_2", None),SlotSet("cvd_hdl_3", None),SlotSet("cvd_hdl_4", None),SlotSet("cvd_blood_1", None),SlotSet("cvd_cholestrol_2", None),SlotSet("cvd_cholestrol_3", None),SlotSet("cvd_cholestrol_4", None),SlotSet("cvd_cholestrol_5", None),SlotSet("cvd_blood_1", None),SlotSet("cvd_blood_2", None),SlotSet("cvd_blood_3", None),SlotSet("cvd_blood_4", None),SlotSet("current_result", details)]


class ActionaSubmitGastroenterology(Action):
  def name(self) -> Text:
    return "action_submit_gastroenterology"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    dataSet = {}
    dataSet["has_abdomen"] = tracker.get_slot('has_abdomen')
    dataSet["fever_F3L1"] = tracker.get_slot('fever_F3L1')
    dataSet["fever_F3L2"] = tracker.get_slot('fever_F3L2')
    dataSet["fever_F3C"] = tracker.get_slot('fever_F3C')
    dataSet["fever_F3R1"] = tracker.get_slot('fever_F3R1')
    dataSet["fever_F3R2"] = tracker.get_slot('fever_F3R2')
    dataSet["pain_fatty_meal"] = tracker.get_slot('pain_fatty_meal')
    dataSet["pain_periods"] = tracker.get_slot('pain_periods')
    dataSet["nausea"] = tracker.get_slot('nausea')
    dataSet["heartburn"] = tracker.get_slot('heartburn')
    dataSet["affect_heartburn"] = tracker.get_slot('affect_heartburn')
    dataSet["worse_lie_down"] = tracker.get_slot('worse_lie_down')
    dataSet["hurt_pass_urine"] = tracker.get_slot('hurt_pass_urine')
    dataSet["blood_stools"] = tracker.get_slot('blood_stools')
    dataSet["heartburn_fewer"] = tracker.get_slot('heartburn_fewer')
    dataSet["jaundice"] = tracker.get_slot('jaundice')
    dataSet["blood_transfusion"] = tracker.get_slot('blood_transfusion')
    dataSet["sexual_partners"] = tracker.get_slot('sexual_partners')
    dataSet["diarrhea"] = tracker.get_slot('diarrhea')
    dataSet["duration_diarrhea"] = tracker.get_slot('duration_diarrhea')
    dataSet["diarrhea_blood_stools"] = tracker.get_slot('diarrhea_blood_stools')
    dataSet["diarrhea_medications"] = tracker.get_slot('diarrhea_medications')
    dataSet["lost_weight"] = tracker.get_slot('lost_weight')
    dataSet["duration"] = tracker.get_slot('duration')
    dataSet["bmi"] = tracker.get_slot('bmi')
    dataSet["chest_smoke"] = tracker.get_slot("chest_smoke")
    dataSet["chest_alcohol"] = tracker.get_slot("chest_alcohol")
    dataSet["chest_recent_covid"] = tracker.get_slot("chest_recent_covid")
    dataSet["chest_diagnose_diabetes"] = tracker.get_slot("chest_diagnose_diabetes")
    dataSet["chest_diagnose_Hypertension"] = tracker.get_slot("chest_diagnose_Hypertension")
    dataSet["chest_diagnose_Asthma"] = tracker.get_slot("chest_diagnose_Asthma")
    dataSet["chest_diagnose_High_Cholesterol"] = tracker.get_slot("chest_diagnose_High_Cholesterol")
    dataSet["gender"] = tracker.get_slot('gender')

    print("dataset",dataSet)
    keys = []
    values = []
    for key, value in dataSet.items():
        if value is None:
            continue
        if key in dataSet:
            keys.append(key)
            values.append(value)       
    data = {
        "keys":';'.join([str(elem) for elem in keys]),
        "values":';'.join([str(elem) for elem in values]),
        "check_type":"Gastroenterology", 
        "user_id": tracker.sender_id
    }
    responses = requests.post(url=API_ENDPOINT+"/addSymptom", data = data)
    
    gender = tracker.get_slot('gender')
    print ("gender value",gender)
    dob = tracker.get_slot('birthday')
    age = 30
    if dob is not None:
      tmp = dob.split("-")
      age = ageCal(date(int(tmp[0]), int(tmp[1]), int(tmp[2])))
      
    url = "http://127.0.0.1:8000/gastro/updated/rasa"
    myobj ={
        "uniqueid":"ea5555laa9722",
        "user_id": tracker.sender_id,
        "gender":gender,
        "age":age,
        "duration":dataSet["duration"],
        "smoke8":dataSet["chest_smoke"],
        "covid10":dataSet["chest_recent_covid"],
        "alcohol9":dataSet["chest_alcohol"],
        "BMI":dataSet["bmi"],
        "abd_45":  dataSet["has_abdomen"],
        "abd_45A": dataSet["fever_F3C"],
        "abd_45RU": dataSet["fever_F3L1"],
        "abd_45LU": dataSet["fever_F3R1"],
        "abd_45RL": dataSet["fever_F3L2"],
        "abd_45LL": dataSet["fever_F3R2"],
        "abd_45B": dataSet["pain_fatty_meal"],
        "abd_45C": dataSet["pain_periods"],
        "abd_45D": dataSet["nausea"],
        "abd_46":  dataSet["heartburn"],
        "abd_46A": dataSet["affect_heartburn"],
        "abd_46B": dataSet["worse_lie_down"],
        "abd_47":  dataSet["hurt_pass_urine"],
        "abd_48":  dataSet["blood_stools"],
        "abd_49":  dataSet["heartburn_fewer"],
        "abd_50":  dataSet["jaundice"],
        "abd_50A": dataSet["blood_transfusion"],
        "abd_50B": dataSet["sexual_partners"],
        "abd_51":  dataSet["diarrhea"],
        "abd_51A": dataSet["duration_diarrhea"],
        "abd_51B": dataSet["diarrhea_blood_stools"],
        "abd_51C": dataSet["diarrhea_medications"],
        "abd_52":  dataSet["lost_weight"]
    }
    x = requests.post(url, json = myobj)
    data = x.json()
    print("json data is", data)
    details =  data['status']  
    # try:
    #   print("You have entered in gastro try")

    details1 =  data['status1']  
    return [SlotSet("blood_transfusion",None),SlotSet("sexual_partners",None),SlotSet("affect_heartburn",None),SlotSet("worse_lie_down",None),SlotSet("duration_diarrhea",None),SlotSet("diarrhea_blood_stools",None),SlotSet("diarrhea_medications",None),SlotSet("has_adomen",None),SlotSet("pain_fatty_meal",None),SlotSet("pain_periods",None),SlotSet("nausea",None),SlotSet("fever_F3C",None),SlotSet("fever_F3L1",None),SlotSet("fever_F3R1",None),SlotSet("fever_F3L2",None),SlotSet("fever_F3R2",None),SlotSet("current_result", details), SlotSet("current_result1", details1)]
    # except Exception as e:
    #   print("Error in current result2 is",e)
    
    #   return [SlotSet("blood_transfusion",None),SlotSet("sexual_partners",None),SlotSet("affect_heartburn",None),SlotSet("worse_lie_down",None),SlotSet("duration_diarrhea",None),SlotSet("diarrhea_blood_stools",None),SlotSet("diarrhea_medications",None),SlotSet("has_adomen",None),SlotSet("pain_fatty_meal",None),SlotSet("pain_periods",None),SlotSet("nausea",None),SlotSet("fever_F3C",None),SlotSet("fever_F3L1",None),SlotSet("fever_F3R1",None),SlotSet("fever_F3L2",None),SlotSet("fever_F3R2",None), SlotSet("current_result", details), SlotSet("current_result1", None)]
    
    

class ActionSubmitBiologicalAge(Action):
  def name(self) -> Text:
    return "action_submit_biological_age"

  async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    dataSet = {}
    dataSet["consume_alcohol"] = tracker.get_slot('consume_alcohol')
    dataSet["drinks_per_week"] = tracker.get_slot('drinks_per_week')
    dataSet["drinks_per_month"] = tracker.get_slot('drinks_per_month')
    dataSet["drink_a_day"] = tracker.get_slot('drink_a_day')
    dataSet["more_drinks_a_day"] = tracker.get_slot('more_drinks_a_day')
    dataSet["No_alcohol"] = tracker.get_slot('No_alcohol')

    dataSet["B_stress"] = tracker.get_slot('B_stress')
    dataSet["walk_to_unwind"] = tracker.get_slot('walk_to_unwind')
    dataSet["Tai_Chi"] = tracker.get_slot('Tai_Chi')
    dataSet["away_or_snack"] = tracker.get_slot('away_or_snack')
    dataSet["keep_on_going"] = tracker.get_slot('keep_on_going')
    dataSet["meditation_5_10_mins"] = tracker.get_slot('meditation_5_10_mins')
    
    dataSet["B_red_meat"] = tracker.get_slot('B_red_meat')
    dataSet["every_day"] = tracker.get_slot('every_day')
    dataSet["taking_time_week"] = tracker.get_slot('taking_time_week')
    dataSet["taking_time_month"] = tracker.get_slot('taking_time_month')
    dataSet["taking_time_never"] = tracker.get_slot('taking_time_never')

    dataSet["B_education_level"] = tracker.get_slot('B_education_level')
    dataSet["high_school"] = tracker.get_slot('high_school')
    dataSet["college"] = tracker.get_slot('college')
    dataSet["university"] = tracker.get_slot('university')
    dataSet["higher_university"] = tracker.get_slot('higher_university')

    dataSet["B_relationship"] = tracker.get_slot('B_relationship')
    dataSet["active_member"] = tracker.get_slot('active_member')
    dataSet["volunteer_regularly"] = tracker.get_slot('volunteer_regularly')
    dataSet["help_out_other"] = tracker.get_slot('help_out_other')
    dataSet["donate_to_charity"] = tracker.get_slot('donate_to_charity')

    dataSet["B_crisis"] = tracker.get_slot('B_crisis')
    dataSet["10_people"] = tracker.get_slot('10_people')
    dataSet["many_friends"] = tracker.get_slot('many_friends')
    dataSet["small_group"] = tracker.get_slot('small_group')
    dataSet["private_person"] = tracker.get_slot('private_person')
    dataSet["crisis_on_my_own"] = tracker.get_slot('crisis_on_my_own')



    dataSet["B_exercise"] = tracker.get_slot('B_exercise')
    dataSet["B_exercise1"] = tracker.get_slot('B_exercise1')
    dataSet["B_exercise2"] = tracker.get_slot('B_exercise2')
    dataSet["B_exercise3"] = tracker.get_slot('B_exercise3')
    dataSet["B_exercise4"] = tracker.get_slot('B_exercise4')

    dataSet["B_smoke"] = tracker.get_slot('B_smoke')
    dataSet["B_smoke1"] = tracker.get_slot('B_smoke1')
    dataSet["B_smoke2"] = tracker.get_slot('B_smoke2')
    dataSet["B_smoke3"] = tracker.get_slot('B_smoke3')
    dataSet["B_smoke4"] = tracker.get_slot('B_smoke4')
    dataSet["B_smoke5"] = tracker.get_slot('B_smoke5')

    dataSet["B_eating_habits"] = tracker.get_slot('B_eating_habits')
    dataSet["eating_habits1"] = tracker.get_slot('eating_habits1')
    dataSet["eating_habits2"] = tracker.get_slot('eating_habits2')
    dataSet["eating_habits3"] = tracker.get_slot('eating_habits3')
    dataSet["eating_habits4"] = tracker.get_slot('eating_habits4')
    dataSet["eating_habits5"] = tracker.get_slot('eating_habits5')


    dataSet["B_coffee_consumption"] = tracker.get_slot('B_coffee_consumption')
    dataSet["coffee_consumption1"] = tracker.get_slot('coffee_consumption1')
    dataSet["coffee_consumption2"] = tracker.get_slot('coffee_consumption2')
    dataSet["coffee_consumption3"] = tracker.get_slot('coffee_consumption3')
    dataSet["coffee_consumption4"] = tracker.get_slot('coffee_consumption4')
    dataSet["coffee_consumption5"] = tracker.get_slot('coffee_consumption5')

    dataSet["B_Sleep_Habbit"] = tracker.get_slot('B_Sleep_Habbit')
    dataSet["Sleep_Habbit1"] = tracker.get_slot('Sleep_Habbit1')
    dataSet["Sleep_Habbit2"] = tracker.get_slot('Sleep_Habbit2')
    dataSet["Sleep_Habbit3"] = tracker.get_slot('Sleep_Habbit3')
    dataSet["Sleep_Habbit4"] = tracker.get_slot('Sleep_Habbit4')


    dataSet["B_lived_beyond_90"] = tracker.get_slot('B_lived_beyond_90')
    dataSet["lived_beyond_90_1"] = tracker.get_slot('lived_beyond_90_1')
    dataSet["lived_beyond_90_2"] = tracker.get_slot('lived_beyond_90_2')
    dataSet["lived_beyond_90_3"] = tracker.get_slot('lived_beyond_90_3')


    
    dataSet["walk_to_unwind"] = tracker.get_slot('walk_to_unwind')
    dataSet["Tai_Chi"] = tracker.get_slot('Tai_Chi')
    dataSet["away_or_snack"] = tracker.get_slot('away_or_snack')
    dataSet["keep_on_going"] = tracker.get_slot('keep_on_going')
    dataSet["meditation_5_10_mins"] = tracker.get_slot('meditation_5_10_mins')

    dataSet["age"] = tracker.get_slot('age')
    
    
    print("your age is", dataSet["age"])
   
    dataSet["bmi"] = tracker.get_slot('bmi')
    
    keys = []
    values = []
    for key, value in dataSet.items():
        if value is None:
            continue
        if key in dataSet:
            keys.append(key)
            values.append(value)       
    data = {
        "keys":';'.join([str(elem) for elem in keys]),
        "values":';'.join([str(elem) for elem in values]),
        "check_type":"BiologicalAge", 
        "user_id": tracker.sender_id
    }
    responses = requests.post(url=API_ENDPOINT+"/addSymptom", data = data)
    
    gender = tracker.get_slot('gender')
    dob = tracker.get_slot('birthday')
    
    if dob is not None:
      tmp = dob.split("-")
      # age = ageCal(date(int(tmp[0]), int(tmp[1]), int(tmp[2])))
       
    url = "http://13.215.220.190/bilogical/updated/rasa/"
    myobj ={
        "uniqueid":"ea5555laa9722",
        "user_id": tracker.sender_id,
        "age":dataSet["age"] ,
        "BMI": dataSet["bmi"],
        "Bio_alchohol1":dataSet["drinks_per_week"],
        "Bio_alchohol2":dataSet["drinks_per_month"],
        "Bio_alchohol3":dataSet["drink_a_day"],
        "Bio_alchohol4":dataSet["more_drinks_a_day"],
        "Bio_stressed1":dataSet["walk_to_unwind"],
        "Bio_stressed2":dataSet["Tai_Chi"],
        "Bio_stressed3":dataSet["away_or_snack"],
        "Bio_stressed4":dataSet["keep_on_going"],
        "Bio_stressed5":dataSet["meditation_5_10_mins"],
        "Bio_red_meat1":dataSet["every_day"],
        "Bio_red_meat2":dataSet["taking_time_week"],
        "Bio_red_meat3":dataSet["taking_time_month"],
        "Bio_red_meat4":dataSet["taking_time_never"],
        "Bio_education1": dataSet["high_school"],
        "Bio_education2": dataSet["college"],
        "Bio_education3": dataSet["university"],
        "Bio_education4": dataSet["higher_university"],
        "Bio_community1": dataSet["active_member"],
        "Bio_community2": dataSet["volunteer_regularly"],
        "Bio_community3": dataSet["help_out_other"],
        "Bio_community4": dataSet["donate_to_charity"],    
        "Bio_crisis1": dataSet["10_people"],
        "Bio_crisis2": dataSet["many_friends"],
        "Bio_crisis3": dataSet["small_group"],
        "Bio_crisis4": dataSet["private_person"],
        "Bio_crisis5": dataSet["crisis_on_my_own"],    
        "Bio_exercise1": dataSet["B_exercise1"],
        "Bio_exercise2": dataSet["B_exercise2"],
        "Bio_exercise3": dataSet["B_exercise3"],
        "Bio_exercise4": dataSet["B_exercise4"],    
        "Bio_smoke1":dataSet["B_smoke1"],
        "Bio_smoke2":dataSet["B_smoke2"],
        "Bio_smoke3":dataSet["B_smoke3"],
        "Bio_smoke4":dataSet["B_smoke4"],
        "Bio_smoke5":dataSet["B_smoke5"],
        "Bio_eating1" : dataSet["eating_habits1"],
        "Bio_eating2" : dataSet["eating_habits2"],
        "Bio_eating3" : dataSet["eating_habits3"],
        "Bio_eating4" : dataSet["eating_habits4"],
        "Bio_eating5" : dataSet["eating_habits5"],
        "Bio_coffee1":dataSet["coffee_consumption1"],
        "Bio_coffee2":dataSet["coffee_consumption2"],
        "Bio_coffee3":dataSet["coffee_consumption3"],
        "Bio_coffee4":dataSet["coffee_consumption4"],
        "Bio_coffee5":dataSet["coffee_consumption5"],   
        "Bio_sleep1":dataSet["Sleep_Habbit1"],
        "Bio_sleep2":dataSet["Sleep_Habbit2"],
        "Bio_sleep3":dataSet["Sleep_Habbit3"],
        "Bio_sleep4":dataSet["Sleep_Habbit4"],  
        "Bio_life1" : dataSet["lived_beyond_90_1"],
        "Bio_life2" : dataSet["lived_beyond_90_2"],
        "Bio_life3" : dataSet["lived_beyond_90_3"]
    }
    x = requests.post(url, json = myobj)
    data = x.json()
    details =  data['status']['context1']
    
    return [SlotSet("lived_beyond_90_1",None),SlotSet("lived_beyond_90_2",None),SlotSet("lived_beyond_90_3",None),SlotSet("Sleep_Habbit1",None),SlotSet("Sleep_Habbit2",None),SlotSet("Sleep_Habbit3",None),SlotSet("Sleep_Habbit4",None),SlotSet("coffee_consumption1",None),SlotSet("coffee_consumption2",None),SlotSet("coffee_consumption3",None),SlotSet("coffee_consumption4",None),SlotSet("coffee_consumption5",None),SlotSet("eating_habits",None),SlotSet("eating_habits2",None),SlotSet("eating_habits3",None),SlotSet("eating_habits4",None),SlotSet("eating_habits5",None),SlotSet("B_smoke1",None),SlotSet("B_smoke2",None),SlotSet("B_smoke3",None),SlotSet("B_smoke4",None),SlotSet("B_smoke5",None),SlotSet("B_exercise1",None),SlotSet("B_exercise2",None),SlotSet("B_exercise3",None),SlotSet("B_exercise4",None),SlotSet("10_people",None),SlotSet("many_friends",None),SlotSet("small_group",None),SlotSet("private_person",None),SlotSet("crisis_on_my_own",None),SlotSet("active_member",None),SlotSet("volunteer_regularly",None),SlotSet("help_out_other",None),SlotSet("donate_to_charity",None),SlotSet("high_school",None),SlotSet("college",None),SlotSet("university",None),SlotSet("higher_university",None),SlotSet("every_day",None),SlotSet("taking_time_week",None),SlotSet("taking_time_month",None),SlotSet("taking_time_never",None),SlotSet("walk_to_unwind",None),SlotSet("Tai_Chi",None),SlotSet("away_or_snack",None),SlotSet("keep_on_going",None),SlotSet("meditation_5_10_mins",None),SlotSet("No_alcohol",None),SlotSet("more_drinks_a_day",None),SlotSet("drink_a_day",None),SlotSet("drinks_per_month",None),SlotSet("drinks_per_week",None),SlotSet("current_result", str(details))]

       