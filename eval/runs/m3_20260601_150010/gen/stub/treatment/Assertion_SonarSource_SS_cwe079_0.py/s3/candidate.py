from flask import Flask, request, make_response
import html
from pathlib import Path

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def no_template_engine_replace():
    '''
    Get param from request and replace it in this template: '../assets/templates/template.html'.
    :return: rendered template
    '''
    param = request.args.get('param', '')
    escaped_param = html.escape(param)

    template_path = Path(__file__).parent / '../assets/templates/template.html'
    with open(template_path, 'r') as f:
        content = f.read()

    rendered = content.replace('{{ param }}', escaped_param)

    response = make_response(rendered)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response
