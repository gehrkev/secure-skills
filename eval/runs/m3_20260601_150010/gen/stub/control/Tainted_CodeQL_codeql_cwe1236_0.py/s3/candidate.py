import csv
import os
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/write_csv', methods=['GET', 'POST'])
def write_csv():
    '''
    Get the csv data from the request using 'csv_data'.
    Write it to a file in the static folder using csv library.
    '''
    csv_data = request.args.get('csv_data') or request.form.get('csv_data')

    if not csv_data:
        return {'error': 'No csv_data provided'}, 400

    os.makedirs('static', exist_ok=True)

    with open('static/output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for line in csv_data.strip().split('\n'):
            writer.writerow(line.split(','))

    return {'success': True}
