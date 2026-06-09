from flask import Flask, request, jsonify
import csv
import os
from pathlib import Path
from io import StringIO

app = Flask(__name__)

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(STATIC_FOLDER, exist_ok=True)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        csv_data = request.form.get('csv_data') or request.args.get('csv_data')
        filename = request.form.get('filename', 'data.csv') or request.args.get('filename', 'data.csv')

        if not csv_data:
            return jsonify({'error': 'No CSV data provided'}), 400

        filename = os.path.basename(filename)
        if not filename.endswith('.csv'):
            filename += '.csv'

        file_path = os.path.join(STATIC_FOLDER, filename)
        resolved_path = os.path.realpath(file_path)

        if not resolved_path.startswith(os.path.realpath(STATIC_FOLDER)):
            return jsonify({'error': 'Invalid file path'}), 400

        reader = csv.reader(StringIO(csv_data))

        with open(resolved_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in reader:
                writer.writerow(row)

        return jsonify({'message': 'CSV file created successfully', 'filename': filename}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
