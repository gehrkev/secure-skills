from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/deleteImage')
def delete_image():
    path = request.args.get('path')

    if path and os.path.exists(path):
        os.remove(path)
        return "The file has been deleted"

    return "The file does not exist"

if __name__ == '__main__':
    app.run()
