import csv
from flask import Flask
from flask import request
from io import StringIO
import os

app = Flask(__name__)

@app.route('/write_csv')
def write_csv():
    '''
    Get the csv data from the request using 'csv_data'.
    Write it to a file in the static folder using csv library.
    '''
    csv_data = request.args.get('csv_data')

    if not csv_data:
        return {'error': 'csv_data is required'}, 400

    # Ensure static folder exists
    os.makedirs('static', exist_ok=True)

    # Parse CSV data using csv.reader
    csv_file = StringIO(csv_data)
    reader = csv.reader(csv_file)
    rows = list(reader)

    # Write to file in static folder using csv.writer
    with open('static/output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return {'message': 'CSV written successfully'}, 200
