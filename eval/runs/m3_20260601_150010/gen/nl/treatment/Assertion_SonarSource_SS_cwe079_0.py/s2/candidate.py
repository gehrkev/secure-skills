from flask import Flask, request
from jinja2 import Environment, FileSystemLoader
import os

app = Flask(__name__)

template_dir = os.path.join(os.path.dirname(__file__), '../assets/templates')
env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)

@app.route('/template_replaced', methods=['GET'])
def template_replaced():
    replacement_value = request.args.get('replacement', '')
    template = env.get_template('template.html')
    rendered = template.render(replacement=replacement_value)
    return rendered

if __name__ == '__main__':
    app.run()
