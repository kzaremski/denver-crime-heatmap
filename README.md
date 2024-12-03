# Denver Crime Heatmap
**CS 3120 Machine Learning Project**  
Crime Prediction Heatmap Web Application for Denver, CO

This project provides a web-based crime prediction heatmap powered by machine learning models. Built using Flask, the web application enables users to visualize crime data and make predictions based on historical crime patterns in Denver, CO.

## Deployed Instance
<https://dencrime.zarem.ski>

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Flask Application](#running-the-flask-application)
- [Directory Structure](#directory-structure)
- [Architecture](#architecture)
- [Model Training & Performance](#model-training-and-performance)
- [License](#license)

## Prerequisites

To run this project locally, you will need:

- Python 3.8+ installed on your system
- `pip` or `pip3` for managing Python packages

Ensure that you have the required dependencies listed in the `requirements_webapp.txt` file before proceeding with setup.

## Setup Instructions

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

Clone the repository to your local machine.

### 2. Create a Python Virtual Environment

For most python installs you will need to create a virtual environment since they moved away from system wide packages.

#### On macOS/Linux:

```bash
python3 -m venv .venv
```

#### On Windows:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment to isolate dependencies:

#### On macOS/Linux:

```bash
source .venv/bin/activate
```

#### On Windows:

```bash
.\venv\Scripts\activate
```

### 4. Install Required Dependencies

Install the necessary packages from the `requirements_webapp.txt` file:

```bash
pip3 install -r requirements_webapp.txt
```

This will install Flask, machine learning libraries, and other dependencies required for the web application and data analysis.

## Running the Flask Application

After setting up the environment and installing dependencies, follow these steps to run the Flask application:

1. Ensure you are in the project directory with the virtual environment activated.
2. Start the Flask development server with the following command:

```bash
python3 wsgi.py
```

You should see the following output indicating the server is running:

```bash
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Now, you can open your browser and navigate to `http://127.0.0.1:5000/` to interact with the application. The app will need to build the predictions database, which may take up to a few hours.

## Directory Structure

The project is organized as follows:

```
denver-crime-heatmap/
│
├── app/                   # Contains the Flask application
│   ├── app.py             # Main application file with all HTTP endpoints and the prediction background thread
│   ├── database.py        # Database controller with session generator
│   ├── engine.py          # Prediction engine that runs on the pickled models
│   ├── map.py             # Utility class for the map grid and geo functions and transformations
│   ├── models.py          # Contains database models (SQLAlchemy)
│   ├── static/            # Static files (CSS, JavaScript, images)
│   └── templates/         # HTML templates for rendering the web pages
├── data/                  # Contains data files
├── artifacts/             # Contains trained models
├── denver_crime_heatmap.ipynb # EDA, training
├── requirements_webapp.txt # Python dependencies for the web application
├── ...                    # Other misc.
└── README.md              
```

## Architecture

This is a simple web application. It serves everything and handles requests using a Flask web application. Model predictions are cached in an SQLite database. There is a background thread that runs periodically computing the next predictions in the future.

## Model Training and Performance
See the notebook in the root for my EDA and model training. I have used HistGradientBoosting, RandomForest, and even pytorch neural networks ranging from 3 to 12 layers deep.
I was unable to achieve good performance for any, so I proceeded with my original pick of HistGradientBoosting models.

### Crime Likelihood/Count Regressor (HistGradientBoostingRegressor)  
This model was trained to predict the likelihood or count of crimes based on the features in the dataset. Despite optimizing hyperparameters and performing feature engineering, the model's performance was underwhelming, with a low R-squared value indicating it struggled to explain variance in the data. The metrics suggest the predictions are close in magnitude but not reliably accurate. This could be due to limited signal in the dataset or missing important predictive features.  

#### Metrics
* Mean Squared Error: 0.10421870655349885
* Root Mean Squared Error: 0.32282922196340724
* Mean Absolute Error: 0.14820025331663794
* R2: 0.030293926173318053

### Crime Type Classifier (HistGradientBoostingClassifier)
This model was designed to classify the type of crime based on the provided features. The precision, recall, and F1 scores indicate that the model often misclassifies crime types, likely due to the dataset's class imbalance or overlapping feature distributions. Even with hyperparameter tuning and regularization, the classifier performed poorly. The high root mean squared error further shows difficulty in aligning predictions with true labels.  

#### Metrics
* Precision: 0.2863567980346278
* Recall: 0.28638432187812946
* F1 Score: 0.26120728152142597
* Root Mean Squared Error: 4.750856661203363

In the future, more can be done in the way of feature engineering and model optimization. I would like to explore deep neural networks with more parameters to accommodate the spatial and temporal resolution of the data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

