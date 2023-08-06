from flask import Flask, request, jsonify, make_response, render_template, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime
from datetime import datetime, timedelta
import pytz
from flask_mail import Mail, Message
from flask_rq2 import RQ
# from rq.worker import Worker
# import schedule
import time
import threading
import redis
from rq_scheduler import Scheduler as rq_scheduler
from rq import Worker, Queue, Connection
# from rq.job import Job
# from rq.registry import StartedJobRegistry
import csv
from io import StringIO
# import pdfkit
# import os

scheduler_thread = None
worker_thread = None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'sahilbhure1021'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
# CORS(app)
# CORS(app, origins=['http://localhost:8080'])  # Replace with your frontend's domain

CORS(app, origins=['http://localhost:8080'], supports_credentials=True, expose_headers='Authorization')

rq = RQ(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'madhurimuke24@gmail.com'
app.config['MAIL_PASSWORD'] = 'icobcjyunbteepta'

mail = Mail(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id', ondelete='CASCADE'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    show = db.relationship("Show", backref="bookings", lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'show': self.show.to_dict(),  # Include the show details in the booking dictionary
            'num_tickets': self.num_tickets,
            'booking_date': self.get_booking_date(),
        }
    def get_booking_date(self):
        # Convert the booking_date to UTC
        booking_date_utc = self.booking_date.replace(tzinfo=pytz.timezone('UTC'))

        # Convert the UTC datetime to IST
        ist_timezone = pytz.timezone('Asia/Kolkata')
        booking_date_ist = booking_date_utc.astimezone(ist_timezone)

        # Format the IST datetime as a string
        formatted_date_str = booking_date_ist.strftime('%d/%m/%Y %I:%M:%S %p')

        return formatted_date_str
       
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin = db.relationship('User', backref='theatres')
    capacity = db.Column(db.Integer, nullable=False) 
  
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'admin_id': self.admin_id,
            'capacity': self.capacity,
        }
        
    def to_csv_row(self):
        id = self.id
        name= self.name
        address= self.address
        capacity = self.capacity
        return f"{id},{name},{address},{capacity}"
    
class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    theatre = db.relationship("Theatre", backref="shows", lazy=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(500))
    ticket_price = db.Column(db.Float, nullable=False, default=0.0)
    genre = db.Column(db.String(50), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

    average_rating = db.Column(db.Float, default=0.0)
    num_ratings = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.strftime('%Y-%m-%d'),
            'time': self.time.strftime('%H:%M'),
            'theatre_id': self.theatre_id,
            'theatre_name': self.theatre.name if self.theatre else "",
            'theatre_address': self.theatre.address if self.theatre else "",
            'description': self.description, 
            'genre': self.genre,
            'ticket_price': self.ticket_price,    
            'available_seats': self.available_seats if self.available_seats is not None else None,        
            'average_rating': self.average_rating,  # Include average_rating
            'num_ratings': self.num_ratings, 
        }

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Add a unique constraint to ensure a user can rate a show only once
    db.UniqueConstraint('user_id', 'show_id', name='uq_user_show_rating')

    user = db.relationship("User", backref="ratings")
    show = db.relationship("Show", backref="ratings")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'show_id': self.show_id,
            'rating': self.rating,
        }



@app.route('/generate_monthly_report/<int:year>/<int:month>', methods=['GET'])
@jwt_required()
def generate_user_monthly_report(year, month):
    try:
        current_user = get_jwt_identity()

        if not current_user:
            return jsonify({"error": "User not found."}), 404

        report_data = get_user_monthly_report_data(current_user, year, month)
        template_name = 'monthly_report.html'
        
        rendered_html = render_template(template_name, user=current_user, report_data=report_data, year=year, month=month)

        # Create a response with the HTML content
        response = make_response(rendered_html)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Disposition'] = f'attachment; filename=monthly_report_{year}_{month}.html'
        
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


    except Exception as e:
        return jsonify({"error": str(e)}), 500

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


