'''
CS 3120 Machine Learning Term Project
Denver Crime Heatmap
Konstantin Zaremski
November 28, 2024
'''

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
