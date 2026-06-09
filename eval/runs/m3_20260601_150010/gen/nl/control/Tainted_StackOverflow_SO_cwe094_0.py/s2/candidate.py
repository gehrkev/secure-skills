from flask import Flask, request

app = Flask(__name__)

@app.route('/contents_dict', methods=['GET', 'POST'])
def contents_dict():
    contents = request.args.get('contents') or request.form.get('contents')
    result = eval(contents)
    return result

if __name__ == '__main__':
    app.run()
