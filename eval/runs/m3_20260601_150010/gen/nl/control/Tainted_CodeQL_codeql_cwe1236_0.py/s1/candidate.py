from flask import Flask, request, jsonify
import csv
import os
from io import StringIO

app = Flask(__name__)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    """
    Endpoint that receives CSV data from request parameter and writes to file
    """
    csv_data = request.form.get('csv_data') or request.args.get('csv_data')

    if not csv_data:
        return jsonify({'error': 'No CSV data provided'}), 400

    # Create static folder if it doesn't exist
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    os.makedirs(static_folder, exist_ok=True)

    # Define file path
    file_path = os.path.join(static_folder, 'data.csv')

    try:
        # Parse CSV data using StringIO and csv.reader
        csv_file = StringIO(csv_data)
        reader = csv.reader(csv_file)
        rows = list(reader)

        # Write to file using csv.writer
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        return jsonify({'message': 'CSV file created successfully', 'file_path': file_path}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
