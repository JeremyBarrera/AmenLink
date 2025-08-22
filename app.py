import os
import uuid
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import jwt
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.environ.get('ALLOWED_ORIGINS', '*')}})

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DATABASE'] = 'amenlink.db'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)

# JWT Authentication
def generate_token(user_id):
    payload = {
        'sub': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
            
        user_id = decode_token(token)
        if not user_id:
            return jsonify({'error': 'Invalid token'}), 401
            
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        g.current_user = user
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.current_user['is_admin']:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to AmenLink API"})

# ===== AUTHENTICATION =====
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    db = get_db()
    if db.execute('SELECT id FROM users WHERE username = ?', (data['username'],)).fetchone():
        return jsonify({'error': 'Username already exists'}), 409
    
    user_id = str(uuid.uuid4())
    password_hash = generate_password_hash(data['password'])
    
    db.execute(
        'INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)',
        (user_id, data['username'], password_hash)
    )
    db.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user_id,
            'username': data['username']
        }
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', 
        (data['username'],) 
    ).fetchone()
    
    if not user or not check_password_hash(user['password_hash'], data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    token = generate_token(user['id'])
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'is_admin': bool(user['is_admin'])
        }
    })

# ===== SERMONS =====
@app.route('/sermons', methods=['GET'])
def get_sermons():
    db = get_db()
    sermons = db.execute('''
        SELECT s.*, u.username as author 
        FROM sermons s
        LEFT JOIN users u ON s.user_id = u.id
        ORDER BY s.date DESC
    ''').fetchall()
    return jsonify([dict(sermon) for sermon in sermons])

@app.route('/sermons', methods=['POST'])
@auth_required
def add_sermon():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('speaker'):
        return jsonify({'error': 'Title and speaker required'}), 400
    
    sermon_id = str(uuid.uuid4())
    db = get_db()
    
    db.execute(
        '''INSERT INTO sermons 
           (id, title, speaker, date, audio_url, video_url, description, user_id) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            sermon_id,
            data['title'],
            data['speaker'],
            data.get('date', datetime.now().isoformat()),
            data.get('audio_url'),
            data.get('video_url'),
            data.get('description', ''),
            g.current_user['id']
        )
    )
    db.commit()
    
    new_sermon = db.execute('SELECT * FROM sermons WHERE id = ?', (sermon_id,)).fetchone()
    return jsonify({
        'message': 'Sermon added successfully',
        'sermon': dict(new_sermon)
    }), 201

@app.route('/sermons/<sermon_id>', methods=['GET'])
def get_sermon(sermon_id):
    db = get_db()
    sermon = db.execute('''
        SELECT s.*, u.username as author 
        FROM sermons s
        LEFT JOIN users u ON s.user_id = u.id
        WHERE s.id = ?
    ''', (sermon_id,)).fetchone()
    
    if not sermon:
        return jsonify({'error': 'Sermon not found'}), 404
    
    return jsonify(dict(sermon))

# ===== EVENTS =====
@app.route('/events', methods=['GET'])
def get_events():
    db = get_db()
    events = db.execute('''
        SELECT e.*, u.username as organizer 
        FROM events e
        LEFT JOIN users u ON e.user_id = u.id
        ORDER BY e.date DESC
    ''').fetchall()
    return jsonify([dict(event) for event in events])

@app.route('/events', methods=['POST'])
@auth_required
def add_event():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('date'):
        return jsonify({'error': 'Name and date required'}), 400
    
    event_id = str(uuid.uuid4())
    db = get_db()
    
    db.execute(
        '''INSERT INTO events 
           (id, name, description, date, location, image_url, user_id) 
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (
            event_id,
            data['name'],
            data.get('description', ''),
            data['date'],
            data.get('location', ''),
            data.get('image_url', ''),
            g.current_user['id']
        )
    )
    db.commit()
    
    new_event = db.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    return jsonify({
        'message': 'Event added successfully',
        'event': dict(new_event)
    }), 201

@app.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    db = get_db()
    event = db.execute('''
        SELECT e.*, u.username as organizer 
        FROM events e
        LEFT JOIN users u ON e.user_id = u.id
        WHERE e.id = ?
    ''', (event_id,)).fetchone()
    
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    return jsonify(dict(event))

