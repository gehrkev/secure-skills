from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/install', methods=['GET', 'POST'])
def install():
    package = request.args.get('package') or request.form.get('package')
    if package:
        subprocess.run(['pip', 'install', package], check=False)
        return package
    return 'No package specified', 400

if __name__ == '__main__':
    app.run()
