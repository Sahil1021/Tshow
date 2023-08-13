from flask import request, jsonify, make_response, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app import app, db, mail, cache
from app.models import Booking, User, Theatre, Show, Rating
from app.helpers import get_user_monthly_report_data, send_report_email
from datetime import datetime, timedelta
from flask_cors import cross_origin 
from flask_jwt_extended import create_access_token
import pytz
import csv
from io import StringIO
from flask_mail import Message

@app.route('/generate_monthly_report/<int:year>/<int:month>', methods=['GET'])
@jwt_required()
def generate_user_monthly_report(year, month):
    try:
        current_username = get_jwt_identity()

        if not current_username:
            return jsonify({"error": "User not found."}), 404

        report_data = get_user_monthly_report_data(current_username, year, month)
        template_name = 'monthly_report.html'

        rendered_html = render_template(template_name, user=current_username, report_data=report_data, year=year, month=month)

        # Get the user's email using the username
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify({"error": "User not found."}), 404

        # Send the report email only to the logged-in user's email
        send_report_email(user.email, response.data, year, month)

        # Create a response with the HTML content
        response = make_response(rendered_html)
        response.headers['Content-Type'] = 'text/html'
        response.headers['Content-Disposition'] = f'attachment; filename=monthly_report_{year}_{month}.html'

        return jsonify({"message": "Monthly report generated and sent via email."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
# @cache.cached(timeout=300) 
@jwt_required()
def get_user_rated_shows():
    print("Executing get_user_rated_shows route...")
    try:
        current_username = get_jwt_identity()
        user = User.query.filter_by(username=current_username).first()
        if not user:
            return jsonify({"error": "User not found."}), 404

        rated_shows = [rating.show.to_dict() for rating in user.ratings]
        return jsonify(rated_shows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/theatres/<int:theatreId>/shows", methods=["GET"])
def get_shows_for_theatre(theatreId):
    theatre = Theatre.query.get(theatreId)
    if not theatre:
        return jsonify({"error": "Theater not found."}), 404

    shows = Show.query.filter_by(theatre_id=theatreId).all()
    return jsonify([show.to_dict() for show in shows]), 200

@app.route('/api/shows/UserBookings', methods=['GET'])
# @cache.cached(timeout=300) 
@jwt_required()
def get_user_bookings():
    print("Executing get_user_bookings route...")
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
# @cache.cached(timeout=300) 
def list_shows():
    print("Executing list_shows route...")
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
        with db.session.begin_nested():
            email_sent = False
            for show in theatre.shows:
                show_bookings = show.bookings
                # Send email to users who booked tickets for the cancelled show
                for booking in show_bookings:
                    user = User.query.filter_by(username=booking.user_id).first()
                    if user:
                        if send_email(user.email, show,booking):
                            email_sent = True
                        else:
                            email_sent = False
                            break
                    else:
                        print("User not found for booking:", booking.user_id)
                
                # Delete associated bookings and ratings for the show
                for booking in show_bookings:
                    db.session.delete(booking)
                for rating in show.ratings:
                    db.session.delete(rating)
                db.session.delete(show)
                
            # Delete the theatre if email sending is successful
            if email_sent or not theatre.shows:
                db.session.delete(theatre)
                db.session.commit()
                return jsonify({"message": "Theatre and associated shows deleted successfully and emails sent"}), 200
            else:
                return jsonify({"message": "Theatre and associated shows not deleted due to email sending failure"}), 500

    except Exception as e:
        print("Error deleting theatre:", e)
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the theatre."}), 500

@app.route('/api/shows/<int:show_id>', methods=['DELETE'])
def delete_show(show_id):
    show = Show.query.get(show_id)
    if not show:
        return jsonify({"error": "Show not found."}), 404

    try:
        with db.session.begin_nested():
            email_sent = False
            for booking in show.bookings:
                user = User.query.filter_by(username=booking.user_id).first()
                if user:
                    if send_email(user.email, show, booking):
                        email_sent = True
                    else:
                        email_sent = False
                        break
                else:
                    print("User not found for booking:", booking.user_id)
            
            # Delete bookings and show if email sending is successful or if there are no bookings
            if email_sent or not show.bookings:
                for booking in show.bookings:
                    db.session.delete(booking)
                for rating in show.ratings:
                    db.session.delete(rating)
                db.session.delete(show)
                db.session.commit()
                return jsonify({"message": "Show deleted successfully"}), 200
            else:
                return jsonify({"error": "Email sending failed, show not deleted."}), 500     
       
    except Exception as e:
        print("Error deleting show:", e)
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the show."}), 500

def send_email(user_email, show, booking):
    try:
        total_amount = show.ticket_price * booking.num_tickets 
        msg = Message("Show cancelled",
                      sender="madhurimuke24@gmail.com",
                      recipients=[user_email])
        msg.body = f"Dear User,\n\nUnfortunately, Your booking for the following show has been canceled:\n\nShow Name: {show.name}\nTheatre: {show.theatre.name}\nAddress: {show.theatre.address}\nTicket per price: {show.ticket_price}\nNo. of Tickets: {booking.num_tickets}\n\nYour booking amount {total_amount}Rs will be refunded.\n\nThank You!,\nThe Tshow Team"
       
        mail.send(msg)
        print(f"email sent to {user_email}")
        return True
    except Exception as e:
        print(f"Error sending email to {user_email}: {e}")
        return False

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
# @cache.cached(timeout=300) 
def list_theatres():
    print("Executing list_theatres route...")
    theatres = Theatre.query.all()
    return jsonify([theatre.to_dict() for theatre in theatres])
    return jsonify([show.to_dict() for show in shows])

@app.route('/api/theatres/<int:theatreId>/export_csv', methods=['GET'])
@jwt_required()
@cross_origin(origin='http://localhost:8080')  
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

        csv_data = csv_buffer.getvalue()
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment; filename=theatre_data.csv"
        response.headers["Content-type"] = "text/csv"

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500
