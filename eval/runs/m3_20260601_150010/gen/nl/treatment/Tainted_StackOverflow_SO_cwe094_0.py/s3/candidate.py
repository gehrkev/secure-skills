from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/contents_dict', methods=['GET', 'POST'])
def contents_dict():
    contents = request.args.get('contents') or request.form.get('contents')

    if contents is None:
        return jsonify({'error': 'contents parameter is required'}), 400

    try:
        result = ast.literal_eval(contents)
        if not isinstance(result, dict):
            return jsonify({'error': 'contents must evaluate to a dictionary'}), 400
        return jsonify(result)
    except (ValueError, SyntaxError):
        return jsonify({'error': 'Invalid dictionary format'}), 400

if __name__ == '__main__':
    app.run()
