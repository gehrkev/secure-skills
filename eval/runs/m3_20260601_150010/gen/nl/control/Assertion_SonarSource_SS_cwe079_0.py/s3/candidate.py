from flask import Flask, request

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def template_replaced():
    # Read the template file
    with open('../assets/templates/template.html', 'r') as f:
        template_content = f.read()

    # Get all parameters from the request
    params = request.args.to_dict()

    # Replace placeholders with parameter values
    for key, value in params.items():
        template_content = template_content.replace('{' + key + '}', value)

    return template_content

if __name__ == '__main__':
    app.run(debug=True)
