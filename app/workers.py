import subprocess
# from app.tasks import display_hello, display_message_at_specific_time
# from app.tasks import send_daily_reminders, send_reminder_email
from app import app
from app.models import db
from datetime import timedelta
from celery.schedules import crontab

if __name__ == '__main__':
    celery = app.celery
    celery.conf.timezone = 'Asia/Kolkata'

    # Create database tables (if not created) within the app context
    with app.app_context():
        db.create_all()

    celery.start()
