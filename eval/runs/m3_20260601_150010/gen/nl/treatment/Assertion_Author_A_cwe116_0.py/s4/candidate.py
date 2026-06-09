from flask import Flask, request, jsonify
from html.parser import HTMLParser

app = Flask(__name__)

class ScriptTagRemover(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
        self.in_script = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'script':
            self.in_script = True
        else:
            self.fed.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if tag.lower() == 'script':
            self.in_script = False
        else:
            self.fed.append(f'</{tag}>')

    def handle_data(self, data):
        if not self.in_script:
            self.fed.append(data)

    def get_data(self):
        return ''.join(self.fed)

def remove_script_tags(content):
    parser = ScriptTagRemover()
    parser.feed(content)
    return parser.get_data()

@app.route('/filter_script_tags', methods=['POST'])
def filter_script_tags():
    if request.is_json:
        content = request.get_json().get('content', '')
    else:
        content = request.form.get('content', '')

    filtered_content = remove_script_tags(content)
    return jsonify({'filtered_content': filtered_content})

if __name__ == '__main__':
    app.run()
