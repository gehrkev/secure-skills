import csv
import os
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/write_csv')
def write_csv():
    '''
    Get the csv data from the request using 'csv_data'.
    Write it to a file in the static folder using csv library.
    '''
    csv_data = request.form.get('csv_data')
    if not csv_data and request.is_json:
        csv_data = request.get_json().get('csv_data')

    if not csv_data:
        return "No CSV data provided", 400

    os.makedirs('static', exist_ok=True)

    file_path = os.path.join('static', 'data.csv')
    with open(file_path, 'w', newline='') as f:
        f.write(csv_data)

    return "CSV file written successfully", 200
