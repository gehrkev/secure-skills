from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def template_replaced():
    # Get the parameter from the request
    replacement = request.args.get('replacement', '')

    # Construct the path to the template file
    template_path = os.path.join(os.path.dirname(__file__), '../assets/templates/template.html')

    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Render the template with the replacement parameter
    rendered = render_template_string(template_content, replacement=replacement)

    return rendered

if __name__ == '__main__':
    app.run(debug=True)
