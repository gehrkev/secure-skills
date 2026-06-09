from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def template_replaced():
    # Get the parameter from the request
    replacement_value = request.args.get('value', '')

    # Read the template file
    try:
        with open('../assets/templates/template.html', 'r') as f:
            template_content = f.read()
    except FileNotFoundError:
        return "Template file not found", 404

    # Render the template with the replacement value using Jinja2
    # This automatically escapes the value to prevent XSS attacks
    rendered = render_template_string(template_content, replacement_value=replacement_value)

    return rendered

if __name__ == '__main__':
    app.run(debug=True)
