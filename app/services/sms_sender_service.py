import http.client
import json
import logging
from collections import namedtuple

from services.convert_unit_service import convert_unit
from configuration.constants import *
from utilities.helper import is_incoming_sms_message_valid

def get_incoming_sms_messages():
  try:
    logging.info("[SMS Service] Fetching incoming SMS messages...")

    conn = http.client.HTTPSConnection(SmsService.SMS_SERVICE_INFOBIP_BASE_URL)
    payload = ''
    headers = {
        'Authorization': SmsService.SMS_SERVICE_INFOBIP_API_KEY,
        'Accept': 'application/json'
    }
    conn.request("GET", SmsService.SMS_GET_INCOMING_SMS_MESSAGES_API_ENDPOINT, payload, headers)
    res = conn.getresponse()
    data = res.read()
    data_decoded = data.decode("utf-8")

    logging.info(f"[SMS Service] Received response from GET 2mkvmw.api.infobip.com/sms/1/inbox/reports: {data_decoded}")
    return data_decoded
  except Exception as ex:
    logging.error(f"[SMS Service] Exception occurred while FETCHING incoming SMS messages: {ex}")
  
def get_detailed_contents_from_incoming_sms(data):
  json_results = json.loads(data)
  
  if "results" not in json_results:
    return []
  
  messages = []
  Message = namedtuple('Message', ['from_number', 'clean_text'])
  
  json_results = json_results["results"]
  for message in json_results:
    from_number = message['from']
    clean_text = message['cleanText']
    messages.append(Message(from_number, clean_text))
  return messages

def send_sms_message(to_phone_number, message):
  try:
    logging.info(f"[SMS Service] Sending SMS to {to_phone_number} with message: {message}")
    conn = http.client.HTTPSConnection(SmsService.SMS_SERVICE_INFOBIP_BASE_URL)

    headers = {
      'Authorization': SmsService.SMS_SERVICE_INFOBIP_API_KEY,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }

    payload = json.dumps({
      "messages": [
        {
            "destinations": [{"to": to_phone_number}],
            "from": SmsService.SMS_SERVICE_FROM_NUMBER,
            "text": message
        }
      ]
    })

    conn.request("POST", SmsService.SMS_POST_SEND_SMS_MESSAGE_API_ENDPOINT, payload, headers)
    res = conn.getresponse()
    data = res.read()
    data_decoded = data.decode('utf-8')

    logging.info(f"[SMS Service] [Sending SMS] Received response from POST 2mkvmw.api.infobip.com/sms/2/text/advanced: {data_decoded}")
  except Exception as ex:
    logging.error(f"[SMS Service] [Sending SMS] Exception occurred while SENDING a SMS messages: {ex}")

def incoming_sms():
  from flask_routes import all_units

  sms_messages_decoded = get_incoming_sms_messages()
  sms_messages_list = get_detailed_contents_from_incoming_sms(sms_messages_decoded)
  for message in sms_messages_list:
    sms_text = message.clean_text
    to_number = message.from_number

    try:
      logging.info(f"[SMS Service] [Incoming SMS] Validating a message from {to_number} with text: {sms_text}")
      is_incoming_sms_message_valid(sms_text)
    except Exception as ex:
      exception_msg = ex
      logging.error(f"[SMS Service] [Incoming SMS] Exception occurred while validating SMS message: {exception_msg}")
      send_sms_message(to_number, str(ex))
      continue

    needles = sms_text.split('/')
    unit_category = needles[0]
    unit_from = needles[1]
    unit_to = needles[2]
    unit_amount = float(needles[3])

    # Convert.
    result = convert_unit(all_units, unit_category, unit_from, unit_to, unit_amount)
    result = '{:,}'.format(result)

    send_sms_message(to_number, f"The result is: {result}")