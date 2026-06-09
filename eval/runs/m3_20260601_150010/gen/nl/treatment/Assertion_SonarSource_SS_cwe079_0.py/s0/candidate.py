from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/template_replaced', methods=['GET'])
def template_replaced():
    param = request.args.get('param', '')

    with open('../assets/templates/template.html', 'r') as f:
        template_content = f.read()

    return render_template_string(template_content, param=param)

if __name__ == '__main__':
    app.run()
