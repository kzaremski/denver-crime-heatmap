'''
CS 3120 Machine Learning Term Project
Denver Crime Heatmap
Konstantin Zaremski
November 28, 2024
'''

from flask import Flask, render_template, jsonify, request
import threading
from time import sleep
from .models import CrimePrediction, Base, engine
from .engine import generate_predictions, get_denver_time
from .database import get_session
from .map import block_to_lat_lon
import pickle
from sklearn.preprocessing import LabelEncoder

FUTURE_HOURS_PREDICTION_BOUND = 170

app = Flask(__name__)

# Create all tables
Base.metadata.create_all(engine)

# Figure out the class decoder
with open('./artifacts/50m_crime_type_model.pkl', 'rb') as f:
    encoder = pickle.load(f)

label_to_int = {str(label): int(idx) for idx, label in enumerate(encoder.classes_)}
int_to_label = {int(idx): str(label) for idx, label in enumerate(encoder.classes_)}

@app.route('/')
def index():
    return render_template('index.html')

offense_category_labels = {
    "public-disorder": "Public Disorder",
    "drug-alcohol": "Drug and Alcohol Offenses",
    "theft-from-motor-vehicle": "Theft from Motor Vehicle",
    "larceny": "Larceny",
    "other-crimes-against-persons": "Other Crimes Against Persons",
    "all-other-crimes": "All Other Crimes",
    "murder": "Murder",
    "robbery": "Robbery",
    "aggravated-assault": "Aggravated Assault",
    "arson": "Arson",
    "burglary": "Burglary",
    "auto-theft": "Auto Theft",
    "white-collar-crime": "White Collar Crime"
}

@app.route('/api/predictions', methods=['POST'])
def serve_predictions():
    data = request.json  # Expecting JSON input
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    time_delta = int(data.get('time_delta'))

    year, day_of_year, day_of_week, hour = get_denver_time(time_delta)

    # Get SQLAlchemy session using get_session()
    session = get_session()

    query = session.query(CrimePrediction)
    query = query.filter(CrimePrediction.day_of_year == day_of_year)
    query = query.filter(CrimePrediction.hour == hour)

    # Execute query and fetch results
    predictions = query.all()

    if not predictions:
        return jsonify({"status": "unavailable", "message": "No predictions found for the specified time."}), 200

    # Format predictions into a list of dictionaries
    results = [
        {
            "lat": block_to_lat_lon(prediction.x, prediction.y)[0],
            "lon": block_to_lat_lon(prediction.x, prediction.y)[1],
            "crime_type": int(prediction.crime_type),
            "crime_count": float(prediction.crime_count),
        }
        for prediction in predictions
    ]

    return jsonify({
        "predictions": results,
        "offense_category_labels": offense_category_labels,
        "label_to_int": label_to_int,
        "int_to_label": int_to_label,
    }), 200

def prediction_generation_background_task():
    print("Started Prediction Daemon")
    while True:
        for time_delta in range(-24, FUTURE_HOURS_PREDICTION_BOUND):
            generate_predictions(time_delta)
        print('Caught up on predictions!')
        sleep(3600 * 10)

def start_background_thread():
    # Start the background thread for generating predictions
    thread = threading.Thread(target=prediction_generation_background_task, daemon=True)
    thread.start()

start_background_thread()
