from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def eval_endpoint():
    data = request.get_json() or {}
    file_contents = data.get('file_contents', '')

    start_idx = file_contents.find('{')
    end_idx = file_contents.rfind('}')

    dict_str = file_contents[start_idx:end_idx + 1]

    result = eval(dict_str)

    return jsonify(result)

if __name__ == '__main__':
    app.run()
