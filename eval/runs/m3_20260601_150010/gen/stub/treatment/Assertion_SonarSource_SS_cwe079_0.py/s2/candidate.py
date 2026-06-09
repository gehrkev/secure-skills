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
    # Get parameter from request
    param = request.args.get('param', '')

    # Escape parameter to prevent XSS (CWE-79)
    escaped_param = escape(param)

    # Construct safe path to template, preventing path traversal (CWE-22)
    template_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates', 'template.html')
    template_path = os.path.abspath(template_path)

    # Validate path is within expected directory
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates'))
    if not template_path.startswith(base_path):
        return make_response('Invalid template path', 400)

    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
    except FileNotFoundError:
        return make_response('Template not found', 404)
    except Exception:
        return make_response('Error reading template', 500)

    # Replace placeholder in template
    rendered = template_content.replace('{{ param }}', escaped_param)

    response = make_response(rendered)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response
