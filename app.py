from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from scripts.Backend import *
import os
import pyrebase

config = {
    "apiKey": "AIzaSyAQNWWueglSwwcU9X07k5x-tlVC9wykCC4",
    "authDomain": "course-tracker-11.firebaseapp.com",
    "databaseURL": "https://course-tracker-11.firebaseio.com",
    "storageBucket": "course-tracker-11.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__, static_folder='build/static', template_folder='build/')
CORS(app)
backend = Backend()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():
    crn = request.form['crn']
    term = request.form['term']
    db.child('courses').update({f"{crn}": f"{term}"})
    return jsonify('This course has been added to the list to track')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 4000), debug=True)

