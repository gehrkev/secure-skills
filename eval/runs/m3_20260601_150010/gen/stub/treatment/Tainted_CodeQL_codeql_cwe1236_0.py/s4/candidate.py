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
    csv_data = request.args.get('csv_data') or request.form.get('csv_data')

    if not csv_data:
        return 'No CSV data provided', 400

    try:
        filename = 'data.csv'
        filepath = os.path.join(app.static_folder, filename)

        abs_filepath = os.path.abspath(filepath)
        abs_static = os.path.abspath(app.static_folder)
        if not abs_filepath.startswith(abs_static):
            return 'Invalid file path', 400

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            reader = csv.reader(io.StringIO(csv_data))
            for row in reader:
                writer.writerow(row)

        return 'CSV written successfully', 200
    except Exception:
        return 'Error writing CSV file', 500
