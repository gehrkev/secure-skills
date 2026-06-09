from flask import Flask, request, render_template
from markupsafe import escape
import unicodedata

app = Flask(__name__)

def normalize_text(text):
    """Normalize text by removing extra whitespace and standardizing unicode."""
    text = ' '.join(text.split())
    text = unicodedata.normalize('NFKD', text)
    return text

@app.route('/result')
def result():
    # Get the ui_data parameter from the request
    ui_data = request.args.get('ui_data', '')

    # Escape the data
    ui_data = escape(ui_data)

    # Normalize the data
    ui_data = normalize_text(str(ui_data))

    # Render the template
    return render_template('result.html', ui_data=ui_data)

if __name__ == '__main__':
    app.run(debug=True)
