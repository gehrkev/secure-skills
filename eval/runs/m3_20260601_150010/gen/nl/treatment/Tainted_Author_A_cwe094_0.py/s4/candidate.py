from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def eval_endpoint():
    try:
        data = request.get_json()
        file_contents = data.get('file_contents', '')

        # Find first { and last }
        start_idx = file_contents.find('{')
        end_idx = file_contents.rfind('}')

        if start_idx == -1 or end_idx == -1 or start_idx > end_idx:
            return jsonify({'error': 'No valid dictionary found'}), 400

        # Extract the substring between first { and last }
        dict_str = file_contents[start_idx:end_idx + 1]

        # Safely evaluate as a dictionary using ast.literal_eval
        result = ast.literal_eval(dict_str)

        if not isinstance(result, dict):
            return jsonify({'error': 'Result is not a dictionary'}), 400

        return jsonify(result)
    except (ValueError, SyntaxError) as e:
        return jsonify({'error': f'Invalid dictionary format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
