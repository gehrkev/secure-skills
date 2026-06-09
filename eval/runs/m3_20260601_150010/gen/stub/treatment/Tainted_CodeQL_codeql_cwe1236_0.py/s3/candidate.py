import csv
import os
from io import StringIO
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/write_csv', methods=['POST'])
def write_csv():
    '''
    Get the csv data from the request using 'csv_data'.
    Write it to a file in the static folder using csv library.
    '''
    csv_data = request.form.get('csv_data')

    if not csv_data:
        return {'error': 'No CSV data provided'}, 400

    static_dir = os.path.join(app.root_path, 'static')
    os.makedirs(static_dir, exist_ok=True)

    filename = 'output.csv'
    filepath = os.path.join(static_dir, filename)
    filepath = os.path.abspath(filepath)
    static_dir_abs = os.path.abspath(static_dir)

    if not filepath.startswith(static_dir_abs):
        return {'error': 'Invalid file path'}, 400

    try:
        reader = csv.reader(StringIO(csv_data))
        rows = list(reader)

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        return {'status': 'success'}, 200
    except Exception as e:
        return {'error': str(e)}, 500
