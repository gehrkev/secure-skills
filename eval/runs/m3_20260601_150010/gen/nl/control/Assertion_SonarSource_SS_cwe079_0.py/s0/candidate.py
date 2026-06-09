from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def template_replaced():
    # Get parameter from request
    replacement_value = request.args.get('value')

    # Read template file
    template_path = os.path.join(os.path.dirname(__file__), '../assets/templates/template.html')
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Render template with the parameter
    rendered = render_template_string(template_content, value=replacement_value)

    return rendered

if __name__ == '__main__':
    app.run()
