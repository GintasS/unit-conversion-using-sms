from dotenv import load_dotenv
import os

# Loading of .env variables here.
load_dotenv()

class SmsService:
  SMS_SERVICE_INFOBIP_API_KEY = os.environ['SMS_SERVICE_INFOBIP_API_KEY']
  SMS_GET_INCOMING_SMS_MESSAGES_API_ENDPOINT = "/sms/1/inbox/reports"
  SMS_POST_SEND_SMS_MESSAGE_API_ENDPOINT = "/sms/2/text/advanced"
  SMS_SERVICE_INFOBIP_BASE_URL = "2mkvmw.api.infobip.com"
  SMS_SERVICE_FROM_NUMBER = os.environ['SMS_SERVICE_FROM_NUMBER']