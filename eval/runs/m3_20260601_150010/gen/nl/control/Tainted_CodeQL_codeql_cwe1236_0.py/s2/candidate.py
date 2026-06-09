import os
import csv
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ensure static folder exists
if not os.path.exists('static'):
    os.makedirs('static')


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    """Endpoint that receives CSV data and writes it to a file in the static folder."""
    # Get CSV data from request parameter
    csv_data = request.form.get('csv_data') or request.args.get('csv_data')

    if not csv_data:
        return jsonify({'error': 'No CSV data provided'}), 400

    try:
        # Define output file path in static folder
        filename = os.path.join('static', 'uploaded_data.csv')

        # Parse CSV data and write to file
        lines = csv_data.strip().split('\n')

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            for line in lines:
                # Split each line and write as a row
                row = line.split(',')
                writer.writerow(row)

        return jsonify({
            'message': 'CSV file written successfully',
            'filename': filename
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
