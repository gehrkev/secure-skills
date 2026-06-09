from flask import Flask, request, render_template
from markupsafe import escape
import unicodedata

app = Flask(__name__)

@app.route('/result')
def result():
    ui_data = request.args.get('ui_data', '')
    ui_data_escaped = escape(ui_data)
    ui_data_normalized = unicodedata.normalize('NFKC', str(ui_data_escaped))
    return render_template('result.html', ui_data=ui_data_normalized)
