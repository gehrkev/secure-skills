from flask import Flask, request, jsonify
import ast

app = Flask(__name__)

@app.route('/eval', methods=['POST'])
def eval_endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400

        file_contents = data.get('file_contents', '')

        # Find the first { and last }
        start = file_contents.find('{')
        end = file_contents.rfind('}')

        if start == -1 or end == -1 or start >= end:
            return jsonify({'error': 'No valid dictionary found'}), 400

        # Extract the substring from first { to last }
        dict_str = file_contents[start:end+1]

        # Safely evaluate as a dictionary using ast.literal_eval
        result = ast.literal_eval(dict_str)

        return jsonify(result)
    except (ValueError, SyntaxError) as e:
        return jsonify({'error': 'Invalid dictionary format'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid request'}), 400

if __name__ == '__main__':
    app.run()
