import os
import csv
import io
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ensure static folder exists
STATIC_FOLDER = 'static'
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    # Get CSV data from request parameter
    csv_data = request.form.get('csv_data') or request.args.get('csv_data')

    if not csv_data:
        return jsonify({'error': 'No CSV data provided'}), 400

    try:
        # Parse CSV data using csv library
        csv_reader = csv.reader(io.StringIO(csv_data))
        rows = list(csv_reader)

        # Write CSV data to file in static folder
        filename = os.path.join(STATIC_FOLDER, 'data.csv')

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        return jsonify({'success': True, 'message': f'CSV data written to {filename}'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
