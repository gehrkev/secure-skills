from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/result')
def result():
    ui_data = request.args.get('ui_data', '')
    escaped_data = escape(ui_data)
    normalized_data = ' '.join(str(escaped_data).split())
    return render_template('result.html', ui_data=normalized_data)
