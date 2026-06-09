from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/eval', methods=['POST', 'GET'])
def eval_endpoint():
    try:
        # Get file_contents from request
        if request.method == 'POST':
            data = request.get_json() or request.form
        else:
            data = request.args

        file_contents = data.get('file_contents')

        if not file_contents:
            return jsonify({'error': 'file_contents not provided'}), 400

        # Find first { and last }
        start = file_contents.find('{')
        end = file_contents.rfind('}')

        if start == -1 or end == -1 or start >= end:
            return jsonify({'error': 'No valid dictionary found'}), 400

        # Strip to just the dictionary part
        dict_str = file_contents[start:end+1]

        # Evaluate as dictionary
        result = eval(dict_str)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
