from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def template_replaced():
    # Get the replacement value from query parameter
    replacement = request.args.get('replacement', '')

    # Read the template file
    template_path = '../assets/templates/template.html'
    with open(template_path, 'r') as f:
        template_content = f.read()

    # Render template with the replacement value
    # Jinja2 auto-escapes variables to prevent XSS attacks
    rendered = render_template_string(template_content, replacement=replacement)

    return rendered

if __name__ == '__main__':
    app.run()
