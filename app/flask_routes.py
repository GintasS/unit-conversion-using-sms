from app import flask_app
from flask import jsonify
import os

from services.read_conversion_files import *
from flask import render_template, request
from services.convert_unit_service import *

@flask_app.route('/home')
def home():
  # Main data structre
  home.all_units = {}

  # Directories
  root_directory = os.getcwd()
  sub_directory = "\\app\\static\\txt files\\"

  # Text files
  main_file = root_directory + sub_directory + "units.txt"
  sub_files = [
      "time_units.txt",
      "length_units.txt",
      "mass_units.txt",
      "electric_current_units.txt",
      "temperature_units.txt",
      "luminous_intensity_units.txt"
  ]
  currency_file = root_directory + sub_directory + "currencies.txt"
  sub_files = [root_directory + sub_directory + item for item in sub_files]

  # Read data & add it to the data structure.
  initialize_main_unit_conversion_file(home.all_units, main_file)
  initialize_sub_unit_conversion_files(home.all_units, sub_files)
  initialize_all_currencies(home.all_units, currency_file)
  
  # Categories to initialize 1st dropdown.
  categories = [key for key in home.all_units.keys()]

  # Render the template(GUI).
  return render_template(
    'index.html',
    title='Unit Co',
    categories=categories
  )

# Units update: will update unit dropdowns on user selection.
@flask_app.route("/units-update")
def index_update():
  try:
    user_category = str(request.args.get('userCategory', 0))

    if user_category not in home.all_units:
        return jsonify({"error": "Invalid category."}), 400

    units = home.all_units[user_category]["units"]
    return jsonify({"subUnits": units})
  except Exception as e:
      return jsonify({"error": str(e)}), 500

@flask_app.route("/convert")
def convert():
  # Url parameters from AJAX call.
  unit_category = request.args.get('userCategory', default='', type=str)
  unit_from = request.args.get('unitFrom', default='', type=str)
  amount = request.args.get('unitFromAmount', default=0.0, type=float)
  unit_to = request.args.get('unitTo', default='', type=str)

  # Validate input parameters
  if not unit_category or not unit_from or not unit_to or amount <= 0:
      return jsonify({"error": "Invalid input parameters."}), 400

  # Perform conversion
  try:
      result = convert_unit(home.all_units, unit_category, unit_from, unit_to, amount)
      formatted_result = '{:,}'.format(result) + " " + unit_to

      return jsonify({"result": formatted_result})
  except Exception as e:
      return jsonify({"error": str(e)}), 500