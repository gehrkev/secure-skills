from flask import Flask, request, render_template
import html
import unicodedata

app = Flask(__name__)

@app.route('/result', methods=['GET'])
def result():
    # Retrieve the ui_data parameter from the request
    ui_data = request.args.get('ui_data', '')

    # Escape the ui_data to prevent XSS attacks
    ui_data = html.escape(ui_data)

    # Normalize the ui_data using NFKD normalization
    ui_data = unicodedata.normalize('NFKD', ui_data)

    # Render using result.html template
    return render_template('result.html', ui_data=ui_data)
