from app import flask_app
from flask import jsonify, render_template, request
from services.convert_unit_service import *

all_units = {}

@flask_app.route('/home')
def home():
  # Main data structre
  categories = [key for key in all_units.keys()]

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

    if user_category not in all_units:
        return jsonify({"error": "Invalid category."}), 400

    units = all_units[user_category]["units"]
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
    result = convert_unit(all_units, unit_category, unit_from, unit_to, amount)
    formatted_result = '{:,}'.format(result) + " " + unit_to

    return jsonify({"result": formatted_result})
  except Exception as e:
    return jsonify({"error": str(e)}), 500