from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def eval():
    file_contents = request.json.get('file_contents')

    # Strip everything before first { and after last }
    start = file_contents.find('{')
    end = file_contents.rfind('}')

    dict_str = file_contents[start:end+1]
    result = eval(dict_str)

    return jsonify(result)

if __name__ == '__main__':
    app.run()
