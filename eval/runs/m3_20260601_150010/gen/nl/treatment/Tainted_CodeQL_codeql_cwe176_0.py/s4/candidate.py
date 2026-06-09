from flask import Flask, render_template, request
from markupsafe import escape
import re

app = Flask(__name__)

@app.route('/result', methods=['GET', 'POST'])
def result():
    ui_data = request.args.get('ui_data', '') or request.form.get('ui_data', '')
    escaped_data = escape(ui_data)
    normalized_data = re.sub(r'\s+', ' ', str(escaped_data).strip())
    return render_template('result.html', ui_data=normalized_data)
