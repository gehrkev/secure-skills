from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/create_variable', methods=['GET', 'POST'])
def create_variable():
    # Get the str_var parameter from request
    str_var = request.args.get('str_var') or request.form.get('str_var')

    # Check if parameter was provided
    if str_var is None:
        return jsonify({'error': 'Missing str_var parameter'}), 400

    # Store the variable and return it
    return jsonify({'str_var': str_var})

if __name__ == '__main__':
    app.run()
