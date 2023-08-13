from app import db
from datetime import datetime 
import pytz

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
  
    # shows = db.relationship("Show", backref="theatre", lazy=True, cascade="all, delete-orphan")
    
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
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), nullable=False)
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
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # ratings = db.relationship("Rating", backref="show", cascade="all, delete-orphan")
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