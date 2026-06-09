import csv
import io
import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/write_csv', methods=['POST'])
def write_csv():
    '''
    Get the csv data from the request using 'csv_data'.
    Write it to a file in the static folder using csv library.
    '''
    try:
        # Get csv_data from request (supports JSON and form data)
        if request.is_json:
            csv_data = request.get_json().get('csv_data')
        else:
            csv_data = request.form.get('csv_data')

        if not csv_data or not isinstance(csv_data, str):
            return {'error': 'Missing or invalid csv_data'}, 400

        # Parse CSV to validate format and extract rows
        rows = list(csv.reader(io.StringIO(csv_data)))

        if not rows:
            return {'error': 'No data in csv_data'}, 400

        # Create safe filepath (prevent path traversal)
        filename = 'data.csv'
        filepath = os.path.join(app.static_folder, filename)

        # Verify resolved path is within static folder
        resolved_path = os.path.abspath(filepath)
        resolved_static = os.path.abspath(app.static_folder)
        if not resolved_path.startswith(resolved_static):
            return {'error': 'Path traversal detected'}, 400

        # Write CSV to file using csv writer
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        return {'success': True, 'message': 'CSV written successfully'}, 200

    except Exception as e:
        return {'error': str(e)}, 500
