import csv
import os
import io
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

    if not csv_data:
        return "No CSV data provided", 400

    csv_reader = csv.reader(io.StringIO(csv_data))
    rows = list(csv_reader)

    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    filepath = os.path.join(static_folder, 'data.csv')

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return "CSV file written successfully", 200
