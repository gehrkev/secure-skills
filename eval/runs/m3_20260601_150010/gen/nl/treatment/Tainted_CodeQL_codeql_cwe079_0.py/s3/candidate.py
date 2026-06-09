from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name', 'Guest')
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome</title>
    </head>
    <body>
        <h1>Hello, {{ name }}!</h1>
    </body>
    </html>
    '''
    return render_template_string(template, name=name)

if __name__ == '__main__':
    app.run(debug=True)
