from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the database
DATABASE_URL = os.getenv('DATABASE_URL')  # Use environment variable for database URL
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a model for storing data
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, name, age):
        self.name = name
        self.age = age

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # Get JSON data from the request
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({'message': 'Name and age are required!'}), 400

    # Insert data into the database
    new_user = UserData(name, age)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Data successfully saved!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
