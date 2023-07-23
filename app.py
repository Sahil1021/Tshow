from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'sahilbhure1021'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin = db.relationship('User', backref='theatres')

    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'admin_id': self.admin_id,
            # Add any other fields you want to include in the dictionary
        }
# API Endpoints

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

    # admin = User.query.get(admin_id)
    # if not admin or admin.role != 'admin':
    #     return jsonify({'message': 'Only admin can create theatres'}), 403
    admin = User.query.filter_by(id=admin_id, role='admin').first()
    if not admin:
        return jsonify({'message': 'Invalid admin ID'}), 403

    theatre = Theatre(name=name, address=address, admin_id=admin_id)
    db.session.add(theatre)
    db.session.commit()

    return jsonify({'message': 'Theatre created successfully'}), 201

@app.route('/api/theatres', methods=['GET'])
def list_theatres():
    theatres = Theatre.query.all()
    return jsonify([theatre.to_dict() for theatre in theatres])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
