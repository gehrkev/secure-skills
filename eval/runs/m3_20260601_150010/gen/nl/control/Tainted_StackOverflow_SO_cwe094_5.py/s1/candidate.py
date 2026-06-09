from flask import Flask, request

app = Flask(__name__)

@app.route('/get_value', methods=['POST', 'GET'])
def get_value():
    data = request.get_json() if request.is_json else request.args

    key = data.get('key')
    obj = data.get('object')

    if key is None or obj is None:
        return "Error: key and object are required", 400

    if not isinstance(obj, dict):
        return "Error: object must be a dictionary", 400

    value = obj.get(key)

    return str(value)

if __name__ == '__main__':
    app.run(debug=True)