# ===== DONATIONS =====
@app.route('/donations', methods=['GET'])
@auth_required
@admin_required
def get_donations():
    db = get_db()
    donations = db.execute('''
        SELECT d.*, u.username as donor 
        FROM donations d
        LEFT JOIN users u ON d.user_id = u.id
        ORDER BY d.date DESC
    ''').fetchall()
    return jsonify([dict(donation) for donation in donations])

@app.route('/donate', methods=['POST'])
@auth_required
def donate():
    data = request.get_json()
    if not data or not data.get('amount'):
        return jsonify({'error': 'Amount required'}), 400
    
    try:
        amount = float(data['amount'])
        if amount <= 0:
            raise ValueError
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400
    
    donation_id = str(uuid.uuid4())
    db = get_db()
    
    db.execute(
        '''INSERT INTO donations 
           (id, name, amount, date, message, user_id) 
           VALUES (?, ?, ?, ?, ?, ?)''',
        (
            donation_id,
            data.get('name', g.current_user['username']),
            amount,
            datetime.now().isoformat(),
            data.get('message', ''),
            g.current_user['id']
        )
    )
    db.commit()
    
    return jsonify({
        'message': 'Thank you for your donation!',
        'donation_id': donation_id
    }), 201

# ===== CONTACT =====
@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('message') or not data.get('email'):
        return jsonify({'error': 'Name, email, and message required'}), 400
    
    contact_id = str(uuid.uuid4())
    db = get_db()
    
    db.execute(
        '''INSERT INTO contacts 
           (id, name, email, message, date) 
           VALUES (?, ?, ?, ?, ?)''',
        (
            contact_id,
            data['name'],
            data['email'],
            data['message'],
            datetime.now().isoformat()
        )
    )
    db.commit()
    
    return jsonify({
        'message': 'Thank you for contacting us!',
        'contact_id': contact_id
    }), 201

@app.route('/contacts', methods=['GET'])
@auth_required
@admin_required
def get_contacts():
    db = get_db()
    contacts = db.execute('SELECT * FROM contacts ORDER BY date DESC').fetchall()
    return jsonify([dict(contact) for contact in contacts])

# ===== CHURCH LOCATIONS =====
@app.route('/locations', methods=['GET'])
def get_locations():
    db = get_db()
    locations = db.execute('SELECT * FROM church_locations').fetchall()
    return jsonify([dict(location) for location in locations])

@app.route('/locations', methods=['POST'])
@auth_required
@admin_required
def add_location():
    data = request.get_json()
    required_fields = ['name', 'address', 'city', 'state', 'zip_code', 'country']
    if not data or any(field not in data for field in required_fields):
        return jsonify({'error': 'All address fields are required'}), 400
    
    location_id = str(uuid.uuid4())
    db = get_db()
    
    db.execute(
        '''INSERT INTO church_locations 
           (id, name, address, city, state, zip_code, country, 
            latitude, longitude, phone, email, website, image_url, user_id) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            location_id,
            data['name'],
            data['address'],
            data['city'],
            data['state'],
            data['zip_code'],
            data['country'],
            data.get('latitude'),
            data.get('longitude'),
            data.get('phone'),
            data.get('email'),
            data.get('website'),
            data.get('image_url'),
            g.current_user['id']
        )
    )
    db.commit()
    
    new_location = db.execute('SELECT * FROM church_locations WHERE id = ?', (location_id,)).fetchone()
    return jsonify({
        'message': 'Location added successfully',
        'location': dict(new_location)
    }), 201

@app.route('/locations/nearby', methods=['GET'])
def find_nearby_churches():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    radius = request.args.get('radius', default=10, type=float)
    
    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude parameters required'}), 400
    
    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return jsonify({'error': 'Invalid coordinates'}), 400
    
    db = get_db()
    # Simple distance calculation (for production, use PostGIS or similar)
    locations = db.execute('''
        SELECT *, 
        (6371 * acos(
            cos(radians(?)) * cos(radians(latitude)) * 
            cos(radians(longitude) - radians(?)) + 
            sin(radians(?)) * sin(radians(latitude))
        )) AS distance
        FROM church_locations
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        HAVING distance < ?
        ORDER BY distance
    ''', (lat, lng, lat, radius)).fetchall()
    
    return jsonify([dict(location) for location in locations])

# Initialize the database and run the app
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)