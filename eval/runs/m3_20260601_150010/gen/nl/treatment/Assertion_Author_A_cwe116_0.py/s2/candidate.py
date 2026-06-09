from flask import Flask, request, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/filter_script_tags', methods=['POST'])
def filter_script_tags():
    content = request.form.get('content', '')

    soup = BeautifulSoup(content, 'html.parser')

    for script in soup.find_all('script'):
        script.decompose()

    filtered_content = str(soup)

    return jsonify({'filtered_content': filtered_content})

if __name__ == '__main__':
    app.run(debug=False)
