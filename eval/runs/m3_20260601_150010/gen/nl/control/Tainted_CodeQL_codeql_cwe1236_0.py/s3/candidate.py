import os
import csv
from io import StringIO
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ensure static folder exists
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)


@app.route('/upload-csv', methods=['POST', 'GET'])
def upload_csv():
    # Get CSV data from request parameter
    csv_data = request.args.get('data') or request.form.get('data')

    if not csv_data:
        return jsonify({'error': 'No CSV data provided'}), 400

    try:
        # Write to file in static folder
        file_path = os.path.join(STATIC_FOLDER, 'uploaded.csv')

        # Parse CSV data using csv library
        csv_file = StringIO(csv_data)
        reader = csv.reader(csv_file)

        # Write parsed CSV to file
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in reader:
                writer.writerow(row)

        return jsonify({
            'message': 'CSV file written successfully',
            'file_path': 'static/uploaded.csv'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
