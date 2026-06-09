from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def evaluate():
    file_contents = request.json.get('file_contents') if request.json else request.form.get('file_contents')

    if not file_contents:
        return jsonify({'error': 'file_contents required'}), 400

    # Find the first { and last }
    start = file_contents.find('{')
    end = file_contents.rfind('}')

    if start == -1 or end == -1 or start > end:
        return jsonify({'error': 'No dictionary found'}), 400

    # Extract the dictionary string
    dict_str = file_contents[start:end+1]

    try:
        # Use ast.literal_eval instead of eval for security (CWE-94)
        result = ast.literal_eval(dict_str)
        return jsonify(result)
    except (ValueError, SyntaxError) as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
