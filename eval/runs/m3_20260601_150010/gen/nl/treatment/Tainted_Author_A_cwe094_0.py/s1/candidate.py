from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/eval', methods=['POST', 'GET'])
def eval_dict():
    # Get file_contents from request
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        file_contents = data.get('file_contents', '')
    else:
        file_contents = request.args.get('file_contents', '')

    # Find first { and last }
    first_brace = file_contents.find('{')
    last_brace = file_contents.rfind('}')

    if first_brace == -1 or last_brace == -1 or first_brace >= last_brace:
        return jsonify({'error': 'No valid braces found'}), 400

    # Extract the substring between first { and last }
    dict_str = file_contents[first_brace:last_brace + 1]

    # Safely evaluate as dictionary using ast.literal_eval
    try:
        result = ast.literal_eval(dict_str)
        return jsonify(result)
    except (ValueError, SyntaxError) as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
