from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/contents_dict', methods=['GET', 'POST'])
def contents_dict():
    contents = request.values.get('contents')
    result = ast.literal_eval(contents)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
