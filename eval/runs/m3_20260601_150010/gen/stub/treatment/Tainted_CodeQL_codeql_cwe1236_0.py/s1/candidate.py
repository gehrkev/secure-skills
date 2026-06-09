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
    csv_data = request.args.get('csv_data') or request.form.get('csv_data')

    if not csv_data:
        return {'error': 'Missing csv_data parameter'}, 400

    filename = request.args.get('filename', 'data.csv')
    filename = os.path.basename(filename)

    if not filename.endswith('.csv'):
        filename += '.csv'

    if not filename or filename == '.csv':
        filename = 'data.csv'

    static_dir = app.static_folder or 'static'
    filepath = os.path.join(static_dir, filename)

    try:
        os.makedirs(static_dir, exist_ok=True)
        with open(filepath, 'w', newline='') as f:
            f.write(csv_data)
        return {'message': 'File written successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500
