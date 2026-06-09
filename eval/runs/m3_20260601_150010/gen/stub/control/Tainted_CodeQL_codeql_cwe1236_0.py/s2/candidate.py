import csv
import os
import io
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/write_csv')
def write_csv():
    '''
    Get the csv data from the request using 'csv_data'.
    Write it to a file in the static folder using csv library.
    '''
    csv_data = request.args.get('csv_data')

    if not csv_data:
        return 'No CSV data provided', 400

    filepath = os.path.join(app.static_folder, 'output.csv')

    reader = csv.reader(io.StringIO(csv_data))
    rows = list(reader)

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return 'CSV written successfully'
