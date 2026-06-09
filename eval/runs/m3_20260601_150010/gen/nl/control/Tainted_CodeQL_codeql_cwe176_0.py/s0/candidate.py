from flask import Flask, request, render_template
from markupsafe import escape
import unicodedata

app = Flask(__name__)

@app.route('/result')
def result():
    # Get ui_data parameter from request
    ui_data = request.args.get('ui_data', '')

    # Escape the data to prevent XSS
    escaped_data = escape(ui_data)

    # Normalize the data (remove extra whitespace and normalize unicode)
    normalized_data = unicodedata.normalize('NFKD', str(escaped_data))
    normalized_data = ' '.join(normalized_data.split())

    # Render using result.html template
    return render_template('result.html', ui_data=normalized_data)

if __name__ == '__main__':
    app.run()
