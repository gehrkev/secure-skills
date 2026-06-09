from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    template = '<h1>Hello, {{ name }}!</h1>'
    return render_template_string(template, name=name)

if __name__ == '__main__':
    app.run()