@app.route('/api/shows/<int:show_id>/rate', methods=['POST'])
@jwt_required()
def rate_show(show_id):
    current_user_id = get_jwt_identity()
    print(current_user_id)
    # Check if the user has already rated the show
    existing_rating = Rating.query.filter_by(show_id=show_id, user_id=current_user_id).first()
    if existing_rating:
        return jsonify({"message": "You have already rated this show.", "average_rating": existing_rating.show.average_rating, "num_ratings": existing_rating.show.num_ratings}), 400

    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        return response
    else:
        print(f"Rating show with ID: {show_id}")
        data = request.get_json()
        rating = data.get('rating')

        if rating is None:
            return jsonify({'message': 'Rating not provided'}), 400

        show = Show.query.get(show_id)
        if not show:
            return jsonify({'message': 'Show not found'}), 404

        # Update the show's average rating and number of ratings
        if show.average_rating is None:
            show.average_rating = rating
            show.num_ratings = 1
        else:
            show.average_rating = (show.average_rating * show.num_ratings + rating) / (show.num_ratings + 1)
            show.num_ratings += 1

        db.session.commit()
        new_rating = Rating(user_id=current_user_id, show_id=show_id, rating=rating)
        db.session.add(new_rating)
        db.session.commit()

        return jsonify({
            'message': 'Show rating updated',
            'average_rating': show.average_rating,
            'num_ratings': show.num_ratings
        }), 200
       
