import requests

def get_exchange_rates(from_currency):
  url = f"https://v6.exchangerate-api.com/v6/c99433df1dfdfcf17f779e5f/latest/{from_currency}"
  try:
      response = requests.get(url)
      response.raise_for_status()  # Raise an error for bad status codes
      data = response.json()
      return data
  except requests.exceptions.RequestException as e:
      return {"error": str(e)}
    
def add_currencies_to_dict(data):
  if "conversion_rates" in data:
    currencies = data["conversion_rates"]
    return currencies
  else:
    return {"error": "Conversion rates not found in the response."}

def convert_from_currency_to_currency(from_currency, to_currency, amount):
  data = get_exchange_rates(from_currency)
  currency_dict = add_currencies_to_dict(data)

  to_currency_exchange_rate = currency_dict[to_currency]
  return float(amount) * float(to_currency_exchange_rate)
