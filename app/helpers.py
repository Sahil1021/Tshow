from app import app, mail
import pytz
from app.models import Booking, User, db
from flask_mail import Message

def get_user_monthly_report_data(user_id, year, month):
    # Retrieve data for the report
    booked_shows = Booking.query.filter(
        Booking.user_id == user_id,
        db.extract('year', Booking.booking_date) == year,
        db.extract('month', Booking.booking_date) == month,
    ).all()

    # Convert the booking data to a list of dictionaries
    booked_shows_list = [booking.to_dict() for booking in booked_shows]

    return booked_shows_list

def send_report_email(user_email, report_data, year, month):
    try:
        msg = Message(f"Monthly Report - {year}/{month}",
                      sender="madhurimuke24@gmail.com",
                      recipients=[user_email])
        msg.body = f"Dear User,\n\nPlease find attached your monthly report for {year}/{month}.\n\nBest regards,\nThe Tshow Team"
        msg.attach(f"monthly_report_{year}_{month}.html", 'text/html', report_data)
        mail.send(msg)
        print(f"Monthly report email sent to {user_email}")
    except Exception as e:
        print(f"Error sending email to {user_email}: {e}")
