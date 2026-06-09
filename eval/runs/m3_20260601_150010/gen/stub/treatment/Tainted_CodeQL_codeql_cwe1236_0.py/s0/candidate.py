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

    if not csv_data:
        return {'error': 'No csv_data provided'}, 400

    filename = 'output.csv'
    filepath = os.path.join(app.static_folder, filename)

    if not os.path.abspath(filepath).startswith(os.path.abspath(app.static_folder)):
        return {'error': 'Invalid file path'}, 400

    try:
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            for line in csv_data.strip().split('\n'):
                if line:
                    writer.writerow(line.split(','))
        return {'message': 'CSV file written successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500
