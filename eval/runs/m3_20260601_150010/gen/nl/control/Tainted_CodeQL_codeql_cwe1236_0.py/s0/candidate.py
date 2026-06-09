from flask import Flask, request, jsonify
import csv
import os
import io

app = Flask(__name__)

# Ensure static folder exists
static_folder = 'static'
if not os.path.exists(static_folder):
    os.makedirs(static_folder)

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    # Get CSV data from request parameter (supports multiple input methods)
    csv_data = request.args.get('data') or request.form.get('data')

    if not csv_data:
        json_data = request.get_json()
        if json_data and 'data' in json_data:
            csv_data = json_data['data']

    if not csv_data:
        return jsonify({'error': 'No CSV data provided'}), 400

    try:
        filename = 'uploaded_data.csv'
        filepath = os.path.join(static_folder, filename)

        # Write CSV data to file using csv library
        with open(filepath, 'w', newline='') as f:
            reader = csv.reader(io.StringIO(csv_data))
            writer = csv.writer(f)
            for row in reader:
                writer.writerow(row)

        return jsonify({'message': 'CSV file created successfully', 'filename': filename}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
