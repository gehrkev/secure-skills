from flask import Flask, request, jsonify
import csv
import os
import re
from io import StringIO

app = Flask(__name__)

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(STATIC_FOLDER, exist_ok=True)

def sanitize_filename(filename):
    filename = os.path.basename(filename)
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    if not filename.endswith('.csv'):
        filename += '.csv'
    return filename

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    try:
        csv_data = request.form.get('csv_data')
        if not csv_data and request.json:
            csv_data = request.json.get('csv_data')

        filename = request.form.get('filename', 'data.csv')
        if not filename and request.json:
            filename = request.json.get('filename', 'data.csv')

        if not csv_data:
            return jsonify({'error': 'No CSV data provided'}), 400

        safe_filename = sanitize_filename(filename)
        file_path = os.path.join(STATIC_FOLDER, safe_filename)

        if not os.path.abspath(file_path).startswith(os.path.abspath(STATIC_FOLDER)):
            return jsonify({'error': 'Invalid file path'}), 400

        csv_buffer = StringIO(csv_data)
        csv_reader = csv.reader(csv_buffer)

        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in csv_reader:
                csv_writer.writerow(row)

        return jsonify({'success': True, 'filename': safe_filename}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
