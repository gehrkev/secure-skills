import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/deleteImage', methods=['GET', 'POST'])
def delete_image():
    path = request.args.get('path') or request.form.get('path')

    try:
        os.remove(path)
        return "The file has been deleted"
    except FileNotFoundError:
        return "The file does not exist"

if __name__ == '__main__':
    app.run(debug=True)
