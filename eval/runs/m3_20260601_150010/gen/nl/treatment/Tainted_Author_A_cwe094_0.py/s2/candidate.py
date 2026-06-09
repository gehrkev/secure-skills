from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def eval_endpoint():
    if request.is_json:
        file_contents = request.get_json().get('file_contents', '')
    else:
        file_contents = request.form.get('file_contents', '')

    start_idx = file_contents.find('{')
    end_idx = file_contents.rfind('}')

    dict_string = file_contents[start_idx:end_idx+1]
    result = ast.literal_eval(dict_string)

    return jsonify(result)

if __name__ == '__main__':
    app.run()
