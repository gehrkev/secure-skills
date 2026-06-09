from flask import Flask, request

app = Flask(__name__)

@app.route('/create_variable')
def create_variable():
    str_var = request.args.get('str_var')
    return str_var

if __name__ == '__main__':
    app.run()
