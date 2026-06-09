from flask import Flask, request, jsonify
import csv
import os
import io

app = Flask(__name__)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    csv_content = request.form.get('csv_data')
    filename = request.form.get('filename', 'data.csv')

    if not csv_content:
        return jsonify({'error': 'No CSV data provided'}), 400

    if not all(c.isalnum() or c in ['-', '_', '.'] for c in filename):
        return jsonify({'error': 'Invalid filename'}), 400

    if not filename.endswith('.csv'):
        filename += '.csv'

    static_dir = os.path.join(app.root_path, 'static')
    file_path = os.path.join(static_dir, filename)

    file_path = os.path.abspath(file_path)
    static_dir = os.path.abspath(static_dir)

    if not file_path.startswith(static_dir):
        return jsonify({'error': 'Invalid file path'}), 400

    os.makedirs(static_dir, exist_ok=True)

    try:
        csv_reader = csv.reader(io.StringIO(csv_content))
        rows = list(csv_reader)

        if not rows:
            return jsonify({'error': 'CSV data is empty'}), 400

        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        return jsonify({'message': 'CSV file uploaded successfully', 'filename': filename}), 200
    except csv.Error as e:
        return jsonify({'error': f'Invalid CSV format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
