from apscheduler.schedulers.background import BackgroundScheduler
from services.sms_sender_service import incoming_sms

def schedule_jobs():
  try:
    print("STARTING THE SCHEDULER")
    scheduler = BackgroundScheduler()
    scan_incoming_sms_messages = scheduler.add_job(incoming_sms, 'interval', minutes=1)
    scheduler.start()
    print("SCHEDULER HAS BEEN STARTED")
  except Exception as e:
    print(e)