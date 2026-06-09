from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def eval_endpoint():
    file_contents = request.json.get('file_contents', '')

    # Find the first { and last }
    first_brace = file_contents.find('{')
    last_brace = file_contents.rfind('}')

    if first_brace == -1 or last_brace == -1 or first_brace > last_brace:
        return jsonify({'error': 'No valid dictionary found'}), 400

    # Extract the substring from first { to last }
    dict_string = file_contents[first_brace:last_brace + 1]

    # Evaluate as a dictionary
    try:
        result = eval(dict_string)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
