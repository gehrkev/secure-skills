from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/parse_string_to_dict', methods=['GET', 'POST'])
def parse_string_to_dict():
    try:
        formatted_str = request.args.get('formattedStr') or request.form.get('formattedStr')

        if request.is_json:
            json_data = request.get_json()
            if json_data and 'formattedStr' in json_data:
                formatted_str = json_data['formattedStr']

        if not formatted_str:
            return jsonify({'error': 'formattedStr parameter is required'}), 400

        result = ast.literal_eval(formatted_str)

        if not isinstance(result, dict):
            return jsonify({'error': 'Input must evaluate to a dictionary'}), 400

        return jsonify(result)
    except (ValueError, SyntaxError) as e:
        return jsonify({'error': f'Invalid dictionary format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
