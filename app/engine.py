'''
CS 3120 Machine Learning Term Project
Denver Crime Heatmap
Konstantin Zaremski
December 1, 2024
'''

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
import pickle

from .map import MapGrid, UPPER_LEFT_CORNER, LOWER_RIGHT_CORNER
from .models import CrimePrediction
from .database import get_session

def get_denver_time(time_delta):
    # Get time values
    utc_now = datetime.utcnow()
    year = utc_now.year
    start_dst = datetime(year, 3, (14 - (datetime(year, 3, 1).weekday() + 1) % 7))
    end_dst = datetime(year, 11, (7 - (datetime(year, 11, 1).weekday() + 1) % 7))

    if start_dst <= utc_now.replace(tzinfo=None) < end_dst:
        offset = timedelta(hours=-6)
    else:
        offset = timedelta(hours=-7)

    denver_time = utc_now + offset

    # Apply the time delta (add or subtract hours)
    denver_time += timedelta(hours=time_delta)

    day_of_year = denver_time.timetuple().tm_yday
    hour = denver_time.hour
    day_of_week = (denver_time.weekday() + 1) % 7

    return year, day_of_year, day_of_week, hour

def generate_predictions(time_delta):
    # Load trained models using pickle
    with open('./artifacts/50m_crime_type_model.pkl', 'rb') as f:
        crime_type_model = pickle.load(f)

    with open('./artifacts/50m_crime_count_model.pkl', 'rb') as f:
        crime_count_model = pickle.load(f)

    # Generate grid
    map_grid = MapGrid(UPPER_LEFT_CORNER, LOWER_RIGHT_CORNER).get_grid()

    # Get the time
    year, day_of_year, day_of_week, hour = get_denver_time(time_delta)

    # Convert hour to a value between 0 and 1 by dividing by 24 (since there are 24 hours in a day)
    hour_normalized = hour / 24.0
    
    # Calculate sine and cosine
    hour_sin = np.sin(2 * np.pi * hour_normalized)
    hour_cos = np.cos(2 * np.pi * hour_normalized)

    # Get SQLAlchemy session using get_session()
    session = get_session()

    # Query for existing prediction to skip model inference
    existing_prediction = session.query(CrimePrediction).filter_by(x=map_grid[0]['block'][0], y=map_grid[0]['block'][1], hour=hour, day_of_year=day_of_year).first()
    
    # Skip if prediction already exists in the DB
    if existing_prediction:
        return
    
    print(f'Generating Predictions for DAY_OF_YEAR={day_of_year}, HOUR={hour}')

    # Prepare features for all grid cells at once
    features_type = []
    features_count = []
    for cell in map_grid:
        x, y = cell['block']

        features_type.append([x, y, year, day_of_year, day_of_week, hour_sin, hour_cos])

    # Convert the lists to numpy arrays
    features_type = np.array(features_type)
    features_count = np.array(features_count)

    # Create DataFrames
    df = pd.DataFrame(features_type, columns=[
        'X_BLOCK',
        'Y_BLOCK',
        'YEAR',
        'DAY_OF_YEAR',
        'DAY_OF_WEEK',
        'HOUR_SIN',
        'HOUR_COS',
    ])

    # Predict for all grid cells at once
    crime_type = crime_type_model.predict(df)
    crime_count = crime_count_model.predict(df)

    # Create CrimePrediction instances
    predictions = [
        CrimePrediction(
            x=map_grid[i]['block'][0],
            y=map_grid[i]['block'][1],
            day_of_year=day_of_year,
            hour=hour,
            crime_type=int(crime_type[i]),
            crime_count=float(crime_count[i])
        )
        for i in range(len(map_grid))
    ]

    # Bulk insert into the database
    session.bulk_save_objects(predictions)
    session.commit()

    print(f'Finished Predictions for DAY_OF_YEAR={day_of_year}, HOUR={hour}')
