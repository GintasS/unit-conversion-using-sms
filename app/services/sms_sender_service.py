from flask import render_template, request
from app import flask_app

@flask_app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
  
  # Get the message the user sent our Twilio number.
  body = request.values.get('Body', None)

  # Start our TwiML response.
  resp = MessagingResponse()

  # Get all '/' to determine category, unit A, unit B, amount.
  # Structure: category/unitFrom/unitTo/amount
  needles = [m.start() for m in re.finditer('/', body)]

  # If there are more/less "/", return SMS message with the helper

  # message.
  if len(needles) != 3:
      resp.message("Bad format, use: category/unitFrom/unitTo/amount")
      return str(resp)

  category_length = len(body[:needles[0]])
  unit_from_length = len(body[needles[0] + 1:needles[1]])
  unit_to_length = len(body[needles[1] + 1:needles[2]])
  unit_amount_length = len(body[needles[2] + 1:])

  # Check if any of our parsed data is empty, if it is, return SMS with
  # the helper message.
  if (category_length == 0 or unit_from_length == 0 or
          unit_to_length == 0 or unit_amount_length == 0):
      resp.message("Bad format, use: category/unitFrom/unitTo/amount")
      return str(resp)

  userCategory = str(body[:needles[0]])
  unitFrom = str(body[needles[0] + 1:needles[1]])
  unitTo = str(body[needles[1] + 1:needles[2]])
  unitFromAmount = float(body[needles[2] + 1:])

  # If user put a negative amount, inform him.
  if unitFromAmount < 0:
      resp.message("Amount should be a non-negative number!")
      return str(resp)

  # If user entered invalid userCategory, tell him.
  if userCategory not in home.all_units:
      resp.message("Unit category is invalid!")
      return str(resp)

  # Search for units.
  pair = {"from_value": "", "to_value": ""}
  for item in home.all_units[userCategory]["units"]:
      if item["unit"] == unitFrom:
          pair["from_value"] = float(eval(item["value"]))
      if item["unit"] == unitTo:
          pair["to_value"] = float(eval(item["value"]))

  # If we didn't found user entered units, inform him.
  if len(str(pair["from_value"])) == 0 or len(str(pair["to_value"])) == 0:
      resp.message("Unit name(s) were not found!")
      return str(resp)

  # Convert.
  result = float(pair["from_value"] * unitFromAmount / pair["to_value"])
  # Format the number.
  result = '{:,}'.format(result)

  # Send SMS message with the conversion.
  resp.message(str(result))
  return str(resp)