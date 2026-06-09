from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/parse_string_to_dict', methods=['GET', 'POST'])
def parse_string_to_dict():
    formatted_str = request.args.get('formattedStr') or request.form.get('formattedStr')
    if formatted_str is None:
        return jsonify({'error': 'formattedStr parameter is required'}), 400

    try:
        result = eval(formatted_str)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
