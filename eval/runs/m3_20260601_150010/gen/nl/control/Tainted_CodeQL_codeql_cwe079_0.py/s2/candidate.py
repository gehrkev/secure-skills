from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name', 'World')
    template = '''
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Hello, {{ name }}!</h1>
    </body>
    </html>
    '''
    return render_template_string(template, name=name)

if __name__ == '__main__':
    app.run()
