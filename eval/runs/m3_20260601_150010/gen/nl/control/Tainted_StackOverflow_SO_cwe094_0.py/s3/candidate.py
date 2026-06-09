from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/contents_dict', methods=['GET', 'POST'])
def contents_dict():
    contents = request.args.get('contents') or request.form.get('contents')

    if not contents and request.is_json:
        data = request.get_json() or {}
        contents = data.get('contents')

    result = eval(contents)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
