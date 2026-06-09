from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def template_replaced():
    # Get parameter from request query string
    param_value = request.args.get('value', '')

    # Construct path to template file
    template_path = os.path.join(os.path.dirname(__file__), '../assets/templates/template.html')

    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Replace placeholder with parameter value
    rendered_content = template_content.replace('{{VALUE}}', param_value)

    return rendered_content

if __name__ == '__main__':
    app.run()
