import os
from services.read_conversion_files import *
from flask_routes import all_units
import logging

def initialize_unit_conversion():
  logging.info("[Unit Conversion Files] Starting to read from .TXT files to get the units...")

  root_directory = os.getcwd()
  sub_directory = os.path.join("app", "static", "txt files")
  main_file = os.path.join(root_directory, "app", "static", "txt files", "units.txt")
  currency_file = os.path.join(root_directory, "app", "static", "txt files", "currencies.txt")

  sub_files = [
    "time_units.txt",
    "length_units.txt",
    "mass_units.txt",
    "electric_current_units.txt",
    "temperature_units.txt",
    "luminous_intensity_units.txt"
  ]

  sub_files = [os.path.join(root_directory, sub_directory, item) for item in sub_files]

  # Read data & add it to the data structure.
  initialize_main_unit_conversion_file(all_units, main_file)
  initialize_sub_unit_conversion_files(all_units, sub_files)
  initialize_all_currencies(all_units, currency_file)

  logging.info("[Unit Conversion Files] All unit conversion files have been successfully initialized.")

def is_incoming_sms_message_valid(message):
  if message.count('/') != 3:
    raise ValueError("Invalid SMS message format. Should have three '/': CONVERT unitCategory/unitFrom/unitTo/amount !")

  # Split the message by slashes
  parts = message.split('/')
  if len(parts) != 4:
    raise ValueError("Invalid SMS message format. Should have a unit category, a unit from, a unit to and an amount: CONVERT unitCategory/unitFrom/unitTo/amount !")
  
  unit_category, unit_from, unit_to, unit_amount = parts
  if not unit_category or not unit_from or not unit_to or not unit_amount:
    raise ValueError("Invalid SMS message format. Should be: CONVERT unitCategory/unitFrom/unitTo/amount")
  if is_unit_category_exists(all_units, unit_category) is False:
    raise ValueError(f"Invalid SMS message data. The Unit category {unit_category} does not exist!")
  if is_sub_unit_exists_in_category(all_units, unit_category, unit_from) is False:
    raise ValueError(f"Invalid SMS message data. The Sub Unit of {unit_from} does not exist!")  
  if is_sub_unit_exists_in_category(all_units, unit_category, unit_to) is False:
    raise ValueError(f"Invalid SMS message data. The Sub Unit of {unit_to} does not exist!")  
  
  # Check if the amount is a valid float
  unit_amount_float = None
  try:
    unit_amount_float = float(unit_amount)
  except ValueError:
    raise ValueError("Invalid SMS message data. Amount should be a valid number !")
  
  if unit_amount_float <= 0:
    raise ValueError("Invalid SMS message data. Amount should be a positive number !")

  return True

def is_unit_category_exists(all_units, unit_category):
  return unit_category in all_units

def is_sub_unit_exists_in_category(all_units, unit_category, sub_unit):
  return any(item["unit"] == sub_unit for item in all_units[unit_category]["units"])