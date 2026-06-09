from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def eval_endpoint():
    file_contents = request.json.get('file_contents', '')

    start_idx = file_contents.find('{')
    end_idx = file_contents.rfind('}')

    if start_idx == -1 or end_idx == -1:
        return jsonify({'error': 'No valid dictionary found'}), 400

    dict_str = file_contents[start_idx:end_idx+1]

    try:
        result = eval(dict_str)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
