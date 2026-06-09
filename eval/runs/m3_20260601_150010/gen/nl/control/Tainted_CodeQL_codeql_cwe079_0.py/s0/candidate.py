from flask import Flask, request, render_template_string

app = Flask(__name__)

template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Hello</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
'''

@app.route('/')
def index():
    name = request.args.get('name', 'World')
    return render_template_string(template, name=name)

if __name__ == '__main__':
    app.run()
