# denver-crime-heatmap
CS 3120 Machine Learning Project - Crime prediction heatmap web app (and data analysis) for Denver, CO.

This project provides a crime prediction heatmap web application built using Flask, where users can visualize crime data and make predictions based on machine learning models. The app is powered by data from the city of Denver.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Flask App](#running-the-flask-app)
- [Directory Structure](#directory-structure)

## Prerequisites

Before running the project, make sure you have Python 3.8+ installed on your system.

You will also need `pip` for managing Python packages.

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/yourusername/denver-crime-heatmap.git
cd denver-crime-heatmap
```

### 2. Create a Python Virtual Environment

Create a new Python virtual environment to isolate project dependencies:

#### On macOS/Linux:

```bash
python3 -m venv venv
```

#### On Windows:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment:

#### On macOS/Linux:

```bash
source venv/bin/activate
```

#### On Windows:

```bash
.\venv\Scripts\activate
```

### 4. Install Required Dependencies

Install the necessary Python packages from the `requirements_webapp.txt` file:

```bash
pip install -r requirements_webapp.txt
```

This will install Flask, machine learning libraries, and other dependencies required for the web app and data analysis.

## Running the Flask App

Once the dependencies are installed, you can start the Flask web application.

1. Make sure you're in the project directory, and your virtual environment is activated.
2. Run the following command to start the Flask development server:

```bash
python app/app.py
```

This will start the server, and you should see output similar to:

```bash
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

You can now visit `http://127.0.0.1:5000/` in your web browser to view the app.

## Directory Structure

Here's a breakdown of the project structure:

```
denver-crime-heatmap/
│
├── app/
│   ├── app.py            # Main Flask app file
│   ├── static/           # Static files (CSS, JS, images)
│   └── templates/        # HTML templates for the web app
│
├── data/                 # Data files (e.g., CSVs, models)
│
├── requirements_webapp.txt # Python dependencies for the web app
│
└── README.md             # This file
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
