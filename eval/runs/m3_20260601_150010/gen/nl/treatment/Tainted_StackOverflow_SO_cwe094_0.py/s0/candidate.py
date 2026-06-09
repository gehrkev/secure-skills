import flask
import ast

app = flask.Flask(__name__)

@app.route('/contents_dict')
def contents_dict():
    contents = flask.request.args.get('contents')
    result = ast.literal_eval(contents)
    return result

if __name__ == '__main__':
    app.run()
