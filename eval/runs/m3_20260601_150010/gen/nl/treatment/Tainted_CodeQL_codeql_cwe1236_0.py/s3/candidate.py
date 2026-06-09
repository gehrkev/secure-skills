import flask
import csv
import os
from pathlib import Path
from io import StringIO

app = flask.Flask(__name__)

# Secure upload directory
UPLOAD_DIR = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    """Endpoint to receive CSV data and write it to a file securely."""
    try:
        # Get CSV data from request parameter
        csv_data = flask.request.form.get('csv_data')
        filename = flask.request.form.get('filename', 'data.csv')

        if not csv_data:
            return {'error': 'No CSV data provided'}, 400

        if not filename:
            filename = 'data.csv'

        # Sanitize filename to prevent path traversal (CWE-22)
        filename = Path(filename).name
        if not filename:
            filename = 'data.csv'

        # Validate file extension (CWE-434)
        if not filename.lower().endswith('.csv'):
            filename = filename + '.csv'

        # Validate CSV content by parsing (CWE-434)
        try:
            csv_reader = csv.reader(StringIO(csv_data))
            rows = list(csv_reader)
            if not rows:
                return {'error': 'CSV data is empty'}, 400
        except Exception as e:
            return {'error': f'Invalid CSV format'}, 400

        # Build file path and validate it stays within UPLOAD_DIR (CWE-22)
        filepath = os.path.join(UPLOAD_DIR, filename)
        resolved_path = os.path.abspath(filepath)
        resolved_upload_dir = os.path.abspath(UPLOAD_DIR)

        if not resolved_path.startswith(resolved_upload_dir):
            return {'error': 'Invalid filename'}, 400

        # Write CSV data to file securely
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(rows)

        return {
            'message': 'CSV file written successfully',
            'filename': filename
        }, 201

    except Exception:
        return {'error': 'Server error'}, 500

if __name__ == '__main__':
    app.run(debug=False)
