from services.currency_converter import convert_from_currency_to_currency

def convert_unit(all_units, unitCategory, unitFrom, unitTo, amount):
  # Validate input parameters
  if not all_units or not unitCategory or not unitFrom or not unitTo or amount <= 0:
      return "Invalid data."

  if unitCategory == "currencies":
      return convert_from_currency_to_currency(unitFrom, unitTo, amount)

  # If user entered invalid userCategory, inform them
  if unitCategory not in all_units:
      return "Invalid Unit Category."

  # Find unit A & B
  from_value = None
  to_value = None
  for item in all_units[unitCategory]["units"]:
    if item["unit"] == unitFrom:
        from_value = float(eval(item["value"]))
    if item["unit"] == unitTo:
        to_value = float(eval(item["value"]))

  # If we didn't find user-entered units, inform them
  if from_value is None or to_value is None:
    return "Invalid Unit(s)."

  # Convert
  result = from_value * amount / to_value
  return result