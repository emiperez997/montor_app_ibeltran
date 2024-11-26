from libs.db import get_users, update_last_seen
from libs.latest_announcement import fetch_latest_announcement
from libs.send_mail import send_mail_announcement
import time
import datetime

SCHEDULE_TIMES = [
  datetime.time(9, 0), # 9:00 AM
  datetime.time(20, 11), # 6:10 PM
  datetime.time(20, 0) # 8:00 PM
]

is_monitoring = False

def wait_until_month(month):
  while datetime.datetime.now().month != month:
    time.sleep(86400) # Wait 1 day

def wait_until_next_schedule():
  now = datetime.datetime.now()
  today = now.date()

  next_run = None
  for schedule_time in SCHEDULE_TIMES:
    run_time = datetime.datetime.combine(today, schedule_time)
    if run_time > now:
      next_run = run_time
      break
  
  if not next_run:
    next_run = datetime.datetime.combine(today + datetime.timedelta(days=1), SCHEDULE_TIMES[0]) 

  time_to_wait = (next_run - now).total_seconds()
  time.sleep(time_to_wait)

def monitor_page():
  while True:
    today = datetime.datetime.now().date()

    if today.month != 2:
      print("Waiting until February...")
      wait_until_month(2)
    
    global is_monitoring
    is_monitoring = True

    print("Checking for new announcements...")
    wait_until_next_schedule()
    
    users = get_users()
    
    latest_announcement = fetch_latest_announcement()

    # tuple to dict
    users = [dict(id=user[0], email=user[1], last_seen=user[2]) for user in users]

    count = 0

    if users:
      for user in users: 
        if user["last_seen"] != latest_announcement:
          print("Sending email to", user["email"])
          update_last_seen(user["email"], latest_announcement)
          send_mail_announcement(user["email"], latest_announcement)
          count += 1
    
    print(f"Emails sent: {count}")