import requests
import telegram
import asyncio


import time

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

import urllib
import os
import requests 



from werkzeug.utils import secure_filename
import os

import requests
from io import BytesIO
from PIL import Image


from datetime import datetime, timedelta
import base64

from telegram import Bot
from telegram import Bot, Update

ACCESS_TOKEN = "6073213402:AAHVmy76yqQvxvgp74KlOQIc5VOMa0ZiDgk"
NGROK_URL = "https://e84e-2407-d000-f-2c1-a9cb-9e5c-7d01-2e65.ngrok-free.app/webhooks/telegram/webhook"

url = f"https://api.telegram.org/bot{ACCESS_TOKEN}/setWebhook"
data = {"url": NGROK_URL}

response = requests.post(url, data=data)
print(response.text)


# # #  create bot object
# # bot = telegram.Bot(token=ACCESS_TOKEN)

# # Set up your bot object
# bot = telegram.Bot(token=ACCESS_TOKEN)

# # Disable webhook
# bot.deleteWebhook()

# # Get latest update
# updates = bot.get_updates()
# latest_update = updates[-1]
# chat_id = latest_update.message.chat_id



# deleting webhook

# bot_token = ACCESS_TOKEN
# telegram_url = 'https://api.telegram.org/bot{}/deleteWebhook'.format(bot_token)

# response = requests.get(telegram_url)

# print(response.json())