@app.route('/api/shows/UserRatedShows', methods=['GET'])
@jwt_required()
def get_user_rated_shows():
    try:
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify({"error": "User not found."}), 404

        rated_shows = [rating.show.to_dict() for rating in user.ratings]
        return jsonify(rated_shows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ...
@app.route("/api/theatres/<int:theatreId>/shows", methods=["GET"])
def get_shows_for_theatre(theatreId):
    theatre = Theatre.query.get(theatreId)
    if not theatre:
        return jsonify({"error": "Theater not found."}), 404

    shows = Show.query.filter_by(theatre_id=theatreId).all()
    return jsonify([show.to_dict() for show in shows]), 200

@app.route('/api/shows/UserBookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    try:
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify({"error": "User not found."}), 404

        bookings = Booking.query.filter_by(user_id=current_username).all()
        booked_shows = [booking.to_dict() for booking in bookings]
        return jsonify(booked_shows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/shows/<int:show_id>/book", methods=["POST"])
@jwt_required()
def book_show(show_id):
    try:
        verify_jwt_in_request()
        data = request.json
        num_tickets = data.get("numTickets")
        if num_tickets is None or not isinstance(num_tickets, int) or num_tickets <= 0:
            return jsonify({"error": "Invalid number of tickets. Please provide a positive integer value."}), 422
        show = Show.query.get(show_id)
        if not show:
            return jsonify({"error": "Show not found."}), 404

        if num_tickets > show.available_seats:
            return jsonify({"error": "Not enough available seats."}), 409
        current_user_id = get_jwt_identity()  
        booking = Booking(user_id=current_user_id, show_id=show_id, num_tickets=num_tickets)
        db.session.add(booking)
        db.session.commit()
        show.available_seats -= num_tickets
        db.session.commit()
        return jsonify({"message": "Show booked successfully!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route("/api/shows/<int:show_id>/seats", methods=["GET"])
def get_available_seats(show_id):
    show = Show.query.get(show_id)
    if not show:
        return jsonify({"error": "Show not found."}), 404

    return jsonify({"available_seats": show.available_seats}), 200

@app.route("/api/shows", methods=["POST"])
def create_show():
    data = request.json
    theatre_id = data["theatre_id"]
    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({"error": "Theatre not found."}), 404
    date = datetime.strptime(data["date"], '%Y-%m-%d')
    time = datetime.strptime(data["time"], '%H:%M').time()
    description = data.get("description")
    genre = data.get("genre")
    ticket_price = data.get("ticket_price") 

    new_show = Show(theatre_id=theatre_id, name=data["name"], time=time, date=date, description=description, genre=genre, ticket_price=ticket_price, available_seats=theatre.capacity)
    db.session.add(new_show)
    db.session.commit()
    return jsonify({"message": "Show created successfully!"}), 201

@app.route('/api/shows', methods=['GET'])
def list_shows():
    current_date = datetime.utcnow().date()
    shows = Show.query.filter(Show.date >= current_date).all()
    return jsonify([show.to_dict() for show in shows])

@app.route('/api/shows/<int:show_id>', methods=['GET', 'PUT'])
def get_or_update_show(show_id):
    if request.method == 'GET':
        show = Show.query.get(show_id)
        if not show:
            return jsonify({'message': 'Show not found'}), 404
        return jsonify(show.to_dict()), 200

    if request.method == 'PUT':
        try:
            show = Show.query.get(show_id)
            if not show:
                return jsonify({'message': 'Show not found'}), 404

            data = request.json
            show.name = data['name']
            show.time = datetime.strptime(data['time'], '%H:%M').time()
            show.date = datetime.strptime(data['date'], '%Y-%m-%d').date()

            show.description = data['description']
            show.ticket_price = data['ticket_price']
            show.genre = data['genre']
            
            db.session.commit()

            return jsonify(show.to_dict()), 200
        except Exception as e:
            print('Error updating show:', e)
            return jsonify({'message': 'An error occurred while updating the show'}), 500

    return jsonify({'message': 'Method not allowed'}), 405

@app.route('/api/shows/<int:show_id>', methods=['DELETE'])
def delete_show(show_id):
    show = Show.query.get(show_id)
    if not show:
        return jsonify({"error": "Show not found."}), 404

    try:
        db.session.delete(show)
        db.session.commit()
        return jsonify({"message": "Show deleted successfully"}), 200
    except Exception as e:
        print("Error deleting show:", e)
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the show."}), 500
    
@app.route("/api/theaters", methods=["GET"])
def get_theaters_by_region():
    address = request.args.get("address")
    theaters = Theatre.query.filter_by(address=address).all()
    theater_data = [{"id": theater.id, "name": theater.name, "address": theater.address} for theater in theaters]
    return jsonify(theater_data)
 
@app.route("/api/theatres/<int:theatreId>", methods=["PUT"])
def update_theatre(theatreId):
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    capacity = data.get('capacity')

    theatre = Theatre.query.get(theatreId)
    if not theatre:
        return jsonify({"error": "Theatre not found."}), 404

    theatre.name = name if name else theatre.name
    theatre.address = address if address else theatre.address
    theatre.capacity = capacity if capacity else theatre.capacity

    db.session.commit()

    return jsonify({"message": "Theatre updated successfully"}), 200

@app.route('/api/theatres/<int:theatreId>', methods=['DELETE'])
def delete_theatre(theatreId):
    theatre = Theatre.query.get(theatreId)
    if not theatre:
        return jsonify({"error": "Theatre not found."}), 404

    try:
        # Delete all shows associated with the theatre
        for show in theatre.shows:
            db.session.delete(show)

        db.session.delete(theatre)
        db.session.commit()
        return jsonify({"message": "Theatre and associated shows deleted successfully"}), 200
    except Exception as e:
        # Log the exception to see the specific error
        print("Error deleting theatre:", e)
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the theatre."}), 500

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not username or not email or not password or not role:
        return jsonify({'message': 'All fields are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 409

    new_user = User(username=username, email=email, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=user.username)
        return jsonify({'access_token': access_token, 'role': user.role})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    return jsonify({'username': user.username, 'role': user.role, 'email': user.email, 'id': user.id })

@app.route('/api/theatres', methods=['POST'])
def create_theatre():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    admin_id = data.get('admin_id')
    capacity = data.get('capacity')

    admin = User.query.filter_by(id=admin_id, role='admin').first()
    if not admin:
        return jsonify({'message': 'Invalid admin ID'}), 403
    theatre = Theatre(name=name, address=address, admin_id=admin_id, capacity=capacity)
    db.session.add(theatre)
    db.session.commit()
    return jsonify({'message': 'Theatre created successfully'}), 201

@app.route("/api/theatres/<int:theatreId>", methods=["GET"])
def get_theatre_by_id(theatreId):
    theatre = Theatre.query.get(theatreId)
    if not theatre:
        return jsonify({"error": "Theater not found."}), 404

    return jsonify(theatre.to_dict()), 200

@app.route('/api/theatres', methods=['GET'])
def list_theatres():
    theatres = Theatre.query.all()
    return jsonify([theatre.to_dict() for theatre in theatres])
    return jsonify([show.to_dict() for show in shows])

# ...
def run_scheduler():
    with app.app_context():
        # Establish a connection to Redis
        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

        # Start the scheduler using the rq_scheduler.Scheduler class
        with Connection(redis_conn):
            scheduler = rq_scheduler(connection=redis_conn)

            # Schedule the send_daily_reminders function to be executed daily
            scheduler.schedule(
                scheduled_time=datetime.utcnow() + timedelta(seconds=5),  # Schedule 5 seconds from now
                func=send_daily_reminders,
                interval=24 * 60 * 60,  # Execute daily
                repeat=None  # Run only once at the scheduled time
            )

def send_daily_reminders():
    with app.app_context():
        try:
            print("Sending daily reminders...")
            current_datetime = datetime.utcnow()
            current_date = current_datetime.date()

            users = User.query.filter_by(role='user').all()
            for user in users:
                latest_booking_date = db.session.query(db.func.max(Booking.booking_date)).filter_by(user_id=user.username).scalar()
                if not latest_booking_date:
                    latest_booking_date = current_datetime.date() - timedelta(days=1)  # Set to 1 day ago, so it triggers the email for new users
                else:
                    latest_booking_date = latest_booking_date.date()

                # print(current_datetime.date())
                # print(latest_booking_date)
                days_since_last_booking = (current_date - latest_booking_date).days

                # print(days_since_last_booking)

                if days_since_last_booking >0:  # Change > to >= to include new users who booked within the last 24 hours
                    send_reminder_email(user.email)
                    print(f"Scheduled reminder email to {user.username} ({user.email})")
                else:
                    print(f"No need to send a reminder to {user.username} ({user.email})")
        except Exception as e:
            print("Error sending daily reminders:", e)

def send_reminder_email(user_email):
    try:
        msg = Message("Daily Reminder",
                      sender="madhurimuke24@gmail.com",
                      recipients=[user_email])
        msg.body = f"Dear User,\n\nThis is a reminder email sent after 1 day of inactivity about booking.\n\nBest regards,\nThe Movie Ticket Booking Team"
        mail.send(msg)
        print(f"Reminder email sent to {user_email}")
    except Exception as e:
        # Log the error and traceback to the console
        print(f"Error sending email to {user_email}: {e}")
        # traceback.print_exc()


from flask_cors import cross_origin
# ...

@app.route('/api/theatres/<int:theatreId>/export_csv', methods=['GET'])
@jwt_required()
@cross_origin(origin='http://localhost:8080')  # Set the allowed origin
def export_theatre_csv(theatreId):
    try:
        theatre = Theatre.query.get(theatreId)
        if not theatre:
            return jsonify({"error": "Theatre not found."}), 404

        # Create a StringIO buffer to hold CSV data
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)

        # Write the header row
        header_row = ["Theatre ID", "Name", "Address", "Capacity"]
        csv_writer.writerow(header_row)

        # Write the theatre data as a row
        theatre_row = [theatre.id, theatre.name, theatre.address, theatre.capacity]
        csv_writer.writerow(theatre_row)

        # Write a separator
        csv_writer.writerow([])

        # Write show details
        show_header_row = ["Show ID", "Name", "Date", "Time", "Description", "Ticket Price", "Genre", "Available Seats"]
        csv_writer.writerow(show_header_row)

        for show in theatre.shows:
            show_row = [
                show.id,
                show.name,
                show.date.strftime('%Y-%m-%d'),
                show.time.strftime('%H:%M'),
                show.description,
                show.ticket_price,
                show.genre,
                show.available_seats
            ]
            csv_writer.writerow(show_row)

        # Get the CSV data as a string
        csv_data = csv_buffer.getvalue()

        # Set up the response with the CSV data
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment; filename=theatre_data.csv"
        response.headers["Content-type"] = "text/csv"

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

    # Create a list containing the queue(s) that the worker should listen to
    queues = [Queue('default', connection=redis_conn)]

    # # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    worker_thread = threading.Thread(target=send_daily_reminders)

    try:
        # Start the Flask app in the main thread

        app.run(debug=True)
        worker_thread.start()

    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Shutting down...")
        # Stop the scheduler thread gracefully
        if scheduler_thread:
            scheduler_thread.join()

        print("Scheduler thread stopped.")