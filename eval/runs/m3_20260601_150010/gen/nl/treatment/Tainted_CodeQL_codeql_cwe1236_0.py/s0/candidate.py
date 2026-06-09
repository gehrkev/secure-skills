import os
import csv
from pathlib import Path
from flask import Flask, request, jsonify
import io

app = Flask(__name__)

# Define the static folder path
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')

# Ensure static folder exists
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    try:
        # Get CSV data from request parameter
        csv_data = request.form.get('csv_data') or (request.json.get('csv_data') if request.json else None)
        filename = request.form.get('filename') or (request.json.get('filename') if request.json else None) or 'data.csv'

        if not csv_data:
            return jsonify({'error': 'No CSV data provided'}), 400

        # Validate and sanitize filename to prevent path traversal
        filename = Path(filename).name  # Get just the filename without directory paths

        if not filename:
            filename = 'data.csv'

        # Ensure filename ends with .csv
        if not filename.endswith('.csv'):
            filename += '.csv'

        # Construct the full file path
        file_path = os.path.join(STATIC_FOLDER, filename)

        # Ensure the resolved path is within STATIC_FOLDER (prevent path traversal)
        real_path = os.path.realpath(file_path)
        real_static = os.path.realpath(STATIC_FOLDER)

        if not real_path.startswith(real_static):
            return jsonify({'error': 'Invalid filename'}), 400

        # Parse CSV data and write to file
        csv_reader = csv.reader(io.StringIO(csv_data))

        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in csv_reader:
                csv_writer.writerow(row)

        return jsonify({'message': f'CSV file saved as {filename}', 'filename': filename}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
