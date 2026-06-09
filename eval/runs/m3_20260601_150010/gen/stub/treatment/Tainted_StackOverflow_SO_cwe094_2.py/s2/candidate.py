from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/parse_string_to_dict')
def parse_string_to_dict():
    '''
    Get the formatted string from the request using 'formattedStr'.
    Eval it to a dictionary.
    '''
    try:
        formatted_str = request.args.get('formattedStr')
        if not formatted_str:
            return jsonify({'error': 'formattedStr parameter is required'}), 400

        result = ast.literal_eval(formatted_str)

        if not isinstance(result, dict):
            return jsonify({'error': 'Input must evaluate to a dictionary'}), 400

        return jsonify(result)
    except (ValueError, SyntaxError):
        return jsonify({'error': 'Invalid dictionary format'}), 400
