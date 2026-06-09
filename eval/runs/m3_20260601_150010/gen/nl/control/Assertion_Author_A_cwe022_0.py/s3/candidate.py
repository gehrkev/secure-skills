from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/deleteImage', methods=['GET', 'POST'])
def delete_image():
    path = request.args.get('path') or request.form.get('path')

    if os.path.exists(path):
        os.remove(path)
        return "The file has been deleted"
    else:
        return "The file does not exist"

if __name__ == '__main__':
    app.run()
