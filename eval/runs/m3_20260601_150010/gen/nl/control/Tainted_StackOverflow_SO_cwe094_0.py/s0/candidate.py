from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/contents_dict', methods=['GET', 'POST'])
def contents_dict():
    contents = request.args.get('contents') or request.form.get('contents')

    if contents is None:
        return {'error': 'contents parameter is required'}, 400

    try:
        result = ast.literal_eval(contents)
        return jsonify(result)
    except (ValueError, SyntaxError, TypeError):
        return {'error': 'Invalid dictionary format'}, 400

if __name__ == '__main__':
    app.run()
