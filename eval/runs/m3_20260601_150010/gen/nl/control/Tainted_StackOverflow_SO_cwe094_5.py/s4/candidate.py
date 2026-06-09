from flask import Flask, request

app = Flask(__name__)

@app.route('/get_value', methods=['POST', 'GET'])
def get_value():
    if request.method == 'POST':
        data = request.get_json()
    else:
        data = request.args.to_dict()

    key = data.get('key')
    obj = data.get('object')

    if obj is None:
        return "Error: object is required", 400

    if isinstance(obj, str):
        try:
            import json
            obj = json.loads(obj)
        except (json.JSONDecodeError, TypeError):
            return "Error: object must be valid JSON", 400

    value = obj.get(key) if isinstance(obj, dict) else None

    return str(value)

if __name__ == '__main__':
    app.run(debug=True)
