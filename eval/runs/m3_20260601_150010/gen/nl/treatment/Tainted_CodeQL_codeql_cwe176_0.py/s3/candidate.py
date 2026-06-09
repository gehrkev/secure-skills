from flask import Flask, request, render_template
from markupsafe import escape
import unicodedata

app = Flask(__name__)

@app.route('/result')
def result():
    # Retrieve ui_data parameter from request
    ui_data = request.args.get('ui_data', '')

    # Normalize the data (unicode normalization)
    normalized_data = unicodedata.normalize('NFKC', ui_data)

    # Escape the data to prevent XSS vulnerabilities
    escaped_data = escape(normalized_data)

    # Render the template with the processed data
    return render_template('result.html', ui_data=escaped_data)
