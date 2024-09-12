from os import environ
from flask_routes import flask_app
from utilities.helper import initialize_unit_conversion 
from services.scheduler_service import schedule_jobs

import logging

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO, format="%(levelname)s %(funcName)s: %(message)s")
  logging.info("[Unit Conversion] Starting Unit Conversion project..")
  
  initialize_unit_conversion()
  schedule_jobs()
  flask_app.run(host='0.0.0.0', port=8000)