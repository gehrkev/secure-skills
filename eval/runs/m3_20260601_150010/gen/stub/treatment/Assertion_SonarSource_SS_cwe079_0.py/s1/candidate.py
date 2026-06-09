from flask import Flask, request, make_response
from markupsafe import escape
import os

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def no_template_engine_replace():
    '''
    Get param from request and replace it in this template: '../assets/templates/template.html'.
    :return: rendered template
    '''
    param = request.args.get('param', '')
    escaped_param = escape(param)

    template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'template.html'))
    safe_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates'))

    if not template_path.startswith(safe_dir):
        return "Access denied", 403

    try:
        with open(template_path, 'r') as f:
            template_content = f.read()

        rendered = template_content.replace('{{ param }}', str(escaped_param))

        response = make_response(rendered)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    except FileNotFoundError:
        return "Template not found", 404
