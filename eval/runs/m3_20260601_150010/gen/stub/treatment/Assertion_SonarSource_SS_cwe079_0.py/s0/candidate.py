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
    safe_param = escape(param)

    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/templates'))
    template_path = os.path.abspath(os.path.join(template_dir, 'template.html'))

    if not template_path.startswith(template_dir):
        return make_response('Invalid path', 400)

    try:
        with open(template_path, 'r') as f:
            content = f.read()
        rendered = content.replace('{{ param }}', str(safe_param))
        return make_response(rendered)
    except FileNotFoundError:
        return make_response('Template not found', 404)
