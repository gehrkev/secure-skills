from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def template_replaced():
    # Get the parameter from the request query string
    value = request.args.get('value', '')

    # Read the template file
    template_path = os.path.join(os.path.dirname(__file__), '../assets/templates/template.html')
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Render the template with the parameter using Jinja2
    rendered = render_template_string(template_content, value=value)

    return rendered

if __name__ == '__main__':
    app.run()
