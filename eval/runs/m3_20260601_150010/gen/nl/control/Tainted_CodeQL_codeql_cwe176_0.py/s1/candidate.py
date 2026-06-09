from flask import Flask, request, render_template
import html
import unicodedata

app = Flask(__name__)

@app.route('/result')
def result():
    ui_data = request.args.get('ui_data', '')
    escaped_data = html.escape(ui_data)
    normalized_data = unicodedata.normalize('NFC', escaped_data)
    return render_template('result.html', ui_data=normalized_data)

if __name__ == '__main__':
    app.run()
