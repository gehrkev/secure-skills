from flask import Flask, request, make_response
import os
from markupsafe import escape

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def no_template_engine_replace():
    '''
    Get param from request and replace it in this template: '../assets/templates/template.html'.
    :return: rendered template
    '''
    param = request.args.get('param', '')

    template_path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), '../assets/templates/template.html')
    )

    base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
    if not template_path.startswith(base_dir):
        return make_response('Invalid template path', 400)

    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
    except FileNotFoundError:
        return make_response('Template not found', 404)

    safe_param = escape(param)

    result = template_content.replace('{{ param }}', safe_param)

    response = make_response(result)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response
