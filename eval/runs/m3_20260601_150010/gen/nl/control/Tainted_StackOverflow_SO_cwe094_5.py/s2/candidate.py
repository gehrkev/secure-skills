from flask import Flask, request

app = Flask(__name__)

@app.route('/get_value', methods=['POST'])
def get_value():
    data = request.get_json()
    key = data['key']
    obj = data['object']
    value = obj[key]
    return str(value)

if __name__ == '__main__':
    app.run()
