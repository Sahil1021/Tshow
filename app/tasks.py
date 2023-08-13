from celery.schedules import crontab, timedelta
from celery import Celery
from flask_mail import Message
from app import app, mail, celery
from datetime import datetime, timedelta
from app.models import Booking, User, db
import pytz
from app import celery
from celery.schedules import timedelta
from app import app  

@celery.task
def send_daily_reminders():
    print("Sending daily reminders...")
    with app.app_context():
        try:
            indian_timezone = pytz.timezone('Asia/Kolkata')
            current_datetime = datetime.now(indian_timezone)
            current_date = current_datetime.date()
            users = User.query.filter_by(role='user').all()
            for user in users:
                latest_booking_date = db.session.query(db.func.max(Booking.booking_date)).filter_by(user_id=user.username).scalar()
                if not latest_booking_date:
                    latest_booking_date = current_datetime.date() - timedelta(days=1)  # Set to 1 day ago, so it triggers the email for new users
                else:
                    latest_booking_date = latest_booking_date.date()
            
                days_since_last_booking = (current_date - latest_booking_date).days

                if days_since_last_booking > 0:
                    send_reminder_email(user.email)
                    print(f"Scheduled reminder email to {user.username} ({user.email})")
                else:
                    print(f"No need to send a reminder to {user.username} ({user.email})")
        except Exception as e:
            print("Error sending daily reminders:", e)
# Send a reminder email to a user

def send_reminder_email(user_email):
    try:
        msg = Message("Daily Reminder",
                      sender="madhurimuke24@gmail.com",
                      recipients=[user_email])
        msg.body = f"Dear User,\n\nThis is a reminder email sent after 1 day of inactivity about booking.\n\nBest regards,\nThe Tshow Team"
        mail.send(msg)
        print(f"Reminder email sent to {user_email}")
    except Exception as e:
        print(f"Error sending email to {user_email}: {e}")



# Calculate the desired execution time for 1:45 PM IST
indian_timezone = pytz.timezone('Asia/Kolkata')
current_datetime = datetime.now(indian_timezone)
desired_execution_time = current_datetime.replace(hour=0, minute=40)

# Calculate the time difference until the desired execution time
time_difference = desired_execution_time - current_datetime

# If the desired execution time has already passed for the day, add a day
if time_difference.total_seconds() < 0:
    time_difference += timedelta(days=1)

# Configure the Celery beat schedule
celery.conf.beat_schedule = {
    'sendReminderEmails': {
        'task': 'app.tasks.send_daily_reminders',
        'schedule': time_difference,
    },
}


