from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/contents_dict', methods=['GET', 'POST'])
def contents_dict():
    try:
        contents = request.args.get('contents') or request.form.get('contents')

        if contents is None:
            return jsonify({'error': 'contents parameter is required'}), 400

        result = ast.literal_eval(contents)
        return jsonify(result)
    except (ValueError, SyntaxError):
        return jsonify({'error': 'Invalid dictionary format'}), 400

if __name__ == '__main__':
    app.run()
