from flask import Flask, request

app = Flask(__name__)

@app.route('/get_value', methods=['POST'])
def get_value():
    data = request.get_json()
    key = data.get('key')
    obj = data.get('object')

    value = obj.get(key) if obj and isinstance(obj, dict) else None
    return str(value)

if __name__ == '__main__':
    app.run()